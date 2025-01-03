import java.util.ArrayList;
import java.util.List;

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
}

public class Listener extends mazeBaseListener {
   // Atributos para almacenar la información del laberinto
   private Point mazeDimensions;
   private Point entry;
   private Point exit;

   @Override 
   public void enterLevel(mazeParser.LevelContext ctx){   
      System.out.println("Llamada a Level");       
   } 
   
   @Override
   public void exitLevel(mazeParser.LevelContext ctx){   
      System.out.println("Saliendo del programa");     
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
           System.out.println("Dimensiones del laberinto establecidas: " + mazeDimensions);
       }
       // No hacemos nada más aquí, las dimensiones quedan guardadas en tempDimensions
   }

   // Métodos para procesar la entrada
   @Override
   public void exitCord_entry(mazeParser.Cord_entryContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());
      entry = new Point(x, y);
      System.out.println("Punto de entrada: " + entry);
   }

   // Métodos para procesar la salida
   @Override
   public void exitCord_exit(mazeParser.Cord_exitContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());
      exit = new Point(x, y);
      System.out.println("Punto de salida: " + exit);
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
       
       // Crear la nueva habitación con la posición y las dimensiones almacenadas
       currentRoom = new Room(position, tempDimensions);
       //rooms.add(currentRoom); esto para despues
       
       System.out.println("Habitación creada: " + currentRoom);
       
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

      public String getType() { return type; }
      public Point getPosition() { return position; }
      public Point getDestination() { return destination; }

      public String toString() {
            return type + " at " + position + (destination != null ? " with destination " + destination : "");
      }
   }

   
    // Métodos para procesar los obstáculos
    @Override
    public void exitCord_bomb(mazeParser.Cord_bombContext ctx) {
        int x = Integer.parseInt(ctx.number(0).getText());
        int y = Integer.parseInt(ctx.number(1).getText());
        // Crear un nuevo obstáculo de tipo BOMB y agregarlo a la lista
        Obstacle bomb = new Obstacle("BOMB", new Point(x, y));
        //obstacles.add(new Obstacle("BOMB", new Point(x, y)));
        System.out.println("Bomba " + bomb);
    }

    @Override
    public void exitCord_enemy(mazeParser.Cord_enemyContext ctx) {
        int x = Integer.parseInt(ctx.number(0).getText());
        int y = Integer.parseInt(ctx.number(1).getText());
        String enemyType = ctx.enemy_type().getText();
         // Crear un nuevo obstáculo de tipo ENEMY y agregarlo a la lista
         Obstacle enemy = new Obstacle("ENEMY_" + enemyType, new Point(x, y));
        //obstacles.add(new Obstacle("ENEMY_" + enemyType, new Point(x, y)));
         System.out.println("Enemigo " + enemy);
    }

   @Override
   public void exitCord_door(mazeParser.Cord_doorContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());
      //obstacles.add(new Obstacle("DOOR", new Point(x, y)));
      Obstacle door = new Obstacle("DOOR", new Point(x, y));
      System.out.println("Puerta " + door);
   }
   
   @Override
   public void exitCord_key(mazeParser.Cord_keyContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());
      //obstacles.add(new Obstacle("KEY", new Point(x, y)));
      Obstacle key = new Obstacle("KEY", new Point(x, y));
      System.out.println("Llave " + key);
   }
   
   @Override
   public void exitCord_coin(mazeParser.Cord_coinContext ctx) {
      int x = Integer.parseInt(ctx.number(0).getText());
      int y = Integer.parseInt(ctx.number(1).getText());
      //obstacles.add(new Obstacle("COIN", new Point(x, y)));
      Obstacle coin = new Obstacle("COIN", new Point(x, y));
      System.out.println("Moneda " + coin);
   }

    @Override
    public void exitCord_trap(mazeParser.Cord_trapContext ctx) {
        int x1 = Integer.parseInt(ctx.number(0).getText());
        int y1 = Integer.parseInt(ctx.number(1).getText());
        int x2 = Integer.parseInt(ctx.number(2).getText());
        int y2 = Integer.parseInt(ctx.number(3).getText());
        /* 
        obstacles.add(new Obstacle("TRAP", 
            new Point(x1, y1), 
            new Point(x2, y2)));
         */
         Obstacle trap = new Obstacle("TRAP", new Point(x1, y1), new Point(x2, y2));
         System.out.println("Trampa " + trap);
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

          // Primero movemos en X
          while (currentX != endX) {
              points.add(new Point(currentX, currentY));
              currentX += (currentX < endX) ? 1 : -1;
          }

          // Luego movemos en Y
          while (currentY != endY) {
              points.add(new Point(currentX, currentY));
              currentY += (currentY < endY) ? 1 : -1;
          }

          // Añadimos el punto final
          points.add(new Point(endX, endY));
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
         //paths.add(path);

         System.out.println("Creado nuevo camino: " + path);
      }
   }

   /**
   * Procesa un punto individual dentro de un PATH {...}
   */
   @Override
   public void exitCord_point(mazeParser.Cord_pointContext ctx) {
      // Si no hay caminos o el último camino es autogenerado, crear uno nuevo

      // if (paths.isEmpty() || paths.get(paths.size() - 1).isAutoGenerated) {
      //    paths.add(new Path());
      // }

      Point point = new Point(
         Integer.parseInt(ctx.number(0).getText()),
         Integer.parseInt(ctx.number(1).getText())
      );

      // Añadir el punto al último camino
      //paths.get(paths.size() - 1).addPoint(point);
      System.out.println("Añadido punto " + point + " al camino actual");
   }

}
