#!/usr/bin/env python3
import argparse
import os


def get_arguments():
    """
    -o and -n arguments must be filled in when running app.
    -p is optional
    e.g.: python rename.py -o old_char -n new_char -p /usr/local
    If replace space character, use a single \ as space character
    e.g.: python rename.py -o \ -n new_char
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", dest="old_character",
                        help="old character(s) of file/folder names to remove")
    parser.add_argument("-n", "--new", dest="new_character",
                        help="new character(s) of file/folder names to add")
    parser.add_argument("-p", "--path", dest="path",
                        help="set path for app to rename files/folders")
    _args = parser.parse_args()
    if not _args.old_character:
        parser.error("[-] Please specify an old character command,"
                     "use --help for more info")
    elif not _args.new_character:
        parser.error("[-] Please specify a new character command,"
                     "use --help for more info")
    return _args


def rename(old, new, path=None):
    # save_path = os.getcwd()
    if path is not None:
        os.chdir(f"{path}")
    file_list = os.listdir()
    for file in file_list:
        new_filename = file.replace(old, new)
        os.rename(file, new_filename)


def main():
    args = get_arguments()
    rename(args.old_character, args.new_character, args.path)
    print(f"old character(s): {args.old_character} has been replaced with",
          f"new character(s): {args.new_character}")
    print("Renaming of file/folder names completed!")


if __name__ == "__main__":
    main()
