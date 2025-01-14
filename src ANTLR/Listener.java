import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.Vector;
import java.util.Objects;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Array;


class Point {
   private int x;
   private int y;

   public Point(int x, int y) {
       this.x = x;
       this.y = y;
   }

   public int getX() { return x; }
   public int getY() { return y; }
   
   @Override
   public String toString() {
       return "(" + x + "," + y + ")";
   }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Point point = (Point) o;
        return x == point.x && y == point.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
}

public class Listener extends mazeBaseListener {
    // Atributos para almacenar la información del laberinto
    private Point mazeDimensions;
    private Point entry;
    private Point exit;

    private List<Room> rooms = new ArrayList<>();
    private List<Obstacle> obstacles = new ArrayList<>();
    private List<Path> paths = new ArrayList<>();
    private List<String> errors = new ArrayList<>();
    private List<String> warnings = new ArrayList<>();
    private List<Point> list_obstacles_points = new ArrayList<>();

    
    // Métodos para obtener la información del laberinto
    public Point getMazeDimensions() { return mazeDimensions; }
    public Point getEntry() { return entry; }
    public Point getExit() { return exit; }
    public List<Room> getRooms() { return rooms; }
    public List<Obstacle> getObstacles() { return obstacles; }
    public List<Point> getAllPointGenerated() { 
        // Devolveremos una lista con solo los puntos generados tanto manualmente como autogenerado
        List<Point> pointsToReturn = new ArrayList<>();
        for (Path path : paths) {
           for (Point point : path.points) {
               pointsToReturn.add(point);
           }
        }
        return pointsToReturn;
    }


    //--------------------------------------------------------------------------------------------------------------------------
    // Metodos de control de fallos
    //--------------------------------------------------------------------------------------------------------------------------

    // Método auxiliar para validar coordenadas
    private void validateCoordinates(int x, int y, String elementType) {
        if (mazeDimensions == null) {
            errors.add("Error: Las dimensiones del laberinto deben definirse antes de añadir elementos");
            return;
        }
        
        if (x < 0 || x >= mazeDimensions.getX() || y < 0 || y >= mazeDimensions.getY()) {
            errors.add(String.format(
                "Error: Coordenadas (%d,%d) fuera de los limites del laberinto [0,%d]x[0,%d] para %s",
                x, y, mazeDimensions.getX() - 1, mazeDimensions.getY() - 1, elementType
            ));
            return;
        }

        // Comprobar si la coordenada ya ha sido utilizada por otro elemento
        Point p = new Point(x, y);
        boolean isRepeated = false;
        for (Point point : list_obstacles_points) {
            if (point.getX() == x && point.getY() == y && !elementType.equals("habitación") && !elementType.equals("trampa (destino)")) {
                isRepeated = true;
                errors.add(String.format("Error: Coordenadas (%d,%d) de %s ya han sido utilizadas por otro elemento", x, y, elementType));
                break;
            }
        }

        // Añadir la coordenada a la lista de puntos de obstáculos si no esta repetida
        if (!isRepeated && !elementType.equals("habitación")) {
            list_obstacles_points.add(p); 
        } 
        
    }

    // Método para validar dimensiones de habitaciones
    private void validateRoomDimensions(int x, int y, int width, int height, String elementType) {
        // Validar que la posición inicial está dentro del laberinto
        validateCoordinates(x, y, elementType);
        
        // Validar que la habitación no se sale de los límites
        if (x + width > mazeDimensions.getX() || y + height > mazeDimensions.getY()) {
            throw new RuntimeException(
                String.format("Error: La habitación en (%d,%d) con dimensiones %dx%d se sale de los limites del laberinto",
                    x, y, width, height)
            );
        }
    }

    // Metodo para comprobar si un punto ya se encuentra en la lista de puntos
    private boolean isPointInPath(Point p, List<Path> list) {
        for (Path path : list) {
            for (Point point : path.points) {
                if (point.getX() == p.getX() && point.getY() == p.getY()) {
                    return true;
                }
            }
        }
        return false;
    }

    //--------------------------------------------------------------------------------------------------------------------------
    // Metodos Del programa
    //--------------------------------------------------------------------------------------------------------------------------

   @Override
   public void exitLevel(mazeParser.LevelContext ctx) {
       List<Obstacle> obstacles_witout_path = new ArrayList<>();

       //comprobar que todos los obstaculos esten dentro de algun camino disponible
       // que comparta la misma coordenada con algun camino
        for (Obstacle obs : obstacles) {
            boolean isInsidePath = false;
            for (Path path : paths) {
                for (Point point : path.points) {
                        if (point.getX() == obs.getPosition().getX() && point.getY() == obs.getPosition().getY()) {
                            isInsidePath = true;
                            break;
                        }
                }
            }

            if (!isInsidePath) {
                obstacles_witout_path.add(obs); //Añadimos el obstaculo a la lista de obstaculos sin camino
                errors.add("ERROR: El obstaculo " + obs + " no está en ningún camino.");
            }
        }

        // Comprobamos si hay mas puertas que llaves 
        int doors = 0;
        int keys = 0;

        for (Obstacle obs : obstacles) {
            if (obs.getType().equals("DOOR")) {
                doors++;
            } else if (obs.getType().equals("KEY")) {
                keys++;
            }
        }

        if (doors > keys) {
            errors.add("ERROR: Hay más puertas que llaves en el laberinto.");   
        }


        // Eliminamos los obstaculos que no estan en ningun camino
        for (Obstacle obs : obstacles_witout_path) {
            obstacles.remove(obs);
        }

        // Comprobamos si las coordenadas de destino de las trampas estan en algun camino
        for (Obstacle obs : obstacles) {
            if (obs.getType().equals("TRAP")) {
                boolean isInsidePath = false;
                for (Path path : paths) {
                    for (Point point : path.points) {
                        if (point.getX() == obs.getDestination().getX() && point.getY() == obs.getDestination().getY()) {
                            isInsidePath = true;
                            break;
                        }
                    }
                }
                if (!isInsidePath) {
                    errors.add("Error: El destino de la trampa " + obs + " no está en ningún camino.");
                }
            }
        }
       
        // Mostrar advertencias
        if (!warnings.isEmpty()) {
            System.out.println("\nWarnings encontradas durante el analisis:");
            for (String warning : warnings) {
                System.out.println("- " + warning);
            }
        }

        // Mostrar errores
        if (!errors.isEmpty()) {
           System.err.println("\nError en la creacion del laberinto:");
           System.err.println("Errores encontrados durante el analisis:");
           for (String error : errors) {
               System.err.println("- " + error);
           }
           System.err.println("No se ha podido generar el archivo MazeStructure.py.");
       } else {
           System.out.println("Analisis completado sin errores.");
           List<Point> points = getAllPointGenerated();
           // Creamos el objeto python para la representacion del laberinto
           generatePythonFile(mazeDimensions, entry, exit, points, obstacles);
       }

   }
    
   // Métodos para procesar las dimensiones globales
   @Override
   public void exitGobal_dim(mazeParser.Gobal_dimContext ctx) {
       int width = Integer.parseInt(ctx.number(0).getText());
       int height = Integer.parseInt(ctx.number(1).getText());
       tempDimensions = new Point(width, height);
       
       // Si estamos en el contexto global del laberinto
       if (ctx.getParent() instanceof mazeParser.MazeContext) {
           mazeDimensions = tempDimensions;
       }
   }

   // Métodos para procesar la entrada
   @Override
   public void exitCord_entry(mazeParser.Cord_entryContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());
      validateCoordinates(x, y, "punto de entrada");

      if (!errors.isEmpty()) {
        return; // Salir del método sin procesar el elemento si hay errores
      }

      entry = new Point(x, y);
   }

   // Métodos para procesar la salida
   @Override
   public void exitCord_exit(mazeParser.Cord_exitContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());
      validateCoordinates(x, y, "punto de salida");

      exit = new Point(x, y);
   }

   // Clase interna para representar una habitación
   private class Room {
      private Point position;
      private Point dimensions;

      public Room(Point position, Point dimensions) {
         this.position = position;
         this.dimensions = dimensions;
      }

      public Point getPosition() { return position; }
      public Point getDimensions() { return dimensions; }
      public String toString() {
         return "Room at " + position + " with dimensions " + dimensions;
      }
   }

   private Room currentRoom;
   private Point tempDimensions; // Variable temporal para almacenar dimensiones


   @Override
   public void exitDim_room(mazeParser.Dim_roomContext ctx) {
       // Obtener la posición inicial (FROM)
       int startX = Integer.parseInt(ctx.number(0).getText());
       int startY = Integer.parseInt(ctx.number(1).getText());
       Point position = new Point(startX, startY);
       
       // Usar las dimensiones que fueron procesadas en exitGobal_dim
       if (tempDimensions == null) {
           throw new RuntimeException("Error: Dimensiones no encontradas para la habitación");
       }

       validateRoomDimensions(startX, startY, tempDimensions.getX(), tempDimensions.getY(), "habitación");

       
       // Crear la nueva habitación con la posición y las dimensiones almacenadas
       currentRoom = new Room(position, tempDimensions);

       // Añadir la habitación creada a la lista global
       rooms.add(currentRoom);
       // Añadir la extension de la habitacion como puntos y guardarlos en los caminos
         for (int i = 0; i < tempDimensions.getX(); i++) {
              for (int j = 0; j < tempDimensions.getY(); j++) {
                Point p = new Point(startX + i, startY + j);
                //Comprobar si el punto ya está definido como camino 
                if (!isPointInPath(p, paths)){
                    paths.add(new Path());
                    paths.get(paths.size() - 1).addPoint(p);
                }else{
                    warnings.add("WARNING: El punto " + p + " ya se ha definido anteriormente.");
                }

              }
         }
       
       // Limpiar las dimensiones temporales
       tempDimensions = null;
   }

   @Override
   public void enterDim_room(mazeParser.Dim_roomContext ctx) {
       // Asegurarnos de que no hay dimensiones residuales de operaciones anteriores
       tempDimensions = null;
   }

   // Clase interna para representar un obstáculo
   private class Obstacle {
      private String type;
      private String enemy_type; // Para los enemigos
      private Point position;
      private Point destination; // Para las trampas que tienen punto de destino

      public Obstacle(String type, Point position) {
            this.type = type;
            this.position = position;
      }

      public Obstacle(String type, Point position, Point destination) {
            this.type = type;
            this.position = position;
            this.destination = destination;
      }

      public Obstacle(String type, String enemy_type, Point position) {
            this.type = type;
            this.enemy_type = enemy_type;
            this.position = position;
      }

      public String getType() { return type; }
      public Point getPosition() { return position; }
      public Point getDestination() { return destination; }
      public String getEnemyType() { return enemy_type; }

      public String toString() {
            return type + " at " + position + (destination != null ? " with destination " + destination : "") + (enemy_type != null ? " of type " + enemy_type : "");
      }
   }

   
    // Métodos para procesar los obstáculos
    @Override
    public void exitCord_bomb(mazeParser.Cord_bombContext ctx) {
        int x = Integer.parseInt(ctx.number(0).getText());
        int y = Integer.parseInt(ctx.number(1).getText());

        validateCoordinates(x, y, "bomba"); // Validar que las coordenadas están dentro del laberinto

        // Crear un nuevo obstáculo de tipo BOMB y agregarlo a la lista
        Obstacle bomb = new Obstacle("BOMB", new Point(x, y));
        obstacles.add(new Obstacle("BOMB", new Point(x, y)));
    }

    @Override
    public void exitCord_enemy(mazeParser.Cord_enemyContext ctx) {
        int x = Integer.parseInt(ctx.number(0).getText());
        int y = Integer.parseInt(ctx.number(1).getText());
        String enemyType = ctx.enemy_type().getText();

        validateCoordinates(x, y, "enemigo"); // Validar que las coordenadas están dentro del laberinto

        // Crear un nuevo obstáculo de tipo ENEMY y agregarlo a la lista
        Obstacle enemy = new Obstacle("ENEMY", enemyType, new Point(x, y));
        obstacles.add(enemy);
    }

   @Override
   public void exitCord_door(mazeParser.Cord_doorContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());

      validateCoordinates(x, y, "puerta"); // Validar que las coordenadas están dentro del laberinto

      obstacles.add(new Obstacle("DOOR", new Point(x, y)));
      Obstacle door = new Obstacle("DOOR", new Point(x, y));
   }
   
   @Override
   public void exitCord_key(mazeParser.Cord_keyContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());

      validateCoordinates(x, y, "llave"); // Validar que las coordenadas están dentro del laberinto

      obstacles.add(new Obstacle("KEY", new Point(x, y)));
      Obstacle key = new Obstacle("KEY", new Point(x, y));
   }
   
   @Override
   public void exitCord_coin(mazeParser.Cord_coinContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());

      validateCoordinates(x, y, "moneda"); // Validar que las coordenadas están dentro del laberinto

      obstacles.add(new Obstacle("COIN", new Point(x, y)));
      Obstacle coin = new Obstacle("COIN", new Point(x, y));
   }

    @Override
    public void exitCord_trap(mazeParser.Cord_trapContext ctx) {
        int x1 = Integer.parseInt(ctx.number(0).getText());
        int y1 = Integer.parseInt(ctx.number(1).getText());
        int x2 = Integer.parseInt(ctx.number(2).getText());
        int y2 = Integer.parseInt(ctx.number(3).getText());

        validateCoordinates(x1, y1, "trampa (origen)");
        validateCoordinates(x2, y2, "trampa (destino)");
         
        obstacles.add(new Obstacle("TRAP", 
            new Point(x1, y1), 
            new Point(x2, y2)));
         
         Obstacle trap = new Obstacle("TRAP", new Point(x1, y1), new Point(x2, y2));
    }

      /**
     * Clase que representa un camino en el laberinto.
     * Puede ser generado automáticamente (FROM-TO) o definido punto por punto.
     */
   private class Path {
      private List<Point> points;
      private boolean isAutoGenerated;  // Indica si el camino fue generado automáticamente

      public Path() {
          this.points = new ArrayList<>();
          this.isAutoGenerated = false;
      }

      /**
       * Genera automáticamente los puntos intermedios entre dos coordenadas
       * Asume que el movimiento es primero en X y luego en Y
       */
      public void generatePointsBetween(Point start, Point end) {
          this.isAutoGenerated = true;
          points.clear();
          
          int currentX = start.getX();
          int currentY = start.getY();
          int endX = end.getX();
          int endY = end.getY();
        
          // Comprobamos que el camino sea recto
            if (currentX != endX && currentY != endY) {
                errors.add("Error: El camino entre " + start + " y " + end + " no es recto.");
            }

          // miramos si el camino es horizontal o vertical
          if (currentX == endX) {
              // Si es horizontal, movemos en Y
              while (currentY != endY) {
                  Point p = new Point(currentX, currentY);
                  if (!isPointInPath(p, paths)){
                      points.add(p);
                  }else{
                      warnings.add("WARNING: El punto " + p + " ya se ha definido anteriormente.");
                  }
                  currentY += (currentY < endY) ? 1 : -1;
              }
          }
          // Si es vertical, movemos en X
            if (currentY == endY) {
                while (currentX != endX) {
                    Point p = new Point(currentX, currentY);
                    if (!isPointInPath(p, paths)){
                        points.add(p);
                    }else{
                        warnings.add("WARNING: El punto " + p + " ya se ha definido anteriormente.");
                    }
                    currentX += (currentX < endX) ? 1 : -1;
                }
            }

        // Añadimos el punto final
        Point p = new Point(endX, endY);
        if (!isPointInPath(p, paths)){
            points.add(p);
        }else{
            warnings.add("WARNING: El punto " + p + " ya se ha definido anteriormente.");
        }

      }

      public void addPoint(Point p) {
          points.add(p);
      }

      @Override
      public String toString() {
          StringBuilder sb = new StringBuilder();
          sb.append(isAutoGenerated ? "Camino autogenerado: " : "Camino manual: ");
          for (Point p : points) {
              sb.append(p).append(" -> ");
          }
          if (!points.isEmpty()) {
              sb.setLength(sb.length() - 4); // Eliminar la última flecha
          }
          return sb.toString();
      }

    private boolean isValidPath() {
        // Validar si todos los puntos del camino están dentro de los límites del laberinto
        for (Point p : points) {
            if (p.getX() < 0 || p.getX() >= mazeDimensions.getX() || p.getY() < 0 || p.getY() >= mazeDimensions.getY()) {
                return false; // El camino tiene un punto fuera de los límites
            }
        }
        return true; // El camino está completamente dentro de los límites
    }

  }


  /**
   * Procesa un camino definido con FROM ... TO
   * Genera automáticamente los puntos intermedios
   */
  @Override
  public void exitCord_path(mazeParser.Cord_pathContext ctx) {
      // Verificamos si es un camino FROM ... TO
      if (ctx.number() != null) {
          Point start = new Point(
                  Integer.parseInt(ctx.number(0).getText()),
                  Integer.parseInt(ctx.number(1).getText())
          );
  
          Point end = new Point(
                  Integer.parseInt(ctx.number(2).getText()),
                  Integer.parseInt(ctx.number(3).getText())
          );
  
          Path path = new Path();
          path.generatePointsBetween(start, end);
  
          // Validar que el camino esté dentro de los límites del laberinto
          if (!path.isValidPath()) {
              errors.add(String.format("Error: El camino entre %s y %s esta fuera de los limites del laberinto.", start, end));
              return; // Si no es válido, no agregamos el camino
          }
  
          paths.add(path);
      }
  }
  

   /**
   * Procesa un punto individual dentro de un PATH {...}
   */
  @Override
  public void exitCord_point(mazeParser.Cord_pointContext ctx) {
      // Si no hay caminos o el último camino es autogenerado, crear uno nuevo
      if (paths.isEmpty() || paths.get(paths.size() - 1).isAutoGenerated) {
          paths.add(new Path());
      }
  
      Point point = new Point(
              Integer.parseInt(ctx.number(0).getText()),
              Integer.parseInt(ctx.number(1).getText())
      );
  
      // Validar que el punto esté dentro de los límites del laberinto
      if (point.getX() < 0 || point.getX() >= mazeDimensions.getX() || point.getY() < 0 || point.getY() >= mazeDimensions.getY()) {
          errors.add("Error: El punto " + point + " está fuera de los límites del laberinto.");
          return; // Salir sin añadir el punto
      }
  
      // Comprobamos que el punto no esté repetido
        if (isPointInPath(point, paths)) {
            warnings.add("WARNING: El punto " + point + " ya se ha definido anteriormente.");
            return; // Salir sin añadir el punto
        }
      // Añadir el punto al último camino
      paths.get(paths.size() - 1).addPoint(point);
  }

    // Metodo para generar el archivo python
    private void generatePythonFile(Point mazeDimensions, 
        Point entry, Point exit, List<Point> list_points_path, List<Obstacle> list_obstacle){
        FileWriter myWriter = null;
        try {
            myWriter = new FileWriter("MazeStructure.py"); 
            myWriter.write("# Archivo generado desde JAVA, ¡NO MODIFICAR!\n\n");
            // Clase Obstacle
            myWriter.write("class Obstacle:\n");
            myWriter.write("\tdef __init__(self, type, position, destination=None, enemy_type=None):\n");
            myWriter.write("\t\tself.type = type\n");
            myWriter.write("\t\tself.enemy_type = enemy_type\n");
            myWriter.write("\t\tself.position = position\n");
            myWriter.write("\t\tself.destination = destination\n\n");

            // Clase Maze
            myWriter.write("class MazeStructure:\n");
            myWriter.write("\tdef __init__(self, dimensions, entry, exit, list_points_path, list_obstacles):\n");
            myWriter.write("\t\tself.dimensions = dimensions\n");
            myWriter.write("\t\tself.entry = entry\n");
            myWriter.write("\t\tself.exit = exit\n");
            myWriter.write("\t\tself.list_points_path = list_points_path\n");
            myWriter.write("\t\tself.list_obstacles = list_obstacles\n\n");

            // Crear el objeto MazeStructure
            myWriter.write(String.format("# Crear el objeto MazeStructure\n"));
            myWriter.write(String.format("maze_structure = MazeStructure(\n"));
            myWriter.write(String.format("\t(%d, %d),\n", mazeDimensions.getX(), mazeDimensions.getY()));
            myWriter.write(String.format("\t(%d, %d),\n", entry.getX(), entry.getY()));
            myWriter.write(String.format("\t(%d, %d),\n", exit.getX(), exit.getY()));
            myWriter.write(String.format("\t[\n"));
            // Añadimos los puntos de los caminos
            for (Point p : list_points_path) {
                myWriter.write(String.format("\t\t(%d, %d),\n", p.getX(), p.getY()));
            }
            myWriter.write(String.format("\t],\n"));
            // Añadir los obstáculos
            myWriter.write(String.format("\t[\n"));
            for (Obstacle obs : list_obstacle) {
                if (obs.getDestination() != null) {
                    myWriter.write(String.format("\t\tObstacle('%s', (%d, %d), (%d, %d)),\n", obs.getType(), obs.getPosition().getX(), obs.getPosition().getY(), obs.getDestination().getX(), obs.getDestination().getY()));
                } else if (obs.getEnemyType() != null) {
                    myWriter.write(String.format("\t\tObstacle('%s', (%d, %d),enemy_type='%s'),\n", obs.getType(), obs.getPosition().getX(), obs.getPosition().getY(), obs.getEnemyType()));
                } else {
                    myWriter.write(String.format("\t\tObstacle('%s', (%d, %d)),\n", obs.getType(), obs.getPosition().getX(), obs.getPosition().getY()));
                }
            }
            
            myWriter.write("\t],\n"); 
            myWriter.write(")\n\n");
            myWriter.flush(); // volcamos la info restante del buffer al archivo
            myWriter.close();
            System.out.println("Archivo MazeStructure.py generado correctamente.");

        }catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    
    }
}

 
