## Uso de la herramienta ANTLR

En este documento recogeremos todo lo necesario para poder utilizar la herramienta ANTLR y probar nuestra gramatica.

### Instalación de ANTLR (en VSCode)
- Tenemos que instalar la extensión de ANTLR4 en VSCode "ANTLR4 grammar syntax support".
- Instalamos ANTLR4 en nuestro sistema (en powershell).
``` pip install antlr4-tools ```
- Tenemos que añadir una configuración para poder ejecutar ANTLR4 en nuestro sistema.
Se te abrirá un archivo llamado "launch.json" y le damos a "Add Configuration".
    <div style="text-align: center;">
    <img src="images/image.png" width=500>
    </div>

    Se generará una nueva entrada en el archivo con el siguiente formato:

    <div style="text-align: center;">
    <img src="images/image2.png" width=250>
    </div>

    Donde en input pondriamos la ruta de nuestro archivo.txt y en grammar la ruta de nuestra gramatica .g4.

    Una vez hecho la configuración, podemos ir a la opcion de "Run and Debug" y seleccionar la configuración que hemos creado.

    <div style="text-align: center;">
    <img src="images/image3.png" width=150>
    </div>

<br>

### Ejecución via terminal





