import os
import sys


class Reindent:
    def __init__(self, filename):
        self.filename = filename
        self.contents = self.getContents()

    def isExist(self):
        return os.path.isfile(self.filename)

    def getContents(self):
        if self.isExist():
            with open(self.filename, "r") as f:
                return f.read().split("\n")
        print(self.filename, "does not exist!")

    def reindent(self):
        length = len(self.contents)
        with open(self.filename, "w") as f:
            while(length > 0):
                length -= 1
                string = self.contents.pop(0)
                count = 0
                j = 0
                if string == "":
                    f.write(string) if length == 1 else f.write(string + "\n")
                    continue
                while(True):
                    if string[j] == " ":
                        count += 1
                        j += 1
                    else:
                        break
                if count == 0:
                    f.write(string) if length == 1 else f.write(string + "\n")
                    continue
                string = string.replace(
                    " " * count,
                    " " * int(count / int(sys.argv[2]) * int(sys.argv[3])))
                f.write(string) if length == 1 else f.write(string + "\n")
        print("Reindentation completed!")


def invalid(msg=None):
    if msg is None:
        msg = "Invalid command!"
    print(f"{msg}\nUse the help argument to display the help menu")
    print("python main.py help")


def help():
    print("python main.py {path/to/filename} {old number of indent}"
          " {new number of indent}")


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "help":
            help()
        elif len(sys.argv) < 4:
            invalid()
        elif len(sys.argv) == 4:
            filename = sys.argv[1]
            run = Reindent(filename)
            if run.isExist() is True:
                run.reindent()
        else:
            invalid()
    except IndexError as msg:
        invalid(msg)
