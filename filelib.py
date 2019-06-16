import os.path
import re


class FileSystem:

    defaultFilePath = None
    filePath = None

    def setPath(self):
        """
        Set full path. When keying path,
        including new folder is not a requisite.
        """
        self.filePath = input("Please provide full path, "
                              "including new folder and filename to create.\n"
                              "e.g.: /path/newFolder/newFile.txt\n> ")

    def getContents(self, _filePath):
        """
        Check if file exists and if file is empty.
        If both are True, return the contents of the file as a list
        """
        if self.haveFile(_filePath) and not self.isEmpty(_filePath):
            # open and read file
            with open(_filePath, 'r') as readFile:
                fileContents = readFile.read().split("\n")
            fileContents.pop()
            # Exclude last empty line in text file before return string
            return fileContents

    def createFile(self, _filePath=None, displayMsg=False):
        """
        Check if file exist. If it does not, create new file.
        Display message feature added to provide visualization.
        """
        if _filePath is None:
            if self.defaultFilePath is None:
                self.setPath()
            else:
                self.filePath = self.defaultFilePath
        else:
            self.filePath = _filePath
        # Ensures file does not exist to prevent erasing by mistake
        if not os.path.isfile(self.filePath):
            try:
                # Although filename is included, only new directory be created
                os.makedirs(os.path.dirname(self.filePath), exist_ok=True)
                # Creates a new file
                with open(self.filePath, 'w'):
                    pass
                if displayMsg is not False:
                    print(f"A new file has been created at:\n{self.filePath}")
            except FileExistsError as msg:
                print(msg)

    @classmethod
    def useDefaultPath(cls, fileType):
        """
        This will override the predetermined defaultFilePath value.
        Choose file type to set default path and filename.
        Available file types: 1) authen 2) spam
        Add more if needed or just use the createFile method directly.
        """
        cls.defaultFilePath = cls.backOneFolder(cls.getScriptPath())
        settings = {
            "authen": "/settings/authentication.txt",
            "spam": "/settings/spam_list.txt"
        }
        if settings.get(fileType) is None:
            raise ValueError(f"File type: '{fileType}' not available! "
                             "Please use other file types or create one.")
        else:
            cls.defaultFilePath += settings[fileType]

    @staticmethod
    def haveFile(_filePath):
        """Return True if file exists."""
        return os.path.isfile(_filePath)

    @staticmethod
    def isEmpty(_filePath):
        """Return True if file is empty."""
        return os.stat(_filePath).st_size == 0

    @staticmethod
    def getHomePath():
        """
        Get default home path.
        / is not included at the end of the last folder name in path.
        """
        return os.path.expanduser('~')

    @staticmethod
    def getScriptPath():
        """
        Find and return script path that is currently running.
        / is not included at the end of the last folder name in path.
        When concatenating with other strings, remeber to put a /!
        """
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def getCurrentPath():
        """
        Get full path of current working directory
        / is not included at the end of the last folder name in path.
        """
        return os.getcwd()

    @staticmethod
    def backOneFolder(oldPath):
        """
        Go back by one folder, then return full path
        last / character is excluded to make paths of all folders & files
        consistent.
        """
        # Using raw string, so \ not required
        resultList = re.findall(r".+?/", oldPath)
        # Exclude last / character to standardize directories & files in path
        return "".join(resultList)[:-1]

    @staticmethod
    def editFile(_filePath, text):
        if FileSystem.haveFile(_filePath):
            with open(_filePath, "a") as af:
                af.write(text + "\n")
