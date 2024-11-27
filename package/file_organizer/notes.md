# File Organizer notes
Develop a script that organizes files in a directory based on their file types.
 ## Requirements
 1. File handling: Traverse directories and move files to appropriate folders.
 2. Modules and packages: Organize sorting logic, configuration, and logging into separate modules.
 3. Metaprogramming: Dynamically add new file type categories without modifying the core logic.
 4. Error Handling: Manage permissions issues and handle non-existent directories.
 5. Regular expressions: Identify file types using pattern matching.

 ## How it works
 1. run the program with "file-organizer". 
 2. the program lists directories in "package/tests/file_organizer". 
 3. type in the name of the directory you want to organize. 
 4. files are sorted based on their extention. 
  - if an extention is unknown, you will be prompted to chose where it should be sorted. 
  - your answer will be remembered so next time it will be automatic. 