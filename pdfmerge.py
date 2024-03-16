from sys import argv
from pathlib import Path
from PyPDF2 import PdfWriter


# merges files in the order provided in the list
# precondition - every file should be valid
def merge(pdf_list):
    # check if there are a valid amount of arguments (aka more than 1)
    if len(pdf_list) < 2:
        print("Invalid argument(s): Need at least two files to merge")
        return None


# get all the pdf names from a specific folder and sub-folders
def extract_pdfs_from_folder(path_name):
    pdfs = []
    path = Path(path_name)
    if not path.exists():
        print("Invalid argument(s): Path does not exist")
        return None
    for file in path.iterdir():
        # recursively search through every sub-folder
        # if file.is_dir():
        #    pdfs += extract_pdfs_from_folder(file.name)
        if file.suffix.lower() == '.pdf':
            pdfs += file.name
    return pdfs


# gets the pdf file names, returns list of pdf file names
def get_files():
    # determine if command line is being used to pass in arguments
    files = []
    arguments = len(argv)
    if arguments > 1:
        for i in range(1, arguments):
            argument = argv[i]
            # need to check if the file exists
            path = Path(argument)
            if not path.exists():
                print("Invalid argument(s): {} does not exist.".format(argument))
            # also need to check if the file is a pdf
            path_type = path.suffix.lower()
            if path_type == ".pdf":
                files += argv[i]
            elif path.is_dir():
                files += extract_pdfs_from_folder(argv[i])
            else:
                print("Invalid argument(s): {} is not a .pdf file or a folder w/ pdfs.".format(argument))
    # just prompt the user to pick a folder with all the pdfs to merge
    else:
        name = input("Enter the path to the folder with the pdfs: ")
        files = extract_pdfs_from_folder(name)
    return files


if __name__ == '__main__':
    files = get_files()
