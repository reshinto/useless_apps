import platform


class Linux:
    def __init__(self):
        self.name = "Linux"

    def run(self):
        return f"{self.name} version is running"


class Mac:
    def __init__(self):
        self.name = "Mac"

    def run(self):
        return f"{self.name} version is running"


class Windows:
    def __init__(self):
        self.name = "Windows"

    def run(self):
        return f"{self.name} version is running"


class Adapter:
    def __init__(self):
        self._check_os = platform.system()
        self._run_os = None
        self._check_system()

    def _check_system(self):
        if self._check_os == "Linux":
            self._run_os = Linux()
        elif self._check_os == "Darwin":
            self._run_os = Mac()
        elif self._check_os == "Windows":
            self._run_os = Windows()
        else:
            print("Unknown OS")

    def show(self):
        print(self._run_os.run())


a = Adapter()
a.show()
