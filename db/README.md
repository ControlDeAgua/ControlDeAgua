# Cómo utilizar esta base de datos

Al instalar limpiamente el código de `ControlDeAgua`, se incluye el archivo SQLite
(`WaterDB.sqlite3`), completamente vacío. Esto lo hicimos para evitar problemas de
transporte.

Sin embargo, al ejecutar la aplicación principal, puede hallar el siguiente mensaje
(o alguno parecido) en una ventana de error:

```
Traceback (most recent call last):
  [muchos nombres de archivo...] 
sqlite3.OperationalError: File is not a database
```

Esto se debe a que el archivo de la base de datos está **totalmente vacío** (ni siquiera tiene
datos de configuración, que son necesarios para agregar información a las tablas).
Una manera útil de solucionar este problema es usar la app para eliminar la base de datos.

Suena ilógico, pero resuelve el problema. Y es que esta función deja a la base de
datos con la configuración, pero sin información (en vez de dejar el
archivo "totalmente vacío"). Gracias a eso, el archivo ahora será válido, y se
podrá utilizar en el resto de las aplicaciones.

Esto también aplica cuando la base de datos sufrió daños y no puede ser reconocida.
