<h1 style="text-align:center">Minecraft Server</h1>

Este repositorio contiene la estructura y los scripts necesarios para instalar y gestionar un servidor de Minecraft no oficial. Se proporciona una configuración básica y fácil de usar para comenzar a jugar con cuentas no oficiales.


<div style="text-align: center;">
    <img style="width: 400px;" src="assets/logo.jpg" alt="Logo">
</div>

## Requisitos
- Raspberry Pi: Este servidor está diseñado para funcionar en una Raspberry Pi con Ubuntu Server.
- Conexión a Internet: Necesaria para descargar los archivos necesarios.

## Instalación

1. Clonar el repositorio:
      git clone https://github.com/otema666/minecraft-server.git
   cd minecraft-server
   

2. Ejecutar el script de instalación:
      chmod +x install.sh
   ./install.sh
   

3. Iniciar el servidor:
      ./start.sh
   
### Instalación del cliente:
[Click aquí para ver la guía de instalación en el cliente](client.md)

## Configuración
- La configuración principal del servidor se encuentra en el archivo [server.properties](server.properties)
- Los archivos de configuración se encuentran en la carpeta [config/](config/). Puedes editar los archivos .yml según tus preferencias.

### Ejemplos de configuración:

- server.yml: Configuraciones del servidor.
- permissions.yml: Configuraciones de permisos para usuarios.

## Plugins
El servidor cuenta con estos plugins:

* [BlueMap](plugins/bluemap-5.4-paper.jar): Crea un mapa 3D del mundo de Minecraft para visualizar en un navegador.
* [MiniMotd](plugins/minimotd-bukkit-2.1.3.jar): Personaliza el mensaje del día (MOTD) que aparece en la lista de servidores.
* [ImageFrame](plugins/ImageFrame-1.7.13.0.jar): Permite colocar imágenes directamente en marcos en el juego.
* [QualityArmory](plugins/QualityArmory.jar): Añade armas de fuego y mejoras al sistema de combate en Minecraft.
* [DeathChest](plugins/deathchest.jar): Genera cofres en el lugar donde un jugador muere, guardando sus pertenencias.
* [TabTPS](plugins/tabtps-spigot-1.3.26.jar): Muestra estadísticas como TPS y uso de memoria en la lista de jugadores (tabulador).
* [Chunky](plugins/chunky-1.3.0.jar): Permite la generación de terrenos de manera eficiente y optimizada, mejorando el rendimiento del servidor.

Para la guía de instalación de plugins, consultar estas páginas:

* [Hangar de Plugins](https://hangar.papermc.io/paper)
* [docs.papermc.io](https://docs.papermc.io/paper/next-steps)
* [raspberrytips.es](https://raspberrytips.es/minecraft-servidor-raspberry-pi/)


## Uso de cuentas no oficiales

Para jugar con cuentas no oficiales, asegúrate de tener un cliente de Minecraft modificado que permita la autenticación con cuentas no oficiales.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas agregar mejoras o arreglar problemas, por favor crea un fork del repositorio y envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más información.

## Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio o contactarme directamente.
