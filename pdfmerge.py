from sys import argv, exit
from pathlib import Path

import PyPDF2
from PyPDF2 import PdfWriter


# merges files in the order provided in the list
# precondition - every file should be valid
def merge(pdf_list, output_name, destination):
    # check if there are a valid amount of arguments (aka more than 1)
    if len(pdf_list) < 2:
        print("Invalid argument(s): Need at least two files to merge")
        return None
    merger = PyPDF2.PdfMerger
    for path in pdf_list:
        with open(path, 'rb') as fileobj:
            merger.append(fileobj)
    new_path = destination / output_name
    with open(new_path, 'wb') as output_file:
        merger.write(output_file)


# get all the pdf names from a specific folder and sub-folders
def extract_pdfs_from_folder(path_name):
    pdfs = []
    path = Path(path_name)
    if not path.exists():
        print("Invalid argument(s): Path does not exist")
        return pdfs
    for file in path.iterdir():
        # recursively search through every sub-folder
        # if file.is_dir():
        #    pdfs += extract_pdfs_from_folder(file.name)
        if file.suffix.lower() == '.pdf':
            pdfs.append(str(file.resolve()))
    return pdfs


# gets the pdf file names, returns list of pdf file names
def get_files():
    # determine if command line is being used to pass in arguments
    pdf_list = []
    arguments = len(argv)
    if arguments > 1:
        for i in range(1, arguments):
            argument = argv[i]
            # need to check if the file exists
            path = Path(argument)
            if not path.exists():
                print("Invalid argument(s): {} does not exist.".format(argument))
                return pdf_list
            # also need to check if the file is a pdf
            path_type = path.suffix.lower()
            if path_type == ".pdf":
                pdf_list += argv[i]
            elif path.is_dir():
                pdf_list += extract_pdfs_from_folder(argv[i])
            else:
                print("Invalid argument(s): {} is not a .pdf file or a folder w/ pdfs.".format(argument))
                return pdf_list
    # prompt the user to pick a folder with all the pdfs to merge
    else:
        name = input("Enter the path to the folder with the pdfs: ")
        pdf_list = extract_pdfs_from_folder(name)
    return pdf_list


if __name__ == '__main__':
    files = get_files()
    if len(files) == 0:
        exit(-1)
    name = input("Enter the name for the output: ")
    path_name = input("Enter destination: ")
    path = Path(path_name)
    if not path.exists():
        print("Invalid argument(s): {} does not exist.".format(path_name))
        exit(-1)
    merge(files, name, path)
