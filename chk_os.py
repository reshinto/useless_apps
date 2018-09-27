import platform


current_os = platform.system()

if current_os == "Darwin":
    print("Mac")
elif current_os == "Linux":
    print("Linux")
elif current_os == "Windows":
    print("Windows")
else:
    print("Unknown OS")


class Korean:
    def __init__(self):
        self.name = "Korean"

    def speak_korean(self):
        return "An-neyong?"


class British:
    def __init__(self):
        self.name = "British"

    def speak_english(self):
        return "Hello!"


class Adapter:
    def __init__(self, object, **adapted_method):
        self._object = object

        self.__dict__.update(adapted_method)

    def __getattr__(self, attr):
        return getattr(self._object, attr)


objects = []

korean = Korean()

british = British()

objects.append(Adapter(korean, speak=korean.speak_korean))
objects.append(Adapter(british, speak=british.speak_english))

for obj in objects:
    print(f"{obj.name} says '{obj.speak()}'\n")
