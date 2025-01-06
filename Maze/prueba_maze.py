from MazeStructure import maze


def main():
    print(maze.dimensions)
    print(maze.entry)
    print(maze.exit)
    print(maze.list_points_path)
    print(maze.list_obstacles)
    print(maze.list_obstacles[0].type)

if __name__ == '__main__':
    main()