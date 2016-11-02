"""
CP1404/CP5632 Practical
Week 10
File renaming and os examples
CleanupFilesV2
"""
import os
import shutil

__author__ = 'Gareth Mullins'


def main():
    do_not_touch = [".DS_store"]
    ORIGINAL_DIRECTORY = os.getcwd()
    print("Currently working directory: ", os.getcwd())

    # Menu to operate this program
    menu_input = input("D\t(D)own a folder\n"
                       "C\t(Ch)ange the current directory\n"
                       "R\t(R)eturn to the original directory ({})\n"
                       "F\t(F)ormat a folder of files\n"
                       "S\t(Ca)tegorize a folder of files into folders named by the user\n"
                       "Q\t(Q)uit".format(ORIGINAL_DIRECTORY)).upper()

    while menu_input[0].upper() != "Q":
        if menu_input[0].upper() == "D":
            # Change the working directory to a subdirectory
            try:
                os.chdir(os.getcwd() + "//" + input("\nPlease enter the sub directory name or folder name"))
            except OSError:
                print("An error occurred while accessing the folder entered")

        elif menu_input[0].upper() + menu_input[1].lower() == "Ch":
            # Change the currently working directory to a directory of th euser's choosing
            try:
                os.chdir(input("\nPlease enter the new directory in it's entirety"))
            except OSError:
                print("An error occurred while accessing the directory entered")

        elif menu_input == "R":
            # Revert the currently working directory to the original working directory
            os.chdir(ORIGINAL_DIRECTORY)

        elif menu_input == "F":
            # Format each file (and those inside a subdirectory) inside of the subdirectory specified by the user
            current_directory = os.getcwd()
            to_format = input("\nPlease enter the name of the folder that contains the files to be formatted, "
                              "if it's the current folder, enter nothing")
            if to_format == "":
                to_format = os.getcwd()
            else:
                to_format = os.getcwd() + "\\" + to_format
            dirs = directory_walk(to_format)
            # check if there are any sub-directories
            if len(dirs) >= 1:
                walk_subdirectories(dirs, do_not_touch)
            os.chdir(current_directory)

        elif menu_input[0].upper() + menu_input[1].lower() == "Ca":
            # Categorize each file inside of the subdirectory specified by the user
            current_directory = os.getcwd()
            to_categorize = input("\nPlease enter the name of the folder that contains the files to be categorized, "
                                  "if it's the current folder, enter nothing")
            if to_categorize == "":
                to_categorize = os.getcwd()
            else:
                to_categorize = os.getcwd() + "\\" + to_categorize
            categorize_files(to_categorize)
            os.chdir(current_directory)

        else:
            print("\nAn invalid letter was entered")

        # Reopen the menu
        print("\nCurrently working directory: ", os.getcwd())
        menu_input = input("D\t(D)own a folder\n"
                           "C\t(Ch)ange the current directory\n"
                           "R\t(R)eturn to the original directory ({})\n"
                           "F\t(F)ormat a folder of files\n"
                           "S\t(Ca)tegorize a folder of files into folders named by the user\n"
                           "Q\t(Q)uit".format(ORIGINAL_DIRECTORY)).upper()[0]


def fix_filename(filename):
    """
    Fixes up a filename so that it's usable and readable
    :param filename: The name of the file
    :return: new_filename; The reformatted filename
    """
    first_letter = True
    new_filename = ""
    for i in range(len(filename)):
        if first_letter is False and filename[i].isupper() and filename[i - 1] != "(" and filename[i - 1] != " ":
            if filename[i - 1] != "_":
                new_filename += " " + filename[i]
            else:
                new_filename += filename[i]
        else:
            new_filename += filename[i]
        first_letter = False
    new_filename = str.title(new_filename).replace(" ", "_")
    return new_filename


def directory_walk(do_not_touch, new_directory=os.getcwd()):
    """
    Walks through the directory finding files that aren't in "do_not_touch" before calling reformat_filename() to
     reformat them one at a time
    :param do_not_touch: A list of files that are not to be touched
    :param new_directory: The directory that's to be worked in
    :return: dirs; A list of the subdirectories
    """
    os.chdir(new_directory)
    for root, dirs, files in os.walk('.'):
        for name in do_not_touch:
            if name in files:
                files.remove(name)
        print("\nIn", new_directory)
        print("\tcontains subdirectories:", dirs)
        print("\tand files:", files, "\n")
        reformat_filename(files)
        return dirs


def walk_subdirectories(subdir_list, do_not_touch):
    """
    Walks through the subdirectories listed in subdir_list finding files that aren't in do_not_touch before calling them
     to be reformatted
    :param subdir_list: list of the subdirectories to go through
    :param do_not_touch: A list of files that are not to be touched
    :return: None
    """
    for subdirectory in subdir_list:
        os.chdir(os.getcwd() + "\\" + subdirectory)
        for root, dirs, files in os.walk('.'):
            confirmation = ""
            for name in do_not_touch:
                if name in files:
                    files.remove(name)

            print("In", os.getcwd())
            print("\tcontains subdirectories:", dirs)
            print("\tand files:", files)
            while confirmation != "Y" and confirmation != "N":
                confirmation = input("Would you like these files to be formated as well? (Y/N) ").upper()[0]
                if confirmation == "Y":
                    reformat_filename(files)
                elif confirmation != "N":
                    print("An invalid letter was entered")
            os.chdir("..")
    return None


def reformat_filename(file_list):
    """
    Reformat the names in "file_list"
    :param file_list: List of the files to be reformatted
    :return: None
    """
    for filename in file_list:
        print(filename)
        # ignore directories, just process the files
        if not os.path.isdir(filename):
            new_filename = fix_filename(filename)
            new_filename = new_filename.replace(".Txt", ".txt").replace("._T_X_T", ".txt")
            print(new_filename)
            # rename the file from filename to new_filename
            os.rename(filename, new_filename)
    return None


# All three sections put together as one
"""
def categorize_files(directory):
    \"""
    Categorize the files into folders named by the user
    :param directory: The directory that the folders are located
    :return: None
    \"""
    extensions = []
    categorised_something = False
    os.chdir(directory)
    for root, dirs, files in os.walk("."):
        for file in files:
            extension = os.path.splitext(file)[1].replace(".", "")
            if extension not in extensions:
                extensions.append(extension)
                categorised_something = True
        for extension in extensions:
            title = input("What category would you like to sort {} files into?".format(extension))

            destination_dir_name = os.getcwd() + "\\" + title
            # make a new directory
            try:
                os.mkdir(destination_dir_name)
            except OSError:
                pass

        files = os.listdir(".")
        for file in files:
            if os.path.splitext(file)[1].replace(".", "") == extension:
                # move file to the destination directory
                shutil.move(file, destination_dir_name + "\\" + file)
                print("Files with the extension {} have been moved.".format(extension))
        if categorised_something:
            print("\nFiles are categorized")
        else:
            print("Nothing to categorize")
        return None
"""


def categorize_files(directory):
    """
    Categorize the files into folders named by the user
    :param directory: The directory that the folders are located
    :return: None
    """
    extensions = []
    categorised_something = False
    os.chdir(directory)
    for root, dirs, files in os.walk("."):
        for file in files:
            extension = os.path.splitext(file)[1].replace(".", "")
            if extension not in extensions:
                extensions.append(extension)
                categorised_something = True
        for extension in extensions:
            title = input("What category would you like to sort {} files into?".format(extension))
            destination_dir_name = create_directory(title)
            move_files_by_extension(destination_dir_name, extension)
        if categorised_something:
            print("\nFiles are categorized")
        else:
            print("Nothing to categorize")
        return None


def create_directory(title):
    """
    Create a subdirectory with the by name title
    :param title: The folder name
    :return: destination_dir_name; the location of the created subdirectoy
    """
    destination_dir_name = os.getcwd() + "\\" + title
    # make a new directory
    try:
        os.mkdir(destination_dir_name)
    except OSError:
        pass
    return destination_dir_name


def move_files_by_extension(destination_dir_name, extension):
    """
    Move files from the current working directory to the destination_dir_name
    :param destination_dir_name: The directory that the files are to be moved to
    :param extension: The extension that determines the files to be moved
    :return: None
    """
    files = os.listdir(".")
    for file in files:
        if os.path.splitext(file)[1].replace(".", "") == extension:
            # move file to the destination directory
            shutil.move(file, destination_dir_name + "\\" + file)
    print("Files with the extension {} have been moved.".format(extension))
    return None


if __name__ == '__main__':
    main()
