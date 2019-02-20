import subprocess


text_to_speech = "text.txt"
try:
    # open text file
    with open(text_to_speech, "r") as rf:
        # read text & split at new line
        textList = rf.read().split("\n")
        textList.pop()
        for text in textList:
            # parse text and save audio file as aiff format
            subprocess.call(["say", text, "-o", f"{text}.aiff"])
            # convert audio file to mp3 format
            subprocess.call(["lame","-m","m", f"{text}.aiff", f"{text}.mp3"])
            subprocess.call(["rm", f"{text}.aiff"])
except FileNotFoundError as msg:
    print(msg)

print("All texts have been converted to mp3")
