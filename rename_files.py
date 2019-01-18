import argparse
import os


def get_arguments():
    """
    -o must have argument data (must also have -n or -d)
    -n must have argument data (must also have -o)
    -d does not require argument to delete character (must also have -o)
    -ap add new prefix character to filename by itself
    -as add new suffix character to filename by itself
    -p change and set path (optional)
    e.g.: python rename.py -o old_char -n new_char -p /usr/local
    If replace space character, use a single \ followed by a space character
    e.g.: python rename.py -o \  -n new_char
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", dest="old_character",
                        help="old character(s) of file/folder names to remove")
    parser.add_argument("-n", "--new", dest="new_character",
                        help="new character(s) of file/folder names to add")
    # Need to set action="store_true" to work without arguments
    parser.add_argument("-d", "--del", dest="delete", action="store_true",
                        help="delete old character(s) from file/folder names")
    parser.add_argument("-ap", "--add_prefix", dest="prefix",
                        help="add new prefix character to file/folder names")
    parser.add_argument("-as", "--add_suffix", dest="suffix",
                        help="add new suffix character to file/folder names")
    parser.add_argument("-p", "--path", dest="path",
                        help="set path for app to rename files/folders")
    _args = parser.parse_args()
    return _args


class Rename:

    def __init__(self):
        self.args = get_arguments()
        if self.args.path:
            os.chdir(f"{self.args.path}")
        self.file_list = os.listdir()

    def rename(self):
        for file in self.file_list:
            if self.args.delete:
                new_filename = file.replace(self.args.old_character, "")
            elif self.args.prefix:
                new_filename = self.args.prefix + file
            elif self.args.suffix:
                new_filename = file + self.args.suffix
            elif self.args.old_character and self.args.new_character:
                new_filename = file.replace(self.args.old_character,
                                            self.args.new_character)
            os.rename(file, new_filename)


def main():
    run = Rename()
    run.rename()
    print("Renaming of file/folder names completed!")


if __name__ == "__main__":
    main()
