import os
import re
import logging
from package.file_organizer.file_sorter import FileSorter
from package.file_organizer.logger import log_function_call

@log_function_call
def main():
    current_dir = "./package/tests/file_organizer"
    directories = [item for item in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, item))]
    
    print("\nAvailable directories:")
    print("\n".join(directories))

    dir_name_pattern = r"^[a-zA-Z0-9_\-]+$"

    base_dir = input("Enter the directory to organize: ").strip()

    if not re.match(dir_name_pattern, base_dir):
        logging.error(f"Invalid directory name: {base_dir}")
        print("Error: Directory name contains invalid characters. Only alphanumeric characters, dashes, and underscores are allowed.")
        return

    chosen_dir = current_dir + "/" + base_dir

    if not os.path.exists(chosen_dir):
        logging.error(f"Directory does not exist: {base_dir}")
        print(f"Error: The directory '{base_dir}' does not exist.")
        return

    if not os.access(chosen_dir, os.W_OK):
        logging.error(f"Permission denied for directory: {base_dir}")
        print(f"Error: Permission denied to write in '{base_dir}'.")
        return
    
    print("Directory found and permissions are OK: Continuing")

    sorter = FileSorter(chosen_dir)
    sorter.organize_files()

    return "Success"

if __name__ == "__main__":
    main()

