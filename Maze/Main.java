import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import java.io.FileInputStream;
import java.io.InputStream;

public class Main {
    public static void main(String[] args) throws Exception {
        // Verifica que se haya pasado un archivo como argumento
        if (args.length < 1) {
            System.err.println("Por favor, especifica el archivo de entrada.");
            return;
        }

        // Leer el archivo de entrada
        String fileName = args[0];
        InputStream inputStream = new FileInputStream(fileName);

        // Crear un objeto CharStream desde el archivo
        CharStream input = CharStreams.fromStream(inputStream);

        // Crear el lexer, parser y ejecutar el análisis
        mazeLexer lexer = new mazeLexer(input);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        mazeParser parser = new mazeParser(tokens);

        // Inicia el análisis desde la regla más alta definida (e.g., 'program')
        ParseTree tree = parser.program();

        // Mostrar el árbol de análisis generado
        System.out.println(tree.toStringTree(parser));
    }
}
