# Text to Speech converter
## Converts text written in a text.txt file into speech then outputs it to an mp3 file
* tested on MAC OS

### How it works
* Each line in the text.txt file is saved into a list of texts
* Each line is then converted to a .aiff file by using the say command in MAC
* lame is used to convert the .aiff file into a .mp3 file
* All .aiff files will be automatically deleted
* mp3 files will be saved in the app folder
* You may need to install lame if it is not installed on your computer with brew
    * brew install lame

### How to run
* Write all the texts you wanna convert to speech in the text.txt file
* Each line equals to 1 file
* run file
    * python run.py
