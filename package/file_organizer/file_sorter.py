import os
import shutil
import re
import logging
from package.file_organizer.config import FILE_TYPE_CATEGORIES

class FileSorter:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def organize_files(self):
        for filename in os.listdir(self.base_dir):
            file_path = os.path.join(self.base_dir, filename)

            # Skip directories
            if os.path.isdir(file_path):
                continue

            # Determine file type
            file_type = self.identify_file_type(filename)
            if not file_type:
                file_type = "Others"

            # Create destination folder
            dest_folder = os.path.join(self.base_dir, file_type)
            os.makedirs(dest_folder, exist_ok=True)

            # Move file to the appropriate folder
            try:
                shutil.move(file_path, os.path.join(dest_folder, filename))
                logging.info(f"Moved: {file_path} -> {dest_folder}")
            except Exception as e:
                logging.error(f"Failed to move {file_path}: {e}")

    def identify_file_type(self, filename):
        # Match file extensions with regex patterns from config
        for file_type, pattern in FILE_TYPE_CATEGORIES.items():
            if re.search(pattern, filename, re.IGNORECASE):
                return file_type
        return None
