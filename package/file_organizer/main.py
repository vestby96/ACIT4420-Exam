import os
import re
import logging
from package.file_organizer.file_sorter import FileSorter
from package.file_organizer.logger import log_function_call
from package.file_organizer.errors import InvalidDirectoryNameError, DirectoryNotFoundError, PermissionDeniedError

@log_function_call
def main():
    current_dir = "./package/tests/file_organizer"
    directories = [item for item in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, item))]
    
    print("\nAvailable directories:")
    print("\n".join(directories))

    dir_name_pattern = r"^[a-zA-Z0-9_\-]+$"

    while True:
        base_dir = input("Enter the directory to organize: ").strip()

        if not re.match(dir_name_pattern, base_dir):
            logging.error(f"Invalid directory name: {base_dir}")
            print("Error: Directory name contains invalid characters. Only alphanumeric characters, dashes, and underscores are allowed.")
            continue

        chosen_dir = os.path.join(current_dir, base_dir)

        if not os.path.exists(chosen_dir):
            logging.error(f"Directory does not exist: {base_dir}")
            print(f"Error: The directory '{base_dir}' does not exist. Please try again.")
            continue

        if not os.access(chosen_dir, os.W_OK):
            logging.error(f"Permission denied for directory: {base_dir}")
            print(f"Error: Permission denied to write in '{base_dir}'.")
            return  # Exit the program for permission errors.

        # Break out of the loop when the directory is valid
        print("Directory found and permissions are OK: Continuing")
        break    

    sorter = FileSorter(chosen_dir)
    sorter.organize_files()

    return "OK"

if __name__ == "__main__":
    try:
        main()
    except InvalidDirectoryNameError as e:
        logging.error(e)
        print(f"Error: {e}")
    except DirectoryNotFoundError as e:
        logging.error(e)
        print(f"Error: {e}")
    except PermissionDeniedError as e:
        logging.error(e)
        print(f"Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")

