import os
from itertools import tee, islice
import csv
import numpy
from pip._vendor.colorama import Fore

from AscData import AscData


def print_banner(message, border="*"):
    """
    Prints the 'message' within the border.
    param message: A meaningful message.
    param border: Contents of the border.
    """
    line = border * len(message)
    print(Fore.GREEN + "\n" + Fore.GREEN + line)
    print(message)
    print(line + "\n" + Fore.RESET)


def get_list_of_asc_input_files():
    """
    Prompts for user input of a file location.
    Returns for an array containing the file locations and a dictionary for the data file name with its location for
    given user input of a file location.
    return: list of all files location.
    """
    all_files = []
    print(Fore.RED + "Hit 'Enter' to quit." + Fore.RESET)

    path = input(Fore.YELLOW + "Input the folder locations if any ::: " + Fore.RESET)
    if path:
        for r, d, f in os.walk(path):  # r=root, d=directory F=file
            for file in f:
                if ".asc" in file:
                    all_files.append(os.path.join(r, file))
    return all_files


def extract_filename_from_filepath(filepath):
    """
    Returns the filename from the file path.
    :arg filepath file path
    :return filename from the filepath passed.
    """
    if "\\" in filepath:
        return filepath.split("\\")[-1]
    elif "/" in filepath:
        return filepath.split("/")[-1]