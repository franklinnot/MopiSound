# Configuración del Backend de MOPI

Esta guía te muestra cómo levantar el backend de MOPI de forma rápida y sencilla usando **Docker**. Esto elimina problemas de compatibilidad y facilita el desarrollo.

-----

## 1\. Configuración del Entorno

Antes de empezar, asegúrate de tener **Docker** y **FFmpeg** instalados en tu sistema. El servicio se levanta usando el archivo `docker-compose.yml` que ya se encuentra en el proyecto.

### API

Si solo necesitas el contenedor de la API para el desarrollo, asegúrate de que las líneas relacionadas con `redis` estén comentadas en el `docker-compose.yml`. El servicio se levantará sin Redis, ya que tu código puede manejar esta ausencia.

Para iniciar el servicio en este modo, ejecuta:

```bash
docker compose up -d
```

> Si necesitas utilizar Redis, descomenta las líneas correspondientes en el `docker-compose.yml` y luego ejecuta el mismo comando:


Para verificar que los contenedores estén corriendo, usa:

```bash
docker ps
```

Deberías ver el contenedor `cont-apimopi` y, si lo activaste, también `redis`.

### Acceso al servicio

Una vez que los contenedores estén activos, el servicio estará disponible en `http://localhost:8000` y la documentación de la API en `http://localhost:8000/docs`.

-----

## 2\. Comandos Útiles de Docker

| Comando                                   | Descripción                                             |
| ----------------------------------------- | ------------------------------------------------------- |
| `docker compose up -d`                    | Inicia los servicios definidos en el `docker-compose.yml` |
| `docker compose down`                     | Detiene y elimina los contenedores de los servicios     |
| `docker stop cont-apimopi`                | Detiene el contenedor de la API                         |
| `docker start cont-apimopi`               | Reinicia el contenedor de la API                        |
| `docker logs -f cont-apimopi`             | Muestra los logs en tiempo real del contenedor de la API  |
| `docker build -t iso-apimopi .`           | Construye o reconstruye la imagen del backend           |
| `docker tag iso-apimopi tu-repo/iso-apimopi:latest` | Etiqueta una imagen para subirla a un repositorio |

-----

## 3\. Despliegue

Para un despliegue en producción, debes considerar estos puntos clave:

  * **Variables de Entorno:**
    En caso que querer limitar el número de solicitudes, crea un archivo `.env` basado en `.env.example`. Ahí deberás configurar una URL de Redis.

  * **Cookies:**
    Para procesar videos de YouTube, crea un archivo `cookies.txt` dentro de la carpeta `app`. Para saber cómo obtener las cookies, revisa la [documentación de `yt-dlp`](https://www.google.com/search?q=%5Bhttps://github.com/yt-dlp/yt-dlp/wiki/FAQ%23how-do-i-pass-cookies-to-yt-dlp%5D\(https://github.com/yt-dlp/yt-dlp/wiki/FAQ%23how-do-i-pass-cookies-to-yt-dlp\)).