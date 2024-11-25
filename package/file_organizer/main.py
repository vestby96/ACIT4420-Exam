import os
import shutil
import re
import logging
from package.file_organizer.file_sorter import FileSorter

# Setup logging
logging.basicConfig(
    filename='package/file_organizer/file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    current_dir = "./package/tests"
    directories = [item for item in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, item))]
    
    print("\n".join(directories))

    base_dir = input("Enter the directory to organize: ").strip()
    chosen_dir = current_dir + "/" + base_dir

    # Validate directory
    if not os.path.exists(chosen_dir):
        logging.error(f"Directory does not exist: {base_dir}")
        print(f"Error: The directory '{base_dir}' does not exist.")
        return

    if not os.access(chosen_dir, os.W_OK):
        logging.error(f"Permission denied for directory: {base_dir}")
        print(f"Error: Permission denied to write in '{base_dir}'.")
        return
    
    print("Dir found and permissions are OK: Continuing")

    # Initialize FileSorter and start organizing
    sorter = FileSorter(chosen_dir)
    sorter.organize_files()

if __name__ == "__main__":
    main()
