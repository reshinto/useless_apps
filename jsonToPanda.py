"""
Converts JSON to table for readability with pandas api
__version__ = 0.4
"""
from iex import IEX
import pandas as pd
from pandas.io.json import json_normalize


class DataReader:
    """
    [+] Converts JSON file from IEX API into a table with pandas dataframe api
    [+] Usage examples are given in each methods
    {+} Not all methods from IEX API are implemented here, because its not
        required
    [+] Methods like get_price() and get_rivals() are not implemented here
        because output is either an integer or a list, which is not a JSON
        object
    [+] NOT all methods support multiple arguments, refer to iex.py to find out
        which methods are supported
    """

    def __init__(self, *symbols):
        self.stock_api = IEX(*symbols)

    @staticmethod
    def table(data):
        """Convert JSON data to table format as DataFrame"""
        return pd.DataFrame(json_normalize(data))

    # pandas join method does not work with staticmethod as decorator
    # TODO find out why self is not required and why regular method works
    def joinCol(*dataFrame):
        """
        joinCol = join columns
        Join 2 or more dataframes into 1 by columns
        >>> a = DataFrame("aapl")
        >>> test = a.joinCol(a.chart_date("1d"), a.chart_open("1d"),
                             a.chart_close("1d"))
        """
        for i, df in enumerate(dataFrame):
            # 1st element does not contain a dataframe, therefore skip
            if i == 0:
                continue
            # join requires 2 dataframes, so save 1 and skip
            if i == 1:
                dataframes = df
                continue
            # join 2 dataframes, and increment by 1 df per additional loop
            dataframes = dataframes.join(df)
        return dataframes

    def book(self, response):
        """
        response:
            quote, bids, asks, systemEvent
        [+] quote:
            Display quote of 1 stock
            List of keys:
                symbol, companyName, primaryExchange, sector, calculationPrice,
                open, openTime, close, closeTime, high, low, latestPrice,
                latestSource, latestTime, latestUpdate, latestVolume,
                iexRealtimePrice, iexRealtimeSize, iexLastUpdated,
                delayedPrice, delayedPriceTime, extendedPrice, extendedChange,
                extendedChangePercent, extendedPriceTime, previousClose,
                change, changePercent, iexMarketPercent, iexVolume,
                avgTotalVolume, iexBidPrice, iexBidSizae, iexAskPrice,
                iexAskSize, marketCap, peRatio, week52High, week52Low,
                ytdChange
            e.g.:
            >>> a = DataReader('aapl')
            # get all columns of book
            >>> test = a.book_quote("quote")
            # get 1 column of book e.g.: 'symbol'
            >>> test["symbol"]
            # get multi columns of book
            >>> test[["symbol", "companyName"]]
        [+] bids: Currently not displaying anything
        [+] asks: Currently not displaying anything
        [+] systemEvent: Currently not displaying anything
        """
        responses = ["quote", "bids", "asks", "systemEvent"]
        if response in responses:
            return self.table(self.stock_api.get_book()[response])

    def _chart_chk_dynamic(self, period, parameter):
        """
        chart_chk_dynamic = check for 'dynamic' in charts
        [+] Check if period input is 'dynamic'
        [+] If True, print the dynamic range, which is either 1d or 1m
            and then return the data
        """
        if period == "dynamic":
            # TODO display current period range in dashboard
            period_range = self.stock_api.get_charts(period, parameter)[0]
            print(f"Period is {period_range}")
            return self.table(self.stock_api.get_charts(period, parameter)[1])
        else:
            return self.table(self.stock_api.get_charts(period, parameter))

    def _chart_chk_1d(self, period, parameter):
        """
        chart_chk_1d = check chart within the 1 day period
        Check if period input is '1d' or date: e.g.: '20111101'
        Make sure date inputs have len of 8 and are all numerical digits
        None value will be given is condition are not met
        """
        if period == "1d" or len(period) == 8 and period.isdigit() is True:
            return self.table(self.stock_api.get_charts(period, parameter))

    def _chart_chk_not1d(self, period, parameter):
        """
        chart_chk_not1d = check chart that are not in the 1 day period
        [+] This method although similar, is separated from the _chart_chk_1d
            method period support dependencies issues when using the chk
            methods with other chart methods
        [+] Check if period input is NOT '1d' or date: e.g.: '20111101'
        """
        period_range = ["5y", "2y", "1y", "ytd", "6m", "3m", "1m", "dynamic"]
        if period in period_range:
            return self._chart_chk_dynamic(period, parameter)

    # TODO yet to implement parameter feature
    def chart(self, response, period=None, parameter=None):
        """
        response:
            [+] Available for all periods
                - date, label, high, low, volume, open, close, changeOverTime
            [+] Available for period '1d' and date: e.g.: '20181101'
                - minute, average, notional, numberOfTrades, marketHigh,
                  marketLow, marketAverage, marketVolume, marketNotional,
                  marketNumberOfTrades, marketOpen, marketClose,
                  marketChangeOverTime
            [+] Not available for period '1d' and date: e.g.: '20181101'
                - unadjustedVolume, change, changePercent, vwap
        period:
            "5y", "2y", "1y", "ytd", "6m", "3m", "1m", "1d", date: "20181101",
            "dynamic"
        parameters:
            chartReset, chartSimplify, chartInterval, changeFromClose,
            chartLast
        Refer to iex.py for more details
        e.g.:
        >>> a = DataReader("aapl")
        # get date from chart
        >>> a.chart("date")
        """
        all_list = ["date", "label", "high", "low", "volume", "open", "close",
                    "changeOverTime"]
        one_day_list = ["minute", "average", "notional", "numberOfTrades",
                        "marketHigh", "marketLow", "marketAverage",
                        "marketVolume", "marketNotional",
                        "marketNumberOfTrades", "marketOpen", "marketClose",
                        "marketChangeOverTime"]
        not_one_day_list = ["unadjustedVolume", "change", "changePercent",
                            "vwap"]
        if response in not_one_day_list:
            df = self._chart_chk_not1d(period, parameter)
        elif response in one_day_list:
            df = self._chart_chk_1d(period, parameter)
        elif response in all_list:
            df = self._chart_chk_dynamic(period, parameter)
        if df is not None:
            return df.loc[:, [response]]

    def dividends(self, period=None):
        """
        Get dividends data of a company by periods
        periods:
            '5y', '2y', '1y', 'ytd', '6m', '3m', '1m'(default)
        List of keys:
            exDate, paymentDate, recordDate, declaredDate, amount, flag, type,
            qualified, indicated
        Refer to iex.py for more details on keys
        e.g.:
        # get all columns
        >>> a = DataReader("aapl")
        >>> test = a.dividends("5y")
        >>> test
        # get 1 column
        >>> test["amount"]
        # get multi columns
        >>> test[["amount", paymentDate]]
        """
        if period is None:
            return self.table(self.stock_api.get_dividends(period))
        period_list = ["5y", "2y", "1y", "ytd", "6m", "3m", "1m"]
        if period in period_list:
            return self.table(self.stock_api.get_dividends(period))
        else:
            raise ValueError("Only period range of '5y', '2y', '1y', 'ytd',"
                             "'6m', '3m', '1m' are supported")

    def financials(self, period=None):
        """
        Get basic financial statements data of a company
        perid: 'quarter'(default), 'annual'
        List of keys:
            reportDate, grossProfit, costOfRevenue, operatingRevenue,
            totalRevenue, operatingIncome, netIncome, researchAndDevelopment,
            operatingExpense, currentAssets, totalAssets, totalLiabilities,
            currentCash, currentDebt, totalCash, totalDebt, shareholdEquity,
            cashChange, cashFlow, operatingGainsLosses
        e.g.:
        # get all columns
        >>> a = DataReader("aapl")
        >>> test = a.financials("annual)
        # get 1 column
        >>> test["grossProfit"]
        # get multi columns
        >>> test[["grossProfit", "netIncome"]]
        """
        return self.table(self.stock_api.get_financials(period))

    def topTen(self, parameter):
        """
        topTen = List in IEX API
        Get top ten companies data under the parameter category
        parameter:
            mostactive, gainers, losers, iexvolume, iexpercent, infocus
        List of keys:
            symbol, companyName, primaryExchange, sector, calculationPrice,
            open, openTime, close, closeTime, high, low, latestPrice,
            latestSource, latestTime, latestUpdate, latestVolume,
            iexRealtimePrice, iexRealtimeSize, iexLastUpdated, delayedPrice,
            delayedPriceTime, extendedPrice, extendedChange,
            extendedChangePercent, extendedPriceTime, previousClose, change,
            changePercent, iexMarketPercent, iexVolume, avgTotalVolume,
            iexBidPrice, iexBidSize, iexAskPrice, iexAskSize, marketcap,
            peRatio, week52High, week52Low, ytdChange
        e.g.:
        >>> a = DataReader()
        >>> test.topTen()
        # get all columns
        >>> test
        # get 1 column
        >>> test["symbol"]
        # get multi columns
        >>> test[["symbol", "ytdChange"]]
        """
        parameter_list = ["mostactive", "gainers", "losers", "iexvolume",
                          "iexpercent", "infocus"]
        if parameter in parameter_list:
            return self.table(self.stock_api.get_topTen(parameter))

    def news(self, latest=None):
        """
        Get news of a company
        latest must be a string
        latest: refers to the lastest 1 to 50 news
            10 is default
        List of keys:
            datetime, headline, source, url, summary, related, image
        Refer to iex.py for more details on keys
        e.g.:
        # get all columns
        >>> a = DataReader("aapl")
        >>> test = a.news("10")
        >>> test
        # get 1 column
        >>> test["datetime"]
        # get multi columns
        >>> test[["datetime", "headline"]]
        """
        if latest is not None:
            if len(latest) > 2 or latest.isdigit() is False:
                latest = None
        return self.table(self.stock_api.get_news(latest))

    def batchNews(self, latest=None):
        """
        Get market wide news
        latest must be a string
        latest: refers to the lastest 1 to 50 news
            10 is default
        List of keys:
            datetime, headline, source, url, summary, related, image
        Refer to iex.py for more details on keys
        e.g.:
        # get all columns
        >>> a = DataReader()
        >>> test = a.news("10")
        >>> test
        # get 1 column
        >>> test["datetime"]
        # get multi columns
        >>> test[["datetime", "headline"]]
        """
        if latest is not None:
            if len(latest) > 2 or latest.isdigit() is False:
                latest = None
        return self.table(self.stock_api.get_batchNews(latest))

    def quote(self, percentage=False):
        """
        Get quote data of a company
        percentage: True, False
        List of keys:
            symbol, companyName, primaryExchange, sector, calculationPrice,
            open, openTime, close, closeTime, high, low, latestPrice,
            latestSource, latestTime, latestUpdate, latestVolume,
            iexRealtimePrice, iexRealtimeSize, iexLastUpdated, delayedPrice,
            delayedPriceTime, extendedPrice, extendedChange,
            extendedChangePercent, extendedPriceTime, previousClose, change,
            changePercent, iexMarketPercent, iexVolume, avgTotalVolume,
            iexBidPrice, iexBidSizae, iexAskPrice, iexAskSize, marketCap,
            peRatio, week52High, week52Low, ytdChange
        Refer to iex.py for more details on keys
        e.g.:
        # get all columns
        >>> a = DataReader("aapl")
        >>> test = a.quote()
        >>> test
        # get 1 column
        >>> test["symbol"]
        # get multi columns
        >>> test[["symbol", "open"]]
        """
        if percentage is False or percentage is True:
            return self.table(self.stock_api.get_quote(percentage))

    def company(self):
        """
        Get company basic information
        list of keys:
            symbol, companyName, exchange, industry, website, description,
            CEO, issueType, sector, tags(returns a list of tags e.g.:
                Technology, Consumer Electronics, Computer Hardware)
        e.g.:
        # get all columns
        >>> a = DataReader("aapl")
        >>> test = a.company()
        >>> test
        # get 1 column
        >>> test["symbol"]
        # get multi columns
        >>> test[["symbol", "companyName"]]
        """
        return self.table(self.stock_api.get_company())

    def earnings(self):
        """
        Get 4 most recent reported quarter earnings data of a company
        List of keys:
            actualEPS, consensusEPS, estimatedEPS, announceTime,
            numberOfEstimates, EPSSurpriseDollar, EPSReportDate, fiscalPeriod,
            fiscalEndDate, yearAgo, yearAgoChangePercent,
            estimatedChangePercent
        Refer to iex.py for more details on keys
        e.g.:
        # get all columns
        >>> a = DataReader("aapl")
        >>> test = a.earnings()
        # get 1 column
        >>> test["actualEPS"]
        # get multi columns
        >>> test[["actualEPS", "fiscalPeriod"]]
        """
        return self.table(self.stock_api.get_earnings())

    def stats(self):
        """
        Get key financial stats data of a company
        List of keys:
            companyName, marketcap, beta, week52high, week52low, week52change,
            shortInterest, shortDate, dividenRate, dividendYield,
            exDividendDate, latestEPS, latestEPSDate, sharesOutstanding, float,
            returnOnEquity, consensusEPS, numberOfEstimates, symbol, EBITDA,
            revenue, grossProfit, cash, debt, ttmEPS, revenuePerShare,
            revenuePerEmployee, peRatioHigh, peRatioLow, EPSSurpriseDollar,
            EPSSurprisePercent, returnOnAssets, returnOnCapital, profitMargin,
            priceToSales, priceToBook, day200MovingAvg, day50MovingAvg,
            institutionPercent, shortRatio, year5ChangePercent,
            year2ChangePercent, year1ChangePercent, ytdChangePercent,
            month6ChangePercent, month3ChangePercent, month1ChangePercent,
            day5ChangePercent
        Refer to iex.py for more details on keys
        e.g.:
        # get all columns
        >>> a = DataReader("aapl")
        >>> test = a.stats()
        >>> test
        # get 1 column
        >>> test["marketcap"]
        # get multi columns
        >>> test[["marketcap", "cash"]]
        """
        return self.table(self.stock_api.get_stats())

    def largestTrades(self):
        """
        Get live 15 minute delayed, last sale eligible trades data
        List of keys:
            price, size, time, timeLabel, venue, venueName
        Refer to iex.py for more details on keys
        e.g.:
        >>> a = DataReader("aapl")
        >>> test = a.largestTrades()
        # get all columns
        >>> test
        # get 1 column
        >>> test["price"]
        # get multi columns
        >>> test[["price", "size"]]
        """
        return self.table(self.stock_api.get_largestTrades())

    def volByVenue(self):
        """
        Get 13 venue(stock exchanges) data
        List of keys:
            volume, venue, venueName, marketPercent, avgMarketPercent, date
        Refer to iex.py for more details on keys
        e.g.:
        # get all columns
        >>> a = DataReader()
        >>> test = a.volByVenue()
        >>> test
        # get 1 column
        >>> test["venue"]
        # get multi columns
        >>> test[["venue", "marketPercent"]]
        """
        return self.table(self.stock_api.get_volByVenue())


if __name__ == "__main__":
    a = DataReader("aapl", "goog")
    test = a.batchNews()
    # date_range = ["1d", "20181101", "dynamic"]
    # date_range = ["5y", "2y", "1y", "ytd", "6m",
    #               "3m", "1m", "1d", "20181101", "dynamic"]
    # for x in date_range:
    #     print(x)
    #     print(a.chart_vwap(x))
    # test = a.joinCol(a.chart_date("1d"), a.chart_open("1d"))
    print(test)
