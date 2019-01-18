#!/usr/bin/env python3
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
    # if not _args.old_character:
    #     parser.error("[-] Please specify an old character command,"
    #                  "use --help for more info")
    # if not _args.new_character:
    #     parser.error("[-] Please specify a new character command,"
    #                  "use --help for more info")
    return _args


def add_prefix(file_list, prefix):
    for file in file_list:
        new_filename = prefix + file
        os.rename(file, new_filename)


def add_suffix(file_list, suffix):
    for file in file_list:
        new_filename = file + suffix
        os.rename(file, new_filename)


def add_character(file_list, old_character, new_character):
    for file in file_list:
        new_filename = file.replace(old_character, new_character)
        os.rename(file, new_filename)


def delete_character(file_list, old_character):
    for file in file_list:
        new_filename = file.replace(old_character, "")
        os.rename(file, new_filename)


def rename(args):
    # save_path = os.getcwd()
    if args.path:
        os.chdir(f"{args.path}")
    file_list = os.listdir()
    if args.delete:
        delete_character(file_list, args.old_character)
    elif args.prefix:
        add_prefix(file_list, args.prefix)
    elif args.suffix:
        add_suffix(file_list, args.suffix)
    else:
        add_character(file_list, args.old_character, args.new_character)


def main():
    args = get_arguments()
    rename(args)
    print(f"old character(s): {args.old_character} has been replaced with",
          f"new character(s): {args.new_character}")
    print("Renaming of file/folder names completed!")


if __name__ == "__main__":
    main()
