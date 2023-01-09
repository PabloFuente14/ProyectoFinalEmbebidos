# ProyectoFinalEmbebidos
En este repositorio subiremos las actualizaciones de código que hemos ido haciendo y haremos durante el desarrolllo del mismo.
En la Carpeta 'Archivos de prueba' hemos introducido aquellos archivos de prueba que hemos ido utilizando a lo largo del proyecto. No son funcionales en esta entrega. 

Para la correcta ejecución del proyecto,  simplemente vale con ejecutar el archivo Proyecto_Final_PYV.py

Para poder visualizar la base de datos, en la consola de la RPI tenemos que escribir: sudo mysql -u root
Una vez dentro, para seleccionar nuestra base de datos hay que poner: USE DatosFabrica;
Una vez hecho esto, tenemos dos tablas, Contador y Temp_hum, las podemos visualizar con: SELECT * FROM Contador;

Para acceder a Grafana, tenemos que escribir en un navegador la ip de la raspberry seguido de :3000 (el puerto)
!!!Importante, solamente funcionará en equipos que estén dentro de la misma red. 
En nuestro caso: 192.168.0.169:300