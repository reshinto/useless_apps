import platform
import subprocess


class Adapter:
    def __init__(self):
        self._check_os = platform.system()
        self.os_dict = {
            "Darwin": self.osx,
            "Windows": self.windows10,
            "Linux": self.linux
        }

    def run_app(self):
        if self.os_dict.get(self._check_os) is None:
            return "OS not supported"
        self.os_dict[self._check_os]()

    def osx(Self):
        print("OSX")

    def windows10(self):
        print("windows 10")

    def linux(self):
        linux_type = subprocess.check_output(["lsb_release", "-is"]).decode("utf-8")[:-1]
        linux_dict = {
            "Ubuntu": self.ubuntu,
            "Kali": self.kali
        }
        if linux_dict.get(linux_type) is None:
            return "Linux OS not supported"
        linux_dict[linux_type]()

    def ubuntu(self):
        print("ubuntu")

    def kali(self):
        print("kali")


a = Adapter()
a.run_app()
