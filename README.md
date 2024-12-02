# ACIT4420-Exam
 Repo for ACIT4420
 This repo represents two different projects; tarjan-planner and file-organizer.
 
 ## How to Install
  1. Download the repo
  2. Using powershell/terminal, navigate to the base directory
  3. Run the following command to install the package:
   - $ pip install .
 
 ## Tarjan Planner
  
 ### How to Use
  1. $ tarjan-planner
  2. Options:
   - -c: prioritize cost over time
   - -b: let the program use bicycle
   - -p: display the plot
 
 ## File Organizer
 
 
 ### How to Use
 1. $ file-organizer
 
 ## Structure requirements
  1. Main module (main.py): The entry point of your application. It should orchestrate the program’s functionality by calling appropriate functions or classes from other modules.
  2. Custom modules: Implement at least three key functions or classes, each addressing a specific aspect of the problem. Organize these into separate files (e.g., module1.py, module2.py, etc.).
  3. File Handling: Incorporate functionality that reads from or writes to files (e.g., configuration files, logs, data storage).
  4. Metaprogramming: Apply metaprogramming techniques such as decorators or dynamic class modifications to enhance your code’s flexibility and maintainability.
  5. Error Handling: Implement custom error handling to manage runtime issues like file not found, invalid inputs, or network errors.
  6. Regular expressions: Use regular expressions for tasks such as input validation, data parsing, or pattern matching where applicable.
  7. Testing: Write unit tests for your functions or classes using pytest. Ensure that your tests cover various scenarios and edge cases. (optional)

 ## General notes
  - The project is contained in a single package including all tasks.