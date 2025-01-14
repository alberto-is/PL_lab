import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.List;


public class Main {
    public static void main(String[] args) throws Exception {
        
        /* Detección de la fuente de la entrada, desde teclado o fichero */
        
        String inputFile = null;
        if ( args.length>0 ) inputFile = args[0];
        InputStream is = System.in;
        if ( inputFile!=null ) is = new FileInputStream(inputFile);
        
        /* Conecta ANTLR con la entrada */
        
        CharStream input = CharStreams.fromStream(is);
        
        /* Crea el analizador léxico */ 
        
        mazeLexer lexer = new mazeLexer(input);
        
        /* Lanza el analizador léxico sobre la entrada y obtiene la secuencia de tokens */
        
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        
        /* Crea el analizador sintáctico */
        
        mazeParser parser = new mazeParser(tokens);
        
        /* Lanza el analizador sintáctico y obtiene el árbol de análisis */
        
        ParseTree tree = parser.level();
        
        /* System.out.println(tree.toStringTree(parser)); */
        
        /* Recorremos el árbol para darle significado */
        
        ParseTreeWalker walker= new ParseTreeWalker();
        Listener listener = new Listener();
        walker.walk(listener, tree);
        System.out.println();        
    }
}
