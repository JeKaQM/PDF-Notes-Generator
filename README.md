# PDF-Notes-Generator
A simple Python based application that uses OpenAI API to generate notes from a PDF File.

Create a .env file and store your API key there, the file should contain: OPENAI_API_KEY="YOUR KEY"

## NG_CMD MANUAL
This version is **Command Line** built
1. PDF file should be stored in the same directory as the application otherwise specify direct path.
2. The output will be stores in the same directory as the application, new folder called Notes will be created, your output will be saved there, be sure to specify the name of the output file such as 123etc.txt

##NG_Custom_Prompt MANUAL
This version is **GUI** built
1. Select pdf from any location on the machine.
2. Output can be saved into any selected directory, just give the file a name and its extension such as .txt. Type of file is not limited to txt so you can save it to any other type you like.
3. Enter any prompt you wish, if you need particular data from a file or simple notes just type out your instruction and hit generate.
4. Stop generating option will stop the loop however any already generated responses will be saved.

Some Screenshots
================

### Main Screen
![Capture](https://user-images.githubusercontent.com/74925827/231019411-821a1a8c-d79e-4307-8705-f30ebda183c5.PNG)

### Proccessing Screen
![2](https://user-images.githubusercontent.com/74925827/231020288-bcd30777-1dc3-4172-963b-818e2835a8d1.PNG)

