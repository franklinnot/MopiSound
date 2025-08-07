<img src="https://raw.githubusercontent.com/franklinnot/MopiSound/refs/heads/main/frontend/public/icon.svg" width="100" height="100" />

## MOPI - Tu Música, Gratis [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/franklinnot/Mopi-Sound)

**MOPI** es una aplicación web que te permite descargar audio de alta calidad desde YouTube y SoundCloud de forma simple y rápida.

👉 **Puedes probarla aquí:** https://mopi-592fa.web.app/

## ✨ Características

- **Soporte multiplataforma**: YouTube y SoundCloud
- **Múltiples calidades**: 128, 192 y 256 kbps
- **Vista previa**: Reproduce el contenido antes de descargar
- **Interfaz moderna**: Diseño limpio y responsivo con React y Tailwind
- **API robusta**: Backend en FastAPI con rate limiting y validación
- **Dockerizado**: Fácil despliegue y desarrollo

## 🚀 Inicio Rápido

### Backend (API)

1. **Requisitos**: Docker y FFmpeg instalados
2. **Iniciar servicios**:
   ```bash
   cd backend
   docker compose up -d
   ```
3. **Verificar**: El servicio estará disponible en `http://localhost:8000`
4. **Documentación**: Accede a `http://localhost:8000/docs` [3](#0-2)

### Frontend

1. **Instalar dependencias**:
   ```bash
   cd frontend
   npm install
   ```
2. **Desarrollo**:
   ```bash
   npm run dev
   ```
3. **Build**:
   ```bash
   npm run build
   ```

## 🛠 Arquitectura

- **Frontend**: React 19 + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + yt-dlp + Redis (opcional)
- **Rate Limiting**: Protección contra abuso con Redis
- **CORS**: Configurado para desarrollo y producción

## 📝 API Endpoints

| Endpoint           | Método | Descripción                  |
| ------------------ | ------ | ---------------------------- |
| `/download-audio/` | POST   | Descarga audio desde URL     |
| `/iframe-sc/`      | POST   | Obtiene iframe de SoundCloud |
| `/docs`            | GET    | Documentación interactiva    |

## ⚙️ Configuración

### Variables de Entorno (Backend)

- `REDIS_HOST`: Host de Redis (default: host.docker.internal)
- `REDIS_PORT`: Puerto de Redis (default: 6379)
- `REDIS_PASSWORD`: Contraseña de Redis
- `REDIS_SSL`: Habilitar SSL (default: True)
- `IFRAME_SC`: API para iframes de SoundCloud

### Rate Limiting

Por defecto: 1 solicitud cada 5 segundos por IP. Configurable via Redis.

## 🐳 Docker

### Solo API (sin Redis)

```bash
docker compose up -d
```

### Con Redis (para rate limiting)

Descomenta las líneas de Redis en `docker-compose.yml` y ejecuta el mismo comando.

## 🔧 Desarrollo

### Comandos Útiles

| Comando                       | Descripción                       |
| ----------------------------- | --------------------------------- |
| `docker compose up -d`        | Iniciar servicios                 |
| `docker compose down`         | Detener servicios                 |
| `docker logs -f cont-apimopi` | Ver logs de la API                |
| `npm run dev`                 | Servidor de desarrollo (Frontend) |
| `npm run lint`                | Verificar código (Frontend)       |

## 📱 Uso

1. Ingresa el link de YouTube o SoundCloud
2. Previsualiza el contenido
3. Personaliza el título y calidad
4. Descarga tu archivo MP3

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**Desarrollado con ❤️ para la comunidad**
