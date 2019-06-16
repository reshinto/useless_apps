"""
IEX API data
__version__ 0.4
"""
import json  # required to convert string to python object
import requests
import pandas as pd
from pandas.io.json import json_normalize


class IEX:
    """
    IEX API
    [+] Get data from IEX website as string,
        then convert all string to JSON format.
    [+] Use the view_table method to flatten the JSON to a table (PANDAS api)
    [+] If SQL is preferred, convert JSON to SQL with your own methods.
    [+] The get_price method returns a float number, NOT JSON.
    [+] Some methods require additional parameters input
    [+] Methods that have yet to be implemented are assigned with pass,
        because it does not seem useful for implementation at the moment.
    [+] Docs in methods are mostly taken from IEX api developer website
        [-] https://iextrading.com/developer/docs/#getting-started
        [-] Refer to the above link for more information
        [-] JSON sample are included for easy development purposes
    [+] This API does not require additional APIs to run, however, data reading
        will be a chore.
    """

    def __init__(self, *symbols):
        self.prefix = "https://api.iextrading.com/1.0"
        self.symbols = self.get_symbols(*symbols)

    def invalid_args(self):
        if len(self.symbols.split(",")) > 1:
            raise ValueError("Only single arg input are allowed")

    @staticmethod
    def get_data(url):
        """get URL and return data as string"""
        return requests.get("{}".format(url)).text

    @staticmethod
    def get_symbols(*args):
        """
        Get single or multi symbol input(s) and return as string
        """
        if len(args) == 1:
            # unlock nested tuple to get string input
            return args[0].upper()
        return ",".join([arg.upper() for arg in args])

    @staticmethod
    def view_table(json_data):
        """
        Convert json data to table in pandas
        Need to call main key with json_data
        e.g.:
            appl = Iex("appl")
        json_data = appl.get_quotes()
        print(appl.view_table(json_data["quote"])
        """
        return pd.DataFrame(json_normalize(json_data))

    def get_batch(self):
        """
        GET /stock/market/batch
        [+] // .../symbol
            {
            "quote": {...},
            "news": [...],
            "chart": [...]
            }
        [+] // .../market
            {
            "AAPL" : {
                "quote": {...},
                "news": [...],
                "chart": [...]
            },
            "FB" : {
                "quote": {...},
                "news": [...],
                "chart": [...]
            },
            }
        """
        batch = f"/stock/market/batch?symbols={self.symbols}" +\
            "&types=quote,news,chart&range=1m&last=5"
        url = self.prefix + batch
        return json.loads(self.get_data(url))

    def get_single_batch(self):
        """
        GET /stock/{symbol}/batch
        [+] // .../symbol
            {
            "quote": {...},
            "news": [...],
            "chart": [...]
            }
        [+] // .../market
            {
                "AAPL" : {
                    "quote": {...},
                    "news": [...],
                    "chart": [...]
                },
                "FB" : {
                    "quote": {...},
                    "news": [...],
                    "chart": [...]
                }, ...
            }
        """
        self.invalid_args()
        batch = f"/stock/{self.symbols}" +\
            "/batch?types=quote,news,chart&range=1m&last=1"
        url = self.prefix + batch
        return json.loads(self.get_data(url))

    def get_book(self):
        """
        GET /stock/{symbol}/book
        {
          "quote": {...},
          "bids": [...],
          "asks": [...],
          "trades": [...],
          "systemEvent": {...},
        }
        """
        self.invalid_args()
        book = f"/stock/{self.symbols}/book"
        url = self.prefix + book
        return json.loads(self.get_data(url))

    def get_charts(self, period=None, parameter=None):
        """
        GET /stock/{symbol}/chart/{range}
        period:
            5y: 5 years, 2y: 2 years, 1y: 1 year, ytd: year to date,
            6m: 6 months, 3m: 3 months, 1m: 1 month(default), 1d: 1 day,
            date: specific date(YYYYMMDD) e.g.: 20180129,
            dynamic: 1 day(return 1d or 1m)
        # TODO
        Parameters:
            chartReset: boolean. If true, 1d chart will reset at midnight
                        instead of the default behavior of 9:30am ET.
            chartSimplify: boolean. If true, runs a polyline simplification
                           using the Douglas-Peucker algorithm.
                           This is useful if plotting sparkline charts.
            chartInterval: number. If passed, chart data will return every
                           Nth element as defined by chartInterval
            changeFromClose: boolean. If true, changeOverTime and
                             marketChangeOverTime will be relative to previous
                             day close instead of the first value.
            chartLast: number. If passed, chart data will return the last
                       N elements
        [+] // .../1d
            [
                {
                    "date": "20171215"
                    "minute": "09:30",
                    "label": "09:30 AM",
                    "high": 143.98,
                    "low": 143.775,
                    "average": 143.889,
                    "volume": 3070,
                    "notional": 441740.275,
                    "numberOfTrades": 20,
                    "marktHigh": 143.98,
                    "marketLow": 143.775,
                    "marketAverage": 143.889,
                    "marketVolume": 3070,
                    "marketNotional": 441740.275,
                    "marketNumberOfTrades": 20,
                    "open": 143.98,
                    "close": 143.775,
                    "marktOpen": 143.98,
                    "marketClose": 143.775,
                    "changeOverTime": -0.0039,
                    "marketChangeOverTime": -0.004
                } // , { ... }
            ]
        [+] // .../3m
            [
                {
                    "date": "2017-04-03",
                    "open": 143.1192,
                    "high": 143.5275,
                    "low": 142.4619,
                    "close": 143.1092,
                    "volume": 19985714,
                    "unadjustedClose": 143.7,
                    "unadjustedVolume": 19985714,
                    "change": 0.039835,
                    "changePercent": 0.028,
                    "vwap": 143.0507,
                    "label": "Apr 03, 17",
                    "changeOverTime": -0.0039
                } // , { ... }
            ]
        [+] // .../dynamic
            {
                "range": "1m",
                "data": [
                    {
                        "date": "2017-04-03",
                        "open": 143.1192,
                        "high": 143.5275,
                        "low": 142.4619,
                        "close": 143.1092,
                        "volume": 19985714,
                        "unadjustedClose": 143.7,
                        "unadjustedVolume": 19985714,
                        "change": 0.039835,
                        "changePercent": 0.028,
                        "vwap": 143.0507,
                        "label": "Apr 03, 17",
                        "changeOverTime": -0.0039
                    } // , { ... }
                ]
            }
            [+] Available for all periods
                [-] date:
                    - returns market date as string
                    - Almost all of the date format is in yyyy-mm-dd format
                    - except:
                        '1d', date: e.g.: '20181101', and 'dynamic' is in
                        yyyymmdd format
                [-] label:
                    - label refers to the time in 12 hour format e.g.: 10:40 AM
                    - return time or date value as string
                    - for period '1d', date: '20181101', 'dynamic'
                      labels also refers to the date in month dd, yy format
                      e.g.: Nov 25, 18
                    - for period '5y', '2y', '1y', 'ytd', '6m', '3m', '1m'
                      labels only return date format
                      The nearer the date is to the present date,
                      the year will not be displayed
                [-] high:
                    high refers to the highest price, returns float number
                [-] low:
                    low refers to the lowest price, returns float number
                [-] volume:
                    - volume refers to the number of shares traded during a
                        given time period
                    - returns integer number
                [-] open:
                    - open refers to the first price when the stock market
                        opens
                    - returns float number
                [-] close:
                    - close refers to the last price when the stock market
                      closed
                    - returns float number
                [-] changeOverTime:
                    - returns float number
                    - % change of each interval relative to 1st value
                    - Useful for comparing multiple stocks
            [+] Available for period '1d' and date: e.g.: '20181101'
                [-] minute:
                    - minute refers to the time in 24 hour format e.g.: 15:40
                    - returns transaction time as string
                [-] average:
                    average refers to the average price, returns float number
                [-] notional:
                    - refers to the total value of the assets in a leveraged
                      position
                    - contract size * current spot price per unit
                    - equal to the amount used to calculate the payment
                    - returns float number
                [-] numberOfTrades:
                    returns integer number
                [-] marketHigh:
                    returns float number, has 15 minute delay
                [-] marketLow:
                    returns float number, has 15 minute delay
                [-] marketAverage:
                    returns float number, has 15 minute delay
                [-] marketVolume:
                    returns integer number, has 15 minute delay
                [-] marketNotional:
                    returns float number, has 15 minute delay
                [-] marketNumberOfTrades:
                    returns integer number, has 15 minute delay
                [-] marketOpen:
                    returns float number, has 15 minute delay
                [-] marketClose:
                    returns float number, has 15 minute delay
                [-] marketChangeOverTime:
                    - returns float number, has 15 minute delay
                    - % change of each interval relative to 1st value
            [+] Not available for period '1d' and date: e.g.: '20181101'
                [-] unadjustedVolume:
                    unadjusted means raw data, returns integer number
                [-] change:
                    - change is volatility
                    - it refers to the change between stock prices
                    - returns float number
                [-] changePercent:
                    - display the same result as change but in %
                    - returns float number
                [-] vwap:
                    - vwap = volume-weighted average price
                    - vwap = sum(number of shares bought * share price) /
                      total shares bought
                    - returns float number
        """
        self.invalid_args()
        chart = f"/stock/{self.symbols}/chart"
        period_range = ["5y", "2y", "1y", "ytd",
                        "6m", "3m", "1m", "1d"]
        if period is None:
            url = self.prefix + chart + ""
        else:
            if parameter is None:
                if period in period_range:
                    url = self.prefix + chart + "/" + period
                elif period == "dynamic":
                    url = self.prefix + chart + "/" + period
                    range_value = json.loads(self.get_data(url))["range"]
                    data_value = json.loads(self.get_data(url))["data"]
                    return (range_value, data_value)
                else:
                    url = self.prefix + chart + "/date/" + period
            else:
                # TODO implement paramenter feature
                # url = self.prefix + chart + "/" + period + "/" + parameter
                pass
        return json.loads(self.get_data(url))

    def get_collections(self):
        """
        GET /stock/market/collection/{collectionType}
        """
        pass

    def get_company(self):
        """
        Returns an array of quote objects for a given collection type.
        Currently supported collection types are sector, tag, and list
        GET /stock/{symbol}/company
        {
          "symbol": "AAPL",
          "companyName": "Apple Inc.",
          "exchange": "Nasdaq Global Select",
          "industry": "Computer Hardware",
          "website": "http://www.apple.com",
          "description": "Apple Inc is an American multinational technology
                          company. It designs, manufactures, and markets
                          mobile communication and media devices, personal
                          computers, and portable digital music players.",
          "CEO": "Timothy D. Cook",
          "issueType": "cs",
          "sector": "Technology",
          "tags": [
              "Technology",
              "Consumer Electronics",
              "Computer Hardware"
          ]
        }
        """
        self.invalid_args()
        company = f"/stock/{self.symbols}/company"
        url = self.prefix + company
        return json.loads(self.get_data(url))

    def get_crypto(self):
        """
        This will return an array of quotes for all Cryptocurrencies supported
        by the IEX API. Each element is a standard quote object with four
        additional keys.
        GET /stock/market/crypto
        [
          quote,
          ...
        ]
        Response: quote, bidPrice, bidSize, askPrice, askSize
        """
        crypto = "/stock/market/crypto"
        url = self.prefix + crypto
        return json.loads(self.get_data(url))

    def get_delayedQuote(self):
        """
        This returns the 15 minute delayed market quote.
        GET /stock/{symbol}/delayed-quote
        {
          "symbol": "AAPL",
          "delayedPrice": 143.08,
          "delayedSize": 200,
          "delayedPriceTime": 1498762739791,
          "processedTime": 1498763640156
        }
        """
        self.invalid_args()
        delayedQuote = f"/stock/{self.symbols}/delayed-quote"
        url = self.prefix + delayedQuote
        return json.loads(self.get_data(url))

    def get_dividends(self, period=None):
        """
        period:
            5y: 5 years, 2y: 2 years, 1y: 1 year, ytd: year to date,
            6m: 6 months, 3m: 3 months, 1m: 1 month(default)
        GET /stock/{symbol}/dividends/{range}
        [
            {
                "exDate": "2017-08-10",
                "paymentDate": "2017-08-17",
                "recordDate": "2017-08-14",
                "declaredDate": "2017-08-01",
                "amount": 0.63,
                "flag": "",
                "type": "Dividend income",
                "qualified": "Q"
                "indicated": ""
            } // , { ... }
        ]
        exDate: refers to the dividend ex-date
        paymentDate: refers to the payment date
        recordDate: refers to the dividend record date
        declaredDate: refers to the dividend declaration date
        amount: refers to the payment amount
        flag: refers to the dividend flag (
            FI = Final dividend, div ends or instrument ends,
            LI = Liquidation, instrument liquidates,
            PR = Proceeds of a sale of rights or shares,
            RE = Redemption of rights,
            AC = Accrued dividend,
            AR = Payment in arrears,
            AD = Additional payment,
            EX = Extra payment,
            SP = Special dividend,
            YE = Year end,
            UR = Unknown rate,
            SU = Regular dividend is suspended)
        type: refers to the dividend payment type (Dividend income,
            Interest income, Stock dividend, Short term capital gain,
            Medium term capital gain, Long term capital gain,
            Unspecified term capital gain)
        qualified: refers to the dividend income type
            P = Partially qualified income
            Q = Qualified income
            N = Unqualified income
            null = N/A or unknown
        indicated: refers to the indicated rate of the dividend
        """
        self.invalid_args()
        dividends = f"/stock/{self.symbols}/dividends"
        if period is None:
            url = self.prefix + dividends
        else:
            url = self.prefix + dividends + "/" + period
        return json.loads(self.get_data(url))

    def get_earnings(self):
        """
        Pulls data from the four most recent reported quarters.
        GET /stock/{symbol}/earnings
        {
          "symbol": "AAPL",
          "earnings": [
            {
              "actualEPS": 2.1,
              "consensusEPS": 2.02,
              "estimatedEPS": 2.02,
              "announceTime": "AMC",
              "numberOfEstimates": 14,
              "EPSSurpriseDollar": 0.08,
              "EPSReportDate": "2017-05-02",
              "fiscalPeriod": "Q2 2017",
              "fiscalEndDate": "2017-03-31",
              "yearAgo": 1.67,
              "yearAgoChangePercent": .30,
              "estimatedChangePercent": .28,
              "symbolId": 11
            },
            {
              "actualEPS": 3.36,
              "consensusEPS": 3.22,
              "estimatedEPS": 3.22,
              "announceTime": "AMC",
              "numberOfEstimates": 15,
              "EPSSurpriseDollar": 0.14,
              "EPSReportDate": "2017-01-31",
              "fiscalPeriod": "Q1 2017",
              "fiscalEndDate": "2016-12-31",
              "yearAgo": 1.67,
              "yearAgoChangePercent": .30,
              "estimatedChangePercent": .28,
              "symbolId": 11
            },
          ]
        }
        actualEPS: Actual earnings per share for the period
        consensusEPS: Consensus EPS estimate trend for the period
        estimatedEPS: Earnings per share estimate for the period
        announceTime: Time of earnings announcement. BTO (Before open),
                      DMT (During trading), AMC (After close)
        numberOfEstimates: Number of estimates for the period
        EPSSurpriseDollar: Dollar amount of EPS surprise for the period
        EPSReportDate: Expected earnings report date YYYY-MM-DD
        fiscalPeriod: The fiscal quarter the earnings data applies to Q# YYYY
        fiscalEndDate: Date representing the company fiscal quarter end
                       YYYY-MM-DD
        yearAgo: Represents the EPS of the quarter a year ago
        yearAgoChangePercent: Represents the percent difference between the
                              quarter a year ago actualEPS and current period
                              actualEPS.
        estimatedChangePercent: Represents the percent difference between the
                                quarter a year ago actualEPS and current period
                                estimatedEPS.
        symbolId: Represents the IEX id for the stock
        """
        self.invalid_args()
        earnings = f"/stock/{self.symbols}/earnings"
        url = self.prefix + earnings
        return json.loads(self.get_data(url))["earnings"]

    def get_earningsToday(self):
        """
        Returns earnings that will be reported today as two arrays: before the
        open bto and after market close amc. Each array contains an object with
        all keys from earnings, a quote object, and a headline key.
        GET /stock/market/today-earnings
        {
          "bto": [
            {
              "actualEPS": 2.1,
              "consensusEPS": 2.02,
              "estimatedEPS": 2.02,
              "announceTime": "BTO",
              "numberOfEstimates": 14,
              "EPSSurpriseDollar": 0.08,
              "EPSReportDate": "2017-05-02",
              "fiscalPeriod": "Q2 2017",
              "fiscalEndDate": "2017-03-31",
              "yearAgo": 1.67,
              "yearAgoChangePercent": .30,
              "estimatedChangePercent": .28,
              "symbolId": 11,
              "symbol": "AAPL",
              "quote": {
                  ...
              },
              "headline": ""
            },
            ...
          ],
          "amc": [
            {
              "actualEPS": 3.36,
              "consensusEPS": 3.22,
              "estimatedEPS": 3.22,
              "announceTime": "AMC",
              "numberOfEstimates": 15,
              "EPSSurpriseDollar": 0.14,
              "EPSReportDate": "2017-05-02",
              "fiscalPeriod": "Q2 2017",
              "fiscalEndDate": "2017-03-31",
              "yearAgo": 1.67,
              "yearAgoChangePercent": .30,
              "estimatedChangePercent": .28,
              "symbolId": 1,
              "symbol": "A",
              "quote": {
                  ...
              },
              "headline": ""
            },
            ...
          ]
        }
        """
        earningsToday = "/stock/market/today-earnings"
        url = self.prefix + earningsToday
        return json.loads(self.get_data(url))

    def get_effectiveSpread(self):
        """
        [+] This returns an array of effective spread, eligible volume, and
            price improvement of a stock, by market. Unlike volume-by-venue,
            this will only return a venue if effective spread is not ‘N/A’.
            Values are sorted in descending order by effectiveSpread.
            Lower effectiveSpread and higher priceImprovement values are
            generally considered optimal.
        [+] Effective spread is designed to measure marketable orders executed
            in relation to the market center’s quoted spread and takes into
            account hidden and midpoint liquidity available at each market
            center. Effective Spread is calculated by using eligible trade
            prices recorded to the consolidated tape and comparing those trade
            prices to the National Best Bid and Offer (“NBBO”) at the time of
            the execution.
        GET /stock/{symbol}/effective-spread
        [
          {
            "volume": 4899,
            "venue": "XCHI",
            "venueName": "CHX",
            "effectiveSpread": 0.02253725,
            "effectiveQuoted": 0.9539362,
            "priceImprovement": 0.0008471116999999999
          },
          {
            "volume": 9806133,
            "venue": "XBOS",
            "venueName": "NASDAQ BX",
            "effectiveSpread": 0.0127343,
            "effectiveQuoted": 0.9313967,
            "priceImprovement": 0.0007373158
          },
          {
            "volume": 6102991,
            "venue": "IEXG",
            "venueName": "IEX",
            "effectiveSpread": 0.005881705,
            "effectiveQuoted": 0.4532043,
            "priceImprovement": 0.003949427
          }
        ]
        """
        self.invalid_args()
        effectiveSpread = f"/stock/{self.symbols}/effective-spread"
        url = self.prefix + effectiveSpread
        return json.loads(self.get_data(url))

    def get_financials(self, period=None):
        """
        period: 'annual', 'quarter'(default)
        [+] Pulls income statement, balance sheet, and cash flow data from the
            four most recent reported quarters.
        GET /stock/{symbol}/financials
        {
          "symbol": "AAPL",
          "financials": [
            {
              "reportDate": "2017-03-31",
              "grossProfit": 20591000000,
              "costOfRevenue": 32305000000,
              "operatingRevenue": 52896000000,
              "totalRevenue": 52896000000,
              "operatingIncome": 14097000000,
              "netIncome": 11029000000,
              "researchAndDevelopment": 2776000000,
              "operatingExpense": 6494000000,
              "currentAssets": 101990000000,
              "totalAssets": 334532000000,
              "totalLiabilities": 200450000000,
              "currentCash": 15157000000,
              "currentDebt": 13991000000,
              "totalCash": 67101000000,
              "totalDebt": 98522000000,
              "shareholderEquity": 134082000000,
              "cashChange": -1214000000,
              "cashFlow": 12523000000,
              "operatingGainsLosses": null
            } // , { ... }
          ]
        }
        """
        self.invalid_args()
        financials = f"/stock/{self.symbols}/financials"
        if period == "quarter" or period == "annual":
            url = self.prefix + financials + "?period=" + period
        else:
            url = self.prefix + financials
        return json.loads(self.get_data(url))["financials"]

    def get_upcomingIpos(self):
        """
        [+] Returns a list of upcoming IPOs scheduled for the current and next
            month. The response is split into two structures: rawData and
            viewData. rawData represents all available data for an IPO.
            viewData represents data structured for display to a user.
        GET /stock/market/upcoming-ipos
        {
            "rawData": [
                {
                    "symbol": "VCNX",
                    "companyName": "VACCINEX, INC.",
                    "expectedDate": "2018-08-09",
                    "leadUnderwriters": [
                        "BTIG, LLC",
                        "Oppenheimer & Co. Inc."
                    ],
                    "underwriters": [
                        "Ladenburg Thalmann & Co. Inc."
                    ],
                    "companyCounsel": [
                        "Hogan Lovells US LLP and Harter Secrest & Emery LLP"
                    ],
                    "underwriterCounsel": [
                        "Mintz, Levin, Cohn, Ferris, Glovsky and Popeo, P.C."
                    ],
                    "auditor": "Computershare Trust Company, N.A",
                    "market": "NASDAQ Global",
                    "cik": "0001205922",
                    "address": "1895 MOUNT HOPE AVE",
                    "city": "ROCHESTER",
                    "state": "NY",
                    "zip": "14620",
                    "phone": "585-271-2700",
                    "ceo": "Maurice Zauderer",
                    "employees": 44,
                    "url": "www.vaccinex.com",
                    "status": "Filed",
                    "sharesOffered": 3333000,
                    "priceLow": 12,
                    "priceHigh": 15,
                    "offerAmount": null,
                    "totalExpenses": 2400000,
                    "sharesOverAlloted": 499950,
                    "shareholderShares": null,
                    "sharesOutstanding": 11474715,
                    "lockupPeriodExpiration": "",
                    "quietPeriodExpiration": "",
                    "revenue": 206000,
                    "netIncome": -7862000,
                    "totalAssets": 4946000,
                    "totalLiabilities": 6544000,
                    "stockholderEquity": -133279000,
                    "companyDescription": "",
                    "businessDescription": "",
                    "useOfProceeds": "",
                    "competition": "",
                    "amount": 44995500,
                    "percentOffered": "29.05"
                },
                ...
            ],
            "viewData": [
                {
                    "Company": "VACCINEX, INC.",
                    "Symbol": "VCNX",
                    "Price": "$12.00 - 15.00",
                    "Shares": "3,333,000",
                    "Amount": "44,995,500",
                    "Float": "11,474,715",
                    "Percent": "29.05%",
                    "Market": "NASDAQ Global",
                    "Expected": "2018-08-09"
                },
                ...
            ]
        }
        """
        upcomingIpos = "/stock/market/upcoming-ipos"
        url = self.prefix + upcomingIpos
        return json.loads(self.get_data(url))

    def get_todayIpos(self):
        """
        [+] Returns a list of today IPOs scheduled. The response is split into
            two structures: rawData and viewData. rawData represents all
            available data for an IPO. viewData represents data structured for
            display to a user.
        GET /stock/market/today-ipos
        {"rawData":[],"viewData":[],"lastUpdate":"2018-11-06"}
        """
        todayIpos = "/stock/market/today-ipos"
        url = self.prefix + todayIpos
        return json.loads(self.get_data(url))

    def get_thresholdSecurities(self):
        """
        [+] The following are IEX-listed securities that have an aggregate fail
            to deliver position for five consecutive settlement days at a
            registered clearing agency, totaling 10,000 shares or more and
            equal to at least 0.5% of the issuer’s total shares outstanding
            (i.e., “threshold securities”). The report data will be published
            to the IEX website daily at 8:30 p.m. ET with data for that trading
            day.
        """
        pass

    def get_shortInterest(self):
        """
        [+] The consolidated market short interest positions in all IEX-listed
            securities are included in the IEX Short Interest Report.
            The report data will be published daily at 4:00pm ET.
        """
        pass

    def get_stats(self):
        """
        GET /stock/{symbol}/stats
        {
          "companyName": "Apple Inc.",
          "marketcap": 760334287200,
          "beta": 1.295227,
          "week52high": 156.65,
          "week52low": 93.63,
          "week52change": 58.801903,
          "shortInterest": 55544287,
          "shortDate": "2017-06-15",
          "dividendRate": 2.52,
          "dividendYield": 1.7280395,
          "exDividendDate": "2017-05-11 00:00:00.0",
          "latestEPS": 8.29,
          "latestEPSDate": "2016-09-30",
          "sharesOutstanding": 5213840000,
          "float": 5203997571,
          "returnOnEquity": 0.08772939519857577,
          "consensusEPS": 3.22,
          "numberOfEstimates": 15,
          "symbol": "AAPL",
          "EBITDA": 73828000000,
          "revenue": 220457000000,
          "grossProfit": 84686000000,
          "cash": 256464000000,
          "debt": 358038000000,
          "ttmEPS": 8.55,
          "revenuePerShare": 42.2830389885382,
          "revenuePerEmployee": 1900491.3793103448,
          "peRatioHigh": 25.5,
          "peRatioLow": 8.7,
          "EPSSurpriseDollar": null,
          "EPSSurprisePercent": 3.9604,
          "returnOnAssets": 14.15,
          "returnOnCapital": null,
          "profitMargin": 20.73,
          "priceToSales": 3.6668503,
          "priceToBook": 6.19,
          "day200MovingAvg": 140.60541,
          "day50MovingAvg": 156.49678,
          "institutionPercent": 32.1,
          "insiderPercent": null,
          "shortRatio": 1.6915414,
          "year5ChangePercent": 0.5902546932200027,
          "year2ChangePercent": 0.3777449874142869,
          "year1ChangePercent": 0.39751716851558366,
          "ytdChangePercent": 0.36659492036160124,
          "month6ChangePercent": 0.12208398133748043,
          "month3ChangePercent": 0.08466584665846649,
          "month1ChangePercent": 0.009668596145283263,
          "day5ChangePercent": -0.005762605699968781
        }
        marketcap: is not calculated in real time.
        latestEPS: (Most recent quarter)
        returnOnEquity: (Trailing twelve months)
        consensusEPS: (Most recent quarter)
        numberOfEstimates: (Most recent quarter)
        EBITDA: (Trailing twelve months)
        revenue: (Trailing twelve months)
        grossProfit: (Trailing twelve months)
        cash: reers to total cash. (Trailing twelve months)
        debt: refers to total debt. (Trailing twelve months)
        ttmEPS: (Trailing twelve months)
        revenuePerShare: (Trailing twelve months)
        revenuePerEmployee: (Trailing twelve months)
        EPSSurpriseDollar: refers to the difference between actual EPS and
                           consensus EPS in dollars.
        EPSSurprisePercent: refers to the percent difference between actual
                            EPS and consensus EPS.
        returnOnAssets: (Trailing twelve months)
        returnOnCapital: (Trailing twelve months)
        institutionPercent: represents top 15 institutions
        """
        self.invalid_args()
        stats = f"/stock/{self.symbols}/stats"
        url = self.prefix + stats
        return json.loads(self.get_data(url))

    def get_largestTrades(self):
        """
        This returns 15 minute delayed, last sale eligible trades.
        GET /stock/{symbol}/largest-trades
        [
          {
            "price": 186.39,
            "size": 10000,
            "time": 1527090690175,
            "timeLabel": "11:51:30",
            "venue": "EDGX",
            "venueName": "Cboe EDGX"
          },
          ...
        ]
        price: refers to the price of the trade.
        size: refers to the number of shares of the trade.
        time: refers to the time of the trade.
        timeLabel: formatted time string as HH:MM:SS
        venue: refers to the venue where the trade occurred.
               None refers to a TRF (off exchange) trade.
        venueName: formatted venue name where the trade occurred.
        """
        self.invalid_args()
        largestTrades = f"/stock/{self.symbols}/largest-trades"
        url = self.prefix + largestTrades
        return json.loads(self.get_data(url))

    def get_topTen(self, parameter):
        """
        topTen refers to List in IEX API
        Returns an array of quotes for the top 10 symbols in a specified list.
        parameter:
            mostactive, gainers, losers, iexvolume, iexpercent, infocus
        gainers, losers, infocus has the same keys
        # TODO mostactive, iexvolume, iexpercent yet to be tested
        GET /stock/market/list/gainers
        [
            {
                "symbol": "FNSR",
                "companyName": "Finisar Corporation",
                "primaryExchange": "Nasdaq Global Select",
                "sector": "Technology",
                "calculationPrice": "close",
                "open": 22.16,
                "openTime": 1541773800070,
                "close": 21.79,
                "closeTime": 1541797200744,
                "high": 22.71,
                "low": 21.27,
                "latestPrice": 21.79,
                "latestSource": "Close",
                "latestTime": "November 9, 2018",
                "latestUpdate": 1541797200744,
                "latestVolume": 23718511,
                "iexRealtimePrice": null,
                "iexRealtimeSize": null,
                "iexLastUpdated": null,
                "delayedPrice": 21.79,
                "delayedPriceTime": 1541797200744,
                "extendedPrice": 21.8,
                "extendedChange": 0.01,
                "extendedChangePercent": 0.00046,
                "extendedPriceTime": 1541800694870,
                "previousClose": 18.88,
                "change": 2.91,
                "changePercent": 0.15413,
                "iexMarketPercent": null,
                "iexVolume": null,
                "avgTotalVolume": 2561102,
                "iexBidPrice": null,
                "iexBidSize": null,
                "iexAskPrice": null,
                "iexAskSize": null,
                "marketCap": 2554036079,
                "peRatio": 26.25,
                "week52High": 25.41,
                "week52Low": 14.251,
                "ytdChange": 0.1824452430391693
            } // , { ... }
        ]
        """
        topTen = "/stock/market/list/"
        url = self.prefix + topTen + parameter
        return json.loads(self.get_data(url))

    def get_logo(self):
        """
        GET /stock/{symbol}/logo
        {
          "url": "https://storage.googleapis.com/iex/api/logos/AAPL.png"
        }
        returns the logo's url as a string
        """
        self.invalid_args()
        logo = f"/stock/{self.symbols}/logo"
        url = self.prefix + logo
        return json.loads(self.get_data(url))["url"]

    def get_batchNews(self, latest=None):
        """
        latest = Number between 1 and 50. Default is 10.
        Returns up to 50 latest market wide news
        GET /stock/market/news/last/{last}
        [
          {
            "datetime": "2017-06-29T13:14:22-04:00",
            "headline": "Voice Search Technology Creates A New Paradigm For
                         Marketers",
            "source": "Benzinga via QuoteMedia",
            "url": "https://api.iextrading.com/1.0/stock/aapl/article/
                    8348646549980454",
            "summary": "<p>Voice search is likely to grow by leap and bounds,
                        with technological advancements leading to better
                        adoption and fueling the growth cycle, according to
                        Lindsay Boyajian, <a href=\"http://loupventures.com/
                        how-the-future-of-voice-search-affects-marketers-today/
                        \">a guest contributor at Loup Ventu...",
            "related": "AAPL,AMZN,GOOG,GOOGL,MSFT",
            "image": "https://api.iextrading.com/1.0/stock/aapl/news-image/
                      7594023985414148"
          }
        ]
        """
        batchNews = "/stock/market/news"
        if latest is None:
            url = self.prefix + batchNews
        else:
            url = self.prefix + batchNews + "/last/" + str(latest)
        return json.loads(self.get_data(url))

    def get_news(self, latest=None):
        """
        latest = Number between 1 and 50. Default is 10.
        Returns up to 50 latest news
        GET /stock/{symbol}/news/last/{last}
        [
          {
            "datetime": "2017-06-29T13:14:22-04:00",
            "headline": "Voice Search Technology Creates A New Paradigm For
                         Marketers",
            "source": "Benzinga via QuoteMedia",
            "url": "https://api.iextrading.com/1.0/stock/aapl/article/
                    8348646549980454",
            "summary": "<p>Voice search is likely to grow by leap and bounds,
                        with technological advancements leading to better
                        adoption and fueling the growth cycle, according to
                        Lindsay Boyajian, <a href=\"http://loupventures.com/
                        how-the-future-of-voice-search-affects-marketers-today/
                        \">a guest contributor at Loup Ventu...",
            "related": "AAPL,AMZN,GOOG,GOOGL,MSFT",
            "image": "https://api.iextrading.com/1.0/stock/aapl/news-image/
                      7594023985414148"
          }
        ]
        """
        self.invalid_args()
        news = f"/stock/{self.symbols}/news"
        if latest is None:
            url = self.prefix + news
        else:
            url = self.prefix + news + "/last/" + str(latest)
        return json.loads(self.get_data(url))

    def get_batchOHLC(self):
        """
        Returns the official open and close for a given symbol.
        GET /stock/market/ohlc
        {
          "open": {
            "price": 154,
            "time": 1506605400394
          },
          "close": {
            "price": 153.28,
            "time": 1506605400394
          },
          "high": 154.80,
          "low": 153.25
        }
        """
        batchOHLC = "/stock/market/ohlc"
        url = self.prefix + batchOHLC
        return json.loads(self.get_data(url))

    def get_OHLC(self):
        """
        Returns the official open and close for a give symbol.
        GET /stock/{symbol}/ohlc
        {
          "open": {
            "price": 154,
            "time": 1506605400394
          },
          "close": {
            "price": 153.28,
            "time": 1506605400394
          },
          "high": 154.80,
          "low": 153.25
        }
        """
        self.invalid_args()
        OHLC = f"/stock/{self.symbols}/ohlc"
        url = self.prefix + OHLC
        return json.loads(self.get_data(url))

    def get_rivals(self):
        """
        rivals = peers in IEX API
        Return a list of rival companies
        GET /stock/{symbol}/peers
        [
            "MSFT",
            "NOK",
            "IBM",
            "BBRY",
            "HPQ",
            "GOOGL",
            "XLK"
        ]
        """
        self.invalid_args()
        rivals = f"/stock/{self.symbols}/peers"
        url = self.prefix + rivals
        return json.loads(self.get_data(url))

    def get_batchPrevious(self):
        """
        [+] This returns previous day adjusted price data for a single stock,
            or an object keyed by symbol of price data for the whole market.
        GET /stock/market/previous
        {
          "symbol": "AAPL",
          "date": "2017-09-19",
          "open": 159.51,
          "high": 159.77,
          "low": 158.44,
          "close": 158.73,
          "volume": 20810632,
          "unadjustedVolume": 20810632,
          "change": 0.06,
          "changePercent": 0.038,
          "vwap": 158.9944
        }
        """
        batchPrevious = "/stock/market/previous"
        url = self.prefix + batchPrevious
        return json.loads(self.get_data(url))

    def get_previous(self):
        """
        [+] This returns previous day adjusted price data for a single stock,
            or an object keyed by symbol of price data for the whole market.
        GET /stock/{symbol}/previous
        {
          "symbol": "AAPL",
          "date": "2017-09-19",
          "open": 159.51,
          "high": 159.77,
          "low": 158.44,
          "close": 158.73,
          "volume": 20810632,
          "unadjustedVolume": 20810632,
          "change": 0.06,
          "changePercent": 0.038,
          "vwap": 158.9944
        }
        """
        self.invalid_args()
        previous = f"/stock/{self.symbols}/previous"
        url = self.prefix + previous
        return json.loads(self.get_data(url))

    def get_price(self):
        """
        [+] Return the current stock price of a stock as a float number,
            NOT JSON!
        [+] A single number, being the IEX real time price, the 15 minute
            delayedmarket price, or the previous close price, is returned.
        GET /stock/{symbol}/price
        143.28
        """
        self.invalid_args()
        price = f"/stock/{self.symbols}/price"
        url = self.prefix + price
        return float(self.get_data(url))

    def get_quote(self, percentage=False):
        """
        displayPercent: If set to true, all percentage values will be
                        multiplied by a factor of 100
        GET /stock/{symbol}/quote
        {
          "symbol": "AAPL",
          "companyName": "Apple Inc.",
          "primaryExchange": "Nasdaq Global Select",
          "sector": "Technology",
          "calculationPrice": "tops",
          "open": 154,
          "openTime": 1506605400394,
          "close": 153.28,
          "closeTime": 1506605400394,
          "high": 154.80,
          "low": 153.25,
          "latestPrice": 158.73,
          "latestSource": "Previous close",
          "latestTime": "September 19, 2017",
          "latestUpdate": 1505779200000,
          "latestVolume": 20567140,
          "iexRealtimePrice": 158.71,
          "iexRealtimeSize": 100,
          "iexLastUpdated": 1505851198059,
          "delayedPrice": 158.71,
          "delayedPriceTime": 1505854782437,
          "extendedPrice": 159.21,
          "extendedChange": -1.68,
          "extendedChangePercent": -0.0125,
          "extendedPriceTime": 1527082200361,
          "previousClose": 158.73,
          "change": -1.67,
          "changePercent": -0.01158,
          "iexMarketPercent": 0.00948,
          "iexVolume": 82451,
          "avgTotalVolume": 29623234,
          "iexBidPrice": 153.01,
          "iexBidSize": 100,
          "iexAskPrice": 158.66,
          "iexAskSize": 100,
          "marketCap": 751627174400,
          "peRatio": 16.86,
          "week52High": 159.65,
          "week52Low": 93.63,
          "ytdChange": 0.3665,
        }
        symbol: refers to the stock ticker.
        companyName: refers to the company name.
        primaryExchange: refers to the primary listings exchange.
        sector: refers to the sector of the stock.
        calculationPrice: refers to the source of the latest price.
                          ("tops", "sip", "previousclose" or "close")
        open: refers to the official open price
        openTime: refers to the official listing exchange time for the open
        close: refers to the official close price
        closeTime: refers to the official listing exchange time for the close
        high: refers to the market-wide highest price from the SIP. 15 minute
              delayed
        low: refers to the market-wide lowest price from the SIP. 15 minute
             delayed
        latestPrice: refers to the latest price being the IEX real time price,
                     the 15 minute delayed market price, or the previous close
                     price.
        latestSource: refers to the source of latestPrice.
                      ("IEX real time price", "15 minute delayed price",
                      "Close" or "Previous close")
        latestTime: refers to a human readable time of the latestPrice.
                    The format will vary based on latestSource.
        latestUpdate: refers to the update time of latestPrice in milliseconds
                      since midnight Jan 1, 1970.
        latestVolume: refers to the total market volume of the stock.
        iexRealtimePrice: refers to last sale price of the stock on IEX.
                          (Refer to the attribution section above.)
        iexRealtimeSize: refers to last sale size of the stock on IEX.
        iexLastUpdated: refers to the last update time of the data in
                        milliseconds since midnight Jan 1, 1970 UTC or -1 or 0.
                        If the value is -1 or 0, IEX has not quoted the symbol
                        in the trading day.
        delayedPrice: refers to the 15 minute delayed market price during
                      normal market hours 9:30 - 16:00.
        delayedPriceTime: refers to the time of the delayed market price during
                          normal market hours 9:30 - 16:00.
        extendedPrice: refers to the 15 minute delayed market price outside
                       normal market hours 8:00 - 9:30 and 16:00 - 17:00.
        extendedChange: is calculated using extendedPrice from
                        calculationPrice.
        extendedChangePercent: is calculated using extendedPrice from
                               calculationPrice.
        extendedPriceTime: refers to the time of the delayed market price
                           outside normal market hours 8:00 - 9:30 and
                           16:00 - 17:00.
        change: is calculated using calculationPrice from previousClose.
        changePercent: is calculated using calculationPrice from previousClose.
        iexMarketPercent: refers to IEX’s percentage of the market in the
                          stock.
        iexVolume: refers to shares traded in the stock on IEX.
        avgTotalVolume: refers to the 30 day average volume on all markets.
        iexBidPrice: refers to the best bid price on IEX.
        iexBidSize: refers to amount of shares on the bid on IEX.
        iexAskPrice: refers to the best ask price on IEX.
        iexAskSize: refers to amount of shares on the ask on IEX.
        marketCap: is calculated in real time using calculationPrice.
        peRatio: is calculated in real time using calculationPrice.
        week52High: refers to the adjusted 52 week high.
        week52Low: refers to the adjusted 52 week low.
        ytdChange: refers to the price change percentage from start of year to
                   previous close.
        """
        self.invalid_args()
        quote = f"/stock/{self.symbols}/quote"
        if percentage is False:
            url = self.prefix + quote
        else:
            url = self.prefix + quote + "?displayPercent=true"
        return json.loads(self.get_data(url))

    def get_relevant(self):
        """
        [+] Similar to the peers endpoint, except this will return most active
            market symbols when peers are not available. If the symbols
            returned are not peers, the peers key will be false.
        GET /stock/{symbol}/relevant
        {
          "peers": true,
          "symbols": [
              "MSFT",
              "NOK",
              "IBM",
              "BBRY",
              "HPQ",
              "GOOGL",
              "XLK"
          ]
        }
        """
        self.invalid_args()
        relevant = f"/stock/{self.symbols}/relevant"
        url = self.prefix + relevant
        return json.loads(self.get_data(url))

    def get_sectorP(self):
        """
        sectorP = sector performance
        [+] This returns an array of each sector and performance for the
            current trading day. Performance is based on each sector ETF.
        GET /stock/market/sector-performance
        [
          {
            "type": "sector",
            "name": "Industrials",
            "performance": 0.00711,
            "lastUpdated": 1533672000437
          },
          ...
        ]
        """
        sectorP = "/stock/market/sector-performance"
        url = self.prefix + sectorP
        return json.loads(self.get_data(url))

    def get_splits(self, period=None):
        """
        period:
            5y: 5 years, 2y: 2 years, 1y: 1 year, ytd: year to date,
            6m = 6 months, 3m: 3 months, 1m: 1 month(default)
        GET /stock/{symbol}/splits/{range}
        [
            {
                "exDate": "2017-08-10",
                "declaredDate": "2017-08-01",
                "recordDate": "2017-08-14",
                "paymentDate": "2017-08-17",
                "ratio": 0.142857,
                "toFactor": 7,
                "forFactor": 1
            } // , { ... }
        ]
        """
        self.invalid_args()
        splits = f"/stock/{self.symbols}/splits"
        if period is None:
            url = self.prefix + splits
        else:
            url = self.prefix + splits + "/" + period
        return json.loads(self.get_data(url))

    def get_timeSeries(self):
        """
        An alternate way to access the chart endpoint.
        GET /stock/{symbol}/time-series
        [
            {
                "date": "2018-09-24",
                "open": 216.82,
                "high": 221.26,
                "low": 216.63,
                "close": 220.79,
                "volume": 27693358,
                "unadjustedVolume": 27693358,
                "change": 3.13,
                "changePercent": 1.438,
                "vwap": 219.4487,
                "label": "Sep 24",
                "changeOverTime": 0
            },
            ...
        ]
        """
        self.invalid_args()
        timeSeries = f"/stock/aapl/time-series"
        url = self.prefix + timeSeries
        return json.loads(self.get_data(url))

    def get_volByVenue(self):
        """
        volByVenue = Volume by Venue
        [+] Returns 15 minute delayed and 30 day average consolidated volume
            percentage of a stock, by market. This call will always return 13
            values, and will be sorted in ascending order by current day
            trading volume percentage.
        GET /stock/{symbol}/volume-by-venue
        [
          {
            "volume": 0,
            "venue": "XNYS",
            "venueName": "NYSE",
            "marketPercent": 0,
            "avgMarketPercent": 0,
            "date": "N/A"
          },
          ...
        ]
        volume: refers to the current day, 15 minute delayed volume
        venue: refers to the Market Identifier Code (MIC)
        venueName: refers to a readable version of the venue defined by IEX
        date: refers to the date the data was last updated in the
              format YYYY-MM-DD
        marketPercent: refers to the 15 minute delayed percent of total stock
                       volume traded by the venue
        avgMarketPercent: refers to the 30 day average percent of total stock
                          volume traded by the venue
        """
        self.invalid_args()
        volByVenue = f"/stock/{self.symbols}/volume-by-venue"
        url = self.prefix + volByVenue
        return json.loads(self.get_data(url))


if __name__ == "__main__":
    a = IEX()
    test = a.get_topTen("infocus")
    # test = a.get_charts("dynamic")[1]
    # test2 = a.get_topTen("gainers", True)[0]
    # df = a.view_table(test[])
    # print single column
    # print(df.loc[:, ["change"]])

    # print(type(test))
    # clean json data for easy reading
    print(json.dumps(test, indent=4))
    # print(json.dumps(test2, indent=4))
