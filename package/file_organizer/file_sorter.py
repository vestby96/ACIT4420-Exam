import shutil
import os
import logging
import re
from package.file_organizer.config import FILE_TYPE_CATEGORIES
from package.file_organizer.logger import log_function_call

class FileSorter:
    def __init__(self, base_dir, config_path="package/file_organizer/config.py"):
        self.base_dir = base_dir
        self.config_path = config_path

    @log_function_call
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
        return "Success"

    @log_function_call
    def identify_file_type(self, filename):
        for file_type, pattern in FILE_TYPE_CATEGORIES.items():
            if re.search(pattern, filename, re.IGNORECASE):
                return file_type

        # Prompt user for category if file type is unknown
        print(f"Unknown file type for '{filename}'.")
        ext = os.path.splitext(filename)[-1].lstrip('.').lower()
        print("Choose a category to add this file type to:")
        categories = list(FILE_TYPE_CATEGORIES.keys())
        for idx, category in enumerate(categories, 1):
            print(f"{idx}. {category}")

        try:
            choice = int(input("Enter the number of the category: ").strip())
            if 1 <= choice <= len(categories):
                chosen_category = categories[choice - 1]
                self.add_file_type_to_category(chosen_category, ext)
                return chosen_category
            else:
                print("Invalid choice. Skipping file.")
        except ValueError:
            print("Invalid input. Skipping file.")

        return "Others"

    def add_file_type_to_category(self, category, extension):
        # Fetch the current pattern for the category
        current_pattern = FILE_TYPE_CATEGORIES[category]
        
        # Update the pattern: insert the new extension inside the parentheses
        updated_pattern = re.sub(
            r"\((.*?)\)",  # Match the content inside parentheses
            lambda m: f"({m.group(1)}|{re.escape(extension)})",  # Append the new extension inside the parentheses
            current_pattern,
        )
        
        # Persist the changes to the config file before updating the in-memory dictionary
        self.update_config_file(category, current_pattern, updated_pattern)
        
        # Update the in-memory FILE_TYPE_CATEGORIES
        FILE_TYPE_CATEGORIES[category] = updated_pattern
        
        logging.info(f"Added extension '.{extension}' to category '{category}'.")



    def update_config_file(self, category, current_pattern, updated_pattern):
        # Read the current config file
        with open(self.config_path, "r") as file:
            config_data = file.read()

        # Replace the old pattern with the updated pattern for the specific category
        old_entry = f'"{category}": r"{current_pattern}"'
        new_entry = f'"{category}": r"{updated_pattern}"'
        if old_entry not in config_data:
            logging.error(f"Failed to update config: Pattern for category '{category}' not found.")
            return

        config_data = config_data.replace(old_entry, new_entry)

        # Write the updated config back to the file
        with open(self.config_path, "w") as file:
            file.write(config_data)

