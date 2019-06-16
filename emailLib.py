import imaplib
import re


class EmailAccount:

    def __init__(self, username, password, domainName, spamList=None):
        """
        username = email address
        password = email password
        domainName = email type, e.g.: gmail, hotmail
        """
        self.username = username
        self.password = password
        self.spamList = spamList
        self.serverAddress = self.getServerAddress(domainName.lower())
        self.totalMsg = None

    @staticmethod
    def getServerAddress(domainName):
        """Return server address."""
        domainAddresses = {
            "gmail": "imap.gmail.com",
            "hotmail": "imap-mail.outlook.com"
        }
        if domainAddresses.get(domainName) is None:
            raise ValueError(f"{domainName} not implemented.")
        else:
            return domainAddresses[domainName]


class UseIMAP(EmailAccount):

    def __init__(self, username, password, domainName, spamList=None):
        super().__init__(username, password, domainName, spamList)
        self.server = self.getIMAPServer(self.serverAddress)
        self.loginServer = self.server.login(self.username, self.password)

    @staticmethod
    def getIMAPServer(domainAddress):
        """Get email server."""
        return imaplib.IMAP4_SSL(domainAddress)

    def selectFolder(self, mailbox):
        """
        Makes the app select a folder for the next action to take place.
        folderName depends on the email types.
        e.g.: for gmail inbox, folderName = inbox, gmail spam is [Gmail]/Spam
        """
        # double quotes need to included in a single quote to work
        mailbox = f'"{mailbox}"'
        self.server.select(mailbox)

    def getFolderList(self):
        """
        Get all of the mailbox folders in the email and return
        the gathered information as a list.
        All folder names will be returned with their original case to get
        keep original data.
        typ = type, should get 'OK' or 'NO'
        mailboxData is the response.
        Refer to https://svn.python.org/projects/python/trunk/Lib/imaplib.py
        for more information.
        """
        folderList = []
        typ, mailboxData = self.server.list()
        for mailbox in mailboxData:
            flags, delimiter, mailbox_name = self.getMailboxInfo(mailbox)
            folderList.append(mailbox_name)
        return folderList

    def getNumOfEmails(self, mailboxArg, status):
        """
        Get the number of emails, read or unread depending on the
        status type. Then return the number in string format.
        String format is returned as no arithmetics will be involved.
        """
        statusList = ["MESSAGES", "RECENT", "UIDNEXT", "UIDVALIDITY", "UNSEEN"]
        if status.upper() in statusList:
            # Convert all to lowercase for comparison
            if mailboxArg.lower() in [x.lower() for x in self.getFolderList()]:
                status = self.server.status(f'"{mailboxArg}"',
                                            f"({status})")
                searchStatus = status[1][0].decode()
                return re.findall(r"\d+", searchStatus)[0]

    @staticmethod
    def getMailboxInfo(mailbox):
        """Get the mailbox raw data"""
        pattern = re.compile(
            r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
        match = pattern.match(mailbox.decode())
        flags, delimiter, mailboxName = match.groups()
        mailboxName = mailboxName.strip('"')
        return (flags, delimiter, mailboxName)

    def getIDs(self, search):
        """
        Search 1 mailbox for match and return a list of matching IDs in string
        format.
        Folder has to be selected first before implementing.
        Use the self.selectFolder method.
        search must be = "ALL" or e.g.: "(FROM xxx@gmail.com)" or combined
        "(FROM "xxx@gmail.com" SUBJECT "Example message")"
        """
        # self.selectFolder(mailbox)
        typ, msgIDs = self.server.search(None, search)
        # return a list of msgIDs in string format
        return msgIDs[0].decode().split()

    def deleteMsg(self, getIDs, flags, trash):
        """
        Receive a list of IDs in string format.
        Then join all IDs in list to a single string.
        ids has to be a single string of IDs separated with a comma
        to work.
        hotmail: flags = "+FLAGS", trash = r"(\Deleted)"
        gmail: flags = "X-GM-LABELS", trash = "\\Trash"
        """
        try:
            ids = ",".join(getIDs)
            # Add deleted flag to email
            self.server.store(ids, flags, trash)
            # Delete all emails with deleted flag
            self.server.expunge()
        except imaplib.IMAP4.error:
            # Error is produced when mail is not found. Can ignore.
            pass

    def closeServer(self):
        """Only use this if a mailbox has been selected."""
        self.server.close()

    def logoffServer(self):
        self.server.logout()
