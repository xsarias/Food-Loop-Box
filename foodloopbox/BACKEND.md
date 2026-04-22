# Backend Food Loop Box - Django

## Descripción

Backend del proyecto Food Loop Box desarrollado en Django REST Framework. Este proyecto implementa una API completa para gestionar excedentes de alimentos en centros comerciales y restaurantes.

## Estructura del Proyecto

```
foodloopbox/
├── foodloopbox/          # Configuración principal del proyecto
├── apps/
│   ├── core/             # Ubicaciones, aliados, dispositivos inteligentes
│   ├── authentication/   # Autenticación y gestión de usuarios
│   ├── products/         # Gestión de productos
│   ├── transactions/     # Transacciones, reservas, recolecciones
│   └── analytics/        # Reportes y análisis
├── manage.py
└── requirements.txt
```

## Instalación

### Requisitos previos
- Python 3.8+
- pip
- Virtual environment

### Pasos de instalación

1. **Clonar el repositorio**
```bash
cd foodloopbox
```

2. **Crear un ambiente virtual**
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
```

5. **Ejecutar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

El servidor estará disponible en: http://localhost:8000

## API Endpoints

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
