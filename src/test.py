from parser import parse

# Function to read a file and return its contents
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to test the lexer and parser on a file
def test_file(file_path):
    # Read the file content
    maze = None
    input_string = read_file(file_path)
    
    print(f"Testing file: {file_path}\n")

    # Parse the input using the parser
    print("\nParser output:")
    try:
        maze = parse(input_string)
        print("Parsing successful!")
    except Exception as e:
        print(f"Parsing failed: {e}")
    return maze

correct_file = "./Maze/ej_maze_correcto_semantica.txt"
incorrect_file = "./Maze/ej_maze_incorrecto.txt"


# Test the correct file
print("Correct file")
maze = test_file(correct_file)
if maze is not None:
    print("\nMaze:")
    print(maze.print())
else:
    print("\nMaze not created") 

