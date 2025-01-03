from lexer import lexer
from parser import parse

# Function to read a file and return its contents
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to test the lexer and parser on a file
def test_file(file_path):
    # Read the file content
    input_string = read_file(file_path)
    
    print(f"Testing file: {file_path}\n")
    
    # Tokenize the input using the lexer
    print("Lexer output:")
    lexer.input(input_string)
    for token in lexer:
        print(token)

    # Parse the input using the parser
    print("\nParser output:")
    try:
        parse(input_string)
        print("Parsing successful!")
    except Exception as e:
        print(f"Parsing failed: {e}")

correct_file = "./Maze/ej_maze_correcto.txt"
incorrect_file = "./Maze/ej_maze_incorrecto.txt"


# Test the correct file
print("Correct file")
test_file(correct_file)

# Test the incorrect file
#print("\nIncorrect file")
#test_file(incorrect_file)

