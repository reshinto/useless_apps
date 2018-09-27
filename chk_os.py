import platform


class Adapter:
    def __init__(self, run_app):
        self._check_os = platform.system()
        self._run_os = None
        self._check_system(run_app)

    def _check_system(self, run_app):
        if self._check_os == "Linux":
            self._run_os = run_app
        elif self._check_os == "Darwin":
            self._run_os = run_app
        elif self._check_os == "Windows":
            self._run_os = run_app
        else:
            print("Unknown OS")

    def run(self):
        return self._run_os


a = Adapter()
a.run()
