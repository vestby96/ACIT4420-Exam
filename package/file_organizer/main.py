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

        try:
            # Validate directory name
            if not re.match(dir_name_pattern, base_dir):
                raise InvalidDirectoryNameError(
                    "Directory name contains invalid characters. Only alphanumeric characters, dashes, and underscores are allowed"
                )

            chosen_dir = os.path.join(current_dir, base_dir)

            # Check if directory exists
            if not os.path.exists(chosen_dir):
                raise DirectoryNotFoundError(f"The directory '{base_dir}' does not exist")

            # Check for write permissions
            if not os.access(chosen_dir, os.W_OK):
                raise PermissionDeniedError(f"Permission denied to write in '{base_dir}'")

            # Break out of the loop when the directory is valid
            print("Directory found and permissions are OK: Continuing")
            break

        except InvalidDirectoryNameError as e:
            logging.error(e)
            print(f"Error: {e}. Please try again.")
        except DirectoryNotFoundError as e:
            logging.error(e)
            print(f"Error: {e}. Please try again.")
        except PermissionDeniedError as e:
            logging.error(e)
            print(f"Error: {e}. Please try again.")

    # Organize files
    sorter = FileSorter(chosen_dir)
    sorter.organize_files()

    return "OK"


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")

