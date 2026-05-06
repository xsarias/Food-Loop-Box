# Backend Food Loop Box - Django REST Framework

## 📖 Descripción

Backend del proyecto Food Loop Box desarrollado en **Django REST Framework**. Este proyecto implementa una API completa (RESTful) para gestionar excedentes de alimentos en centros comerciales, restaurantes y dispositivos inteligentes.

**Base URL**: `http://localhost:8000/api/v1/`

---

## 📁 Estructura del Proyecto

```
backend/
├── foodloopbox/                  # 🔧 Configuración principal
│   ├── settings.py              # Configuración de Django
│   ├── urls.py                  # Enrutamiento principal
│   ├── asgi.py                  # Servidor ASGI
│   └── wsgi.py                  # Servidor WSGI
│
├── apps/                         # 📦 Aplicaciones del negocio
│   ├── authentication/           # 🔐 Usuarios y autenticación
│   │   ├── models.py           # User, AccessLog, UserPermission
│   │   ├── serializers.py      # Serializadores
│   │   ├── viewsets.py         # Vistas y endpoints
│   │   ├── urls.py             # Rutas
│   │   └── migrations/
│   │
│   ├── core/                     # 🏢 Ubicaciones y dispositivos
│   │   ├── models.py           # Location, Partner, Device, Compartment
│   │   ├── serializers.py
│   │   ├── viewsets.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── products/                 # 🍔 Gestión de productos
│   │   ├── models.py           # FoodCategory, Product
│   │   ├── serializers.py
│   │   ├── viewsets.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── transactions/             # 💳 Compras y reservas
│   │   ├── models.py           # Transaction, Reservation, Collection
│   │   ├── serializers.py
│   │   ├── viewsets.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   └── analytics/                # 📊 Reportes y estadísticas
│       ├── models.py           # DailyStatistics, LocationMetrics
│       ├── serializers.py
│       ├── viewsets.py
│       ├── urls.py
│       └── migrations/
│
├── manage.py                     # CLI de Django
├── requirements.txt              # Dependencias Python
├── init_database.py             # Script para datos de prueba
├── .env.example                 # Plantilla de variables de entorno
└── BACKEND.md                   # Este archivo
```

---

## ⚙️ Requisitos Previos

### Software Necesario
```bash
# Todos los sistemas
- Python 3.8+
- pip (gestor de paquetes Python)
- Git

# Linux/Mac (opcional para producción)
- PostgreSQL 13+
- Redis 6+
```

### Verificar Instalación
```bash
python --version
pip --version
git --version
```

---

## 🚀 Instalación y Setup

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-repo/Food-Loop-Box.git
cd Food-Loop-Box/backend
```

### 2. Crear Ambiente Virtual
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Copiar plantilla
cp .env.example .env

# Editar .env con tus valores (opcional para desarrollo)
nano .env  # o usa tu editor preferido
```

### 5. Ejecutar Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear Superusuario (Admin)
```bash
python manage.py createsuperuser
# Ingresa: username, email, contraseña
```

### 7. (Opcional) Cargar Datos de Prueba
```bash
python manage.py shell < init_database.py
```

### 8. Iniciar Servidor de Desarrollo
```bash
python manage.py runserver
```

**El servidor estará disponible en**: `http://localhost:8000`  
**Admin panel**: `http://localhost:8000/admin/`  
**API docs**: `http://localhost:8000/api/v1/schema/` (si drf-spectacular está instalado)

---

## 🔧 Configuración

### .env - Variables de Entorno

```bash
# ========== DJANGO SETTINGS ==========
DEBUG=True                              # False en producción
SECRET_KEY=django-insecure-tu-clave    # Cambiar en producción ⚠️
ALLOWED_HOSTS=localhost,127.0.0.1

# ========== DATABASE ==========
# SQLite (desarrollo - comentar para usar PostgreSQL)
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL (producción - descomentar y configurar)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=foodloopbox_db
# DB_USER=postgres
# DB_PASSWORD=tu-contraseña-segura
# DB_HOST=localhost
# DB_PORT=5432

# ========== JWT (JSON Web Tokens) ==========
JWT_ACCESS_TOKEN_LIFETIME=3600         # 1 hora en segundos
JWT_REFRESH_TOKEN_LIFETIME=86400       # 1 día en segundos
JWT_ALGORITHM=HS256

# ========== CORS (Frontend) ==========
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# ========== CACHE (opcional) ==========
# REDIS_URL=redis://localhost:6379/0

# ========== EMAIL (opcional) ==========
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=tu-email@gmail.com
# EMAIL_HOST_PASSWORD=tu-contraseña-app
# EMAIL_USE_TLS=True
```

### settings.py - Configuración Principal

Ubicado en `foodloopbox/settings.py`. Configuraciones automáticas:
- ✅ Todas las apps registradas
- ✅ Autenticación JWT configurada
- ✅ CORS habilitado para frontend
- ✅ Paginación: 20 items por página
- ✅ Filtrado y búsqueda habilitados
- ✅ Zona horaria: `America/Bogota`
- ✅ Idioma: `es-ES` (Español)

---

## 📡 API Endpoints

### Autenticación
- `POST /api/v1/auth/token/` - Obtener token JWT
- `POST /api/v1/auth/token/refresh/` - Refrescar token
- `POST /api/v1/auth/login/` - Login (retorna tokens y datos de usuario)
- `POST /api/v1/auth/logout/` - Logout
- `POST /api/v1/auth/users/` - Registrar nuevo usuario
- `GET /api/v1/auth/users/me/` - Perfil del usuario actual
- `POST /api/v1/auth/users/change_password/` - Cambiar contraseña

### Ubicaciones (Core)
- `GET /api/v1/core/locations/` - Listar ubicaciones
- `POST /api/v1/core/locations/` - Crear ubicación
- `GET /api/v1/core/locations/{id}/` - Detalles de ubicación
- `PUT /api/v1/core/locations/{id}/` - Actualizar ubicación
- `DELETE /api/v1/core/locations/{id}/` - Eliminar ubicación
- `GET /api/v1/core/locations/{id}/statistics/` - Estadísticas de ubicación

### Aliados (Partners)
- `GET /api/v1/core/partners/` - Listar aliados
- `POST /api/v1/core/partners/` - Crear aliado
- `GET /api/v1/core/partners/{id}/` - Detalles del aliado
- `GET /api/v1/core/partners/{id}/products/` - Productos del aliado

### Dispositivos Inteligentes
- `GET /api/v1/core/devices/` - Listar dispositivos
- `POST /api/v1/core/devices/` - Crear dispositivo
- `GET /api/v1/core/devices/{id}/` - Detalles del dispositivo
- `POST /api/v1/core/devices/{id}/sync_status/` - Sincronizar estado
- `POST /api/v1/core/devices/{id}/toggle_maintenance/` - Alternar mantenimiento
- `GET /api/v1/core/devices/{id}/compartments_status/` - Estado de compartimientos

### Productos
- `GET /api/v1/products/products/` - Listar productos
- `POST /api/v1/products/products/` - Registrar producto
- `GET /api/v1/products/products/{id}/` - Detalles del producto
- `GET /api/v1/products/products/available/` - Productos disponibles
- `GET /api/v1/products/products/expiring_soon/` - Próximos a vencer
- `POST /api/v1/products/products/{id}/reserve/` - Reservar producto
- `POST /api/v1/products/products/{id}/mark_collected/` - Marcar como recolectado

### Transacciones
- `GET /api/v1/transactions/transactions/` - Listar transacciones
- `POST /api/v1/transactions/transactions/` - Crear transacción
- `GET /api/v1/transactions/transactions/my_transactions/` - Mis transacciones
- `POST /api/v1/transactions/transactions/{id}/mark_completed/` - Marcar como completada

### Reservas
- `GET /api/v1/transactions/reservations/` - Listar reservas
- `POST /api/v1/transactions/reservations/` - Crear reserva
- `GET /api/v1/transactions/reservations/my_reservations/` - Mis reservas
- `POST /api/v1/transactions/reservations/{id}/cancel/` - Cancelar reserva

### Análisis
- `GET /api/v1/analytics/daily-statistics/today/` - Estadísticas de hoy
- `GET /api/v1/analytics/daily-statistics/week_summary/` - Resumen semanal
- `GET /api/v1/analytics/dashboard/overview/` - Panel de control general
- `GET /api/v1/analytics/location-metrics/top_locations/` - Mejores ubicaciones
- `GET /api/v1/analytics/partner-metrics/top_partners/` - Mejores aliados
- `GET /api/v1/analytics/environmental-impact/latest/` - Último reporte de impacto

## Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación. 

### Obtener tokens

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "contraseña"}'
```

Respuesta:
```json
{
  "detail": "Login exitoso",
  "user": {...},
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Usar token en requests

Incluir el token en el header `Authorization`:

```bash
curl -H "Authorization: Bearer <access_token>" \
  http://localhost:8000/api/v1/core/locations/
```

## Admin Panel

Acceder a http://localhost:8000/admin con el superusuario creado.

## Modelos principales

### Core
- **Location**: Ubicaciones donde se instalan los dispositivos
- **BusinessPartner**: Aliados que aportan excedentes
- **SmartDevice**: Dispositivos inteligentes (máquinas)
- **Compartment**: Compartimientos dentro de cada dispositivo

### Authentication
- **User**: Modelo de usuario personalizado
- **AccessLog**: Auditoría de accesos
- **UserPermission**: Permisos personalizados

### Products
- **FoodCategory**: Categorías de alimentos
- **Product**: Productos disponibles para donación o venta

### Transactions
- **Transaction**: Transacciones de compra
- **Reservation**: Reservas de productos
- **Collection**: Recolecciones
- **DeviceInteraction**: Interacciones con dispositivos

### Analytics
- **DailyStatistics**: Estadísticas diarias
- **LocationMetrics**: Métricas por ubicación
- **PartnerMetrics**: Métricas por aliado
- **EnvironmentalImpact**: Impacto ambiental
- **UserActivityReport**: Reportes de actividad de usuarios

## Desarrollo

### Crear nuevos serializers
Los serializers están en `apps/{app_name}/serializers.py`

### Crear nuevos viewsets
Los viewsets (controllers) están en `apps/{app_name}/viewsets.py`

### Crear migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## Testing

```bash
python manage.py test
```

## Despliegue

Para producción:

1. Cambiar `DEBUG=False` en settings.py
2. Cambiar `SECRET_KEY` a una clave segura
3. Usar una base de datos PostgreSQL
4. Usar Gunicorn como servidor WSGI
5. Configurar CORS adecuadamente
6. Usar HTTPS

Ejemplo con Gunicorn:
```bash
gunicorn foodloopbox.wsgi:application --bind 0.0.0.0:8000
```

## Licencia

Proyecto educativo - Universidad Distrital Francisco José de Caldas

## Autor

Desarrollado para el curso de Construcción de Software
