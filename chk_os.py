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
