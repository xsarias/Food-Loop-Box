# Food-Loop-Box

> **Plataforma de Rescate y Distribución de Excedentes Alimentarios**

Proyecto de Construcción de Software que busca reducir el desperdicio de alimentos mediante una plataforma integral que conecta excedentes de restaurantes, supermercados y establecimientos comerciales con clientes interesados en alimentos de calidad a precio social.

**Versión**: 1.0.0  
**Equipo**: Construcción de Software  
**Institución**: Pontificia Universidad Javeriana  
**Fecha**: 2026

---

## Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Requisitos Previos](#requisitos-previos)
4. [Instalación](#instalación)
5. [Configuración](#configuración)
6. [Estructura del Proyecto](#estructura-del-proyecto)
7. [API REST - Documentación Completa](#api-rest---documentación-completa)
8. [Autenticación JWT](#autenticación-jwt)
9. [Guía para el Frontend](#guía-para-el-frontend)
10. [Modelos de Datos](#modelos-de-datos)
11. [Ejemplos de Uso](#ejemplos-de-uso)
12. [Roles y Permisos](#roles-y-permisos)
13. [Troubleshooting](#troubleshooting)

---

## Descripción del Proyecto

### Problema a Resolver
Aproximadamente el 30-40% de alimentos producidos se desperdician globalmente. Restaurantes, supermercados y establecimientos comerciales descartan diariamente alimentos en perfecto estado que podrían beneficiar a personas con recursos limitados.

### Solución
**Food-Loop-Box** es una plataforma que:
- ✅ Permite a aliados comerciales registrar excedentes de alimentos
- ✅ Facilita reservas y compras de productos a precios reducidos
- ✅ Gestiona dispositivos refrigerados inteligentes (Food Loop Box)
- ✅ Proporciona reportes de impacto ambiental y social
- ✅ Crea un ciclo completo de rescate alimentario

### Flujo Principal
```
Restaurante/Aliado         Device Food Loop Box       Cliente
      |                           |                      |
Registra excedentes -----> Almacena productos -----> Busca/Reserva/Compra
      |                           |                      |
Dona o vende        (Control de temperatura)    Retira con código
```

---

## Stack Tecnológico

### Backend
| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **Python** | 3.8+ | Lenguaje principal |
| **Django** | 4.2.0 | Framework web |
| **Django REST Framework** | 3.14.0 | API REST |
| **JWT (SimpleJWT)** | 5.2.2 | Autenticación |
| **PostgreSQL** | 13+ | Base de datos (producción) |
| **SQLite** | - | Base de datos (desarrollo) |
| **Gunicorn** | 20.1.0 | Servidor WSGI |
| **Redis** | 6+ | Cache y Celery broker |
| **Celery** | 5.3.1 | Tareas asincrónicas |

### Herramientas Adicionales
- **django-cors-headers**: Permitir peticiones desde frontend
- **django-filter**: Filtrado avanzado de datos
- **Pillow**: Procesamiento de imágenes
- **python-dotenv**: Gestión de variables de entorno
- **drf-spectacular**: Documentación automática de API

---

## Requisitos Previos

### Software Necesario
```bash
# Windows
- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Git

# Linux/Mac
- Python 3.8 o superior
- pip
- Git
- (Opcional) PostgreSQL para producción
- (Opcional) Redis para caché
```

### Verificar Instalación
```bash
python --version
pip --version
git --version
```

---

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-repo/Food-Loop-Box.git
cd Food-Loop-Box/backend
```

### 2. Crear Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### (opcional) 4. Configurar Variables de Entorno
```bash
# Copiar plantilla
cp .env.example .env

# Editar .env con tus valores
# DEBUG=True
# SECRET_KEY=tu-clave-secreta
# DATABASE_URL=sqlite:///db.sqlite3
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

### 8. Iniciar Servidor
```bash
python manage.py runserver
```

**El servidor estará disponible en**: `http://localhost:8000`

---

## Configuración

### .env - Variables de Entorno

```bash
# Django Settings
DEBUG=True                              # False en producción
SECRET_KEY=django-insecure-tu-clave    # Cambiar en producción
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
# SQLite (desarrollo)
# DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL (producción - descomentar)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=foodloopbox_db
# DB_USER=postgres
# DB_PASSWORD=tu-contraseña
# DB_HOST=localhost
# DB_PORT=5432

# JWT - Duración de Tokens
JWT_ACCESS_TOKEN_LIFETIME=3600         # 1 hora en segundos
JWT_REFRESH_TOKEN_LIFETIME=86400       # 1 día en segundos

# CORS - Orígenes Permitidos (Frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### settings.py - Configuración Principal

Ubicado en `foodloopbox/foodloopbox/settings.py`. Incluye:
- Todas las apps registradas
- Autenticación JWT configurada
- CORS habilitado
- Paginación (20 items por página)
- Filtrado y búsqueda habilitados
- Zona horaria: America/Bogota
- Idioma: Español

---

## Estructura del Proyecto

```
Food-Loop-Box/
│
├── backend/                           # ← Backend Django
│   ├── foodloopbox/                  # Configuración principal
│   │   ├── settings.py               # Configuración de Django
│   │   ├── urls.py                   # Enrutador principal
│   │   ├── asgi.py                   # Servidor ASGI
│   │   └── wsgi.py                   # Servidor WSGI
│   │
│   ├── apps/                         # Aplicaciones del negocio
│   │   ├── authentication/           # 🔐 Usuarios y autenticación
│   │   ├── core/                     # 🏢 Ubicaciones y dispositivos
│   │   ├── products/                 # 🍔 Gestión de productos
│   │   ├── transactions/             # 💳 Compras y reservas
│   │   └── analytics/                # 📊 Reportes y estadísticas
│   │
│   ├── manage.py                     # Herramienta CLI
│   ├── requirements.txt              # Dependencias Python
│   ├── init_database.py              # Script datos de prueba
│   └── .env.example                  # Plantilla de variables
│
├── .gitignore                         # Archivos a ignorar en Git
└── README.md                          # Este archivo
```

### Descripción de Apps

#### apps/authentication/ - Autenticación y Usuarios
- Gestión de usuarios con roles
- Autenticación JWT
- Registro y login
- Cambio de contraseña
- Registro de accesos (auditoría)
- Permisos personalizados

#### apps/core/ - Ubicaciones y Dispositivos
- Ubicaciones (restaurantes, supermercados, centros comerciales)
- Aliados de negocio (proveedores de alimentos)
- Dispositivos Food Loop Box (máquinas refrigeradas)
- Compartimentos dentro de dispositivos
- Estadísticas por ubicación

#### apps/products/ - Gestión de Productos
- Categorías de alimentos
- Registro de productos
- Control de temperatura
- Fechas de vencimiento
- Precios y descuentos
- Imágenes de productos
- Estado de disponibilidad

#### apps/transactions/ - Compras y Reservas
- Transacciones/compras de productos
- Métodos de pago
- Códigos de retiro
- Reservas de productos
- Tracking de recolección

#### apps/analytics/ - Reportes y Estadísticas
- Estadísticas diarias agregadas
- Métricas por ubicación
- Métricas por aliado
- Impacto ambiental (CO2, agua ahorrada)
- Vidas impactadas

---

## API REST - Documentación Completa

### Base URL
```
http://localhost:8000/api/v1/
```

### Autenticación JWT

Todos los endpoints (excepto login/registro) requieren autenticación con JWT.

#### Headers Requeridos
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## AUTENTICACIÓN - `/auth/`

### 1. **POST** - Obtener Tokens JWT
```http
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "usuario@example.com",
  "password": "contraseña123"
}
```

**Respuesta (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "usuario@example.com",
    "email": "usuario@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "customer",
    "is_verified": true,
    "phone": "3001234567"
  }
}
```

**Códigos de Error:**
- `401 Unauthorized`: Credenciales inválidas

---

### 2. **POST** - Refrescar Token de Acceso
```http
POST /api/v1/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Respuesta (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 3. **POST** - Registrar Nuevo Usuario
```http
POST /api/v1/auth/users/
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "nuevo@example.com",
  "password": "Password123!",
  "password_confirm": "Password123!",
  "first_name": "María",
  "last_name": "García",
  "phone": "3109876543",
  "document_type": "cc",
  "document_id": "1234567890",
  "role": "customer"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 2,
  "username": "nuevo_usuario",
  "email": "nuevo@example.com",
  "first_name": "María",
  "last_name": "García",
  "phone": "3109876543",
  "role": "customer",
  "is_verified": false,
  "created_at": "2026-04-25T10:30:00Z"
}
```

---

### 4. **GET** - Obtener Perfil del Usuario Actual
```http
GET /api/v1/auth/users/me/
Authorization: Bearer <access_token>
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "username": "usuario@example.com",
  "email": "usuario@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "role": "customer",
  "is_verified": true,
  "phone": "3001234567",
  "document_id": "1023456789",
  "profile_picture": "https://example.com/media/profiles/user_1.jpg",
  "custom_permissions": [
    {
      "id": 1,
      "permission_name": "ver_productos",
      "category": "products",
      "can_view": true,
      "can_edit": false,
      "can_delete": false,
      "can_export": false
    }
  ]
}
```

---

### 5. **PUT** - Actualizar Perfil
```http
PUT /api/v1/auth/users/me/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Juan",
  "last_name": "Pérez López",
  "phone": "3201234567"
}
```

**Respuesta (200 OK):** Perfil actualizado

---

### 6. **POST** - Cambiar Contraseña
```http
POST /api/v1/auth/users/change_password/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "contraseña_actual",
  "new_password": "nueva_contraseña",
  "new_password_confirm": "nueva_contraseña"
}
```

---

## CORE (Ubicaciones, Aliados, Dispositivos) - `/core/`

### 7. **GET** - Listar Ubicaciones
```http
GET /api/v1/core/locations/
Authorization: Bearer <access_token>
```

**Query Parameters:**
```
?location_type=restaurant        # Filtro: tipo de ubicación
?city=Bogotá                     # Filtro: ciudad
?is_active=true                  # Filtro: activa/inactiva
?search=centro                   # Búsqueda: nombre o dirección
?ordering=-created_at            # Ordenar: -created_at (desc), name (asc)
?page=1                          # Paginación
```

**Respuesta (200 OK):**
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/v1/core/locations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Centro Comercial Hayuelos",
      "location_type": "commercial_center",
      "address": "Carrera 81 #10-10",
      "city": "Bogotá",
      "postal_code": "110811",
      "latitude": 4.635,
      "longitude": -74.133,
      "phone": "(1) 6237700",
      "email": "info@hayuelos.com",
      "is_active": true,
      "created_at": "2026-04-20T08:00:00Z",
      "updated_at": "2026-04-25T10:30:00Z"
    }
  ]
}
```

---

### 8. **POST** - Crear Nueva Ubicación (Admin)
```http
POST /api/v1/core/locations/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Nuevo Restaurante",
  "location_type": "restaurant",
  "address": "Carrera 5 #20-30",
  "city": "Medellín",
  "postal_code": "050001",
  "latitude": 6.2442,
  "longitude": -75.5812,
  "phone": "(4) 5551234",
  "email": "contact@restaurant.com",
  "is_active": true
}
```

---

### 9. **GET** - Estadísticas de Ubicación
```http
GET /api/v1/core/locations/{id}/statistics/
Authorization: Bearer <access_token>
```

**Respuesta (200 OK):**
```json
{
  "location_id": 1,
  "location_name": "Centro Comercial Hayuelos",
  "total_partners": 5,
  "total_products": 42,
  "total_revenue": "2500.50",
  "active_devices": 3,
  "total_transactions": 89
}
```

---

### 10. **GET** - Listar Aliados de Negocio
```http
GET /api/v1/core/partners/
Authorization: Bearer <access_token>

?location={location_id}          # Filtro: por ubicación
?partner_type=restaurant         # Filtro: tipo de aliado
?is_active=true                  # Filtro: activo
?search=colombiano               # Búsqueda
```

**Respuesta (200 OK):**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "name": "Restaurante Colombiano",
      "partner_type": "restaurant",
      "location": 1,
      "location_name": "Centro Comercial Hayuelos",
      "contact_person": "Carlos García",
      "email": "carlos@colombiano.com",
      "phone": "3001234567",
      "business_id": "BUS001",
      "is_active": true,
      "created_at": "2026-04-20T08:00:00Z"
    }
  ]
}
```

---

### 11. **GET** - Listar Dispositivos (Food Loop Box)
```http
GET /api/v1/core/devices/
Authorization: Bearer <access_token>

?status=active                   # Filtro: estado
?location={location_id}          # Filtro: por ubicación
?is_online=true                  # Filtro: en línea
```

**Respuesta (200 OK):**
```json
{
  "count": 12,
  "results": [
    {
      "id": 1,
      "device_id": "FLB-001-HY",
      "location": 1,
      "location_name": "Centro Comercial Hayuelos",
      "status": "active",
      "total_compartments": 8,
      "available_compartments": 5,
      "current_temperature": 3.5,
      "refrigeration_power": 1.0,
      "is_online": true,
      "last_sync": "2026-04-25T10:25:00Z",
      "created_at": "2026-04-15T09:00:00Z"
    }
  ]
}
```

---

### 12. **GET** - Listar Compartimentos
```http
GET /api/v1/core/compartments/
Authorization: Bearer <access_token>

?device={device_id}              # Filtro: por dispositivo
?status=available                # Filtro: estado
```

**Respuesta (200 OK):**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "device": 1,
      "device_id": "FLB-001-HY",
      "compartment_number": 1,
      "status": "available",
      "current_temperature": 3.5,
      "temperature_setpoint": 4.0,
      "is_locked": false,
      "created_at": "2026-04-15T09:00:00Z"
    }
  ]
}
```

---

## PRODUCTOS - `/products/`

### 13. **GET** - Listar Categorías de Alimentos
```http
GET /api/v1/products/categories/
Authorization: Bearer <access_token>

?search=carne                    # Búsqueda
?is_active=true                  # Filtro: activa
```

**Respuesta (200 OK):**
```json
{
  "count": 12,
  "results": [
    {
      "id": 1,
      "name": "Carnes",
      "description": "Productos cárnicos diversos",
      "is_active": true,
      "created_at": "2026-04-15T09:00:00Z"
    },
    {
      "id": 2,
      "name": "Bebidas",
      "description": "Bebidas y refrescos",
      "is_active": true,
      "created_at": "2026-04-15T09:00:00Z"
    }
  ]
}
```

---

### 14. **GET** - Listar Productos Disponibles
```http
GET /api/v1/products/
Authorization: Bearer <access_token>

?status=available                # Filtro: disponible
?product_type=sale               # Filtro: venta/donación
?category={category_id}          # Filtro: categoría
?provider={partner_id}           # Filtro: por proveedor
?is_reserved=false               # Filtro: no reservado
?search=pollo                    # Búsqueda
?ordering=-expiration_date       # Ordenar por fecha vencimiento
?page=1                          # Paginación
```

**Respuesta (200 OK):**
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/v1/products/?page=2",
  "results": [
    {
      "id": 15,
      "name": "Pechuga de Pollo Fresca",
      "category": 1,
      "category_name": "Carnes",
      "description": "Pechuga de pollo premium, 2kg",
      "provider": 1,
      "provider_name": "Restaurante Colombiano",
      "registered_by": 3,
      "registered_by_username": "carlos@colombiano.com",
      "status": "available",
      "product_type": "sale",
      "quantity": 2.0,
      "unit": "kg",
      "original_price": "45000.00",
      "discounted_price": "22500.00",
      "discount_percentage": 50.0,
      "final_price": "22500.00",
      "required_temperature": 2.0,
      "temperature_min": 0.0,
      "temperature_max": 4.0,
      "registration_date": "2026-04-25T09:00:00Z",
      "expiration_date": "2026-04-26T18:00:00Z",
      "compartment": 1,
      "compartment_number": 1,
      "is_reserved": false,
      "image": "https://example.com/media/products/pollo_15.jpg",
      "notes": "Producto de excelente calidad",
      "is_expired_status": false,
      "created_at": "2026-04-25T09:00:00Z"
    }
  ]
}
```

---

### 15. **POST** - Registrar Nuevo Producto
```http
POST /api/v1/products/
Authorization: Bearer <partner_token>
Content-Type: multipart/form-data

{
  "name": "Ensalada César Premium",
  "category": 3,
  "description": "Ensalada fresca con pollo y aderezo casero",
  "provider": 1,
  "product_type": "sale",
  "quantity": 3.5,
  "unit": "kg",
  "original_price": "35000",
  "discounted_price": "17500",
  "discount_percentage": 50,
  "required_temperature": 4.0,
  "temperature_min": 2.0,
  "temperature_max": 6.0,
  "expiration_date": "2026-04-26T20:00:00Z",
  "compartment": 2,
  "notes": "Producto vegano",
  "image": <archivo.jpg>
}
```

**Respuesta (201 Created):** Producto creado

---

### 16. **GET** - Detalles de Producto
```http
GET /api/v1/products/{id}/
Authorization: Bearer <access_token>
```

---

### 17. **PUT** - Actualizar Producto
```http
PUT /api/v1/products/{id}/
Authorization: Bearer <partner_token>
Content-Type: application/json

{
  "quantity": 2.0,
  "status": "reserved"
}
```

---

## TRANSACCIONES - `/transactions/`

### 18. **POST** - Crear Compra (Transacción)
```http
POST /api/v1/transactions/
Authorization: Bearer <customer_token>
Content-Type: application/json

{
  "product": 15,
  "payment_method": "card",
  "notes": "Compra desde mobile"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 42,
  "transaction_id": "TRX-2026042501-001",
  "buyer": 2,
  "buyer_username": "juan@example.com",
  "product": 15,
  "product_name": "Pechuga de Pollo Fresca",
  "amount": "22500.00",
  "currency": "COP",
  "payment_method": "card",
  "status": "completed",
  "withdrawal_code": "ABC123XYZ",
  "withdrawal_code_used": false,
  "withdrawal_date": null,
  "created_at": "2026-04-25T10:30:00Z"
}
```

---

### 19. **GET** - Listar Compras del Usuario
```http
GET /api/v1/transactions/
Authorization: Bearer <access_token>

?status=completed                # Filtro: estado
?payment_method=card             # Filtro: método pago
?ordering=-created_at            # Ordenar
```

---

### 20. **POST** - Hacer Reserva
```http
POST /api/v1/reservations/
Authorization: Bearer <customer_token>
Content-Type: application/json

{
  "product": 15,
  "expiration_date": "2026-04-26T18:00:00Z"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 8,
  "user": 2,
  "product": 15,
  "status": "active",
  "reservation_date": "2026-04-25T10:30:00Z",
  "expiration_date": "2026-04-26T18:00:00Z",
  "collection_date": null
}
```

---

## ANALYTICS - `/analytics/`

### 21. **GET** - Estadísticas Diarias
```http
GET /api/v1/analytics/daily/
Authorization: Bearer <admin_token>

?date=2026-04-25                 # Filtro: fecha específica
?ordering=-date                  # Ordenar
```

**Respuesta (200 OK):**
```json
{
  "count": 30,
  "results": [
    {
      "id": 1,
      "date": "2026-04-25",
      "total_products_registered": 28,
      "total_products_donated": 8,
      "total_products_sold": 15,
      "total_products_expired": 2,
      "total_weight_rescued": 125.5,
      "total_weight_donated": 45.2,
      "total_weight_sold": 78.3,
      "total_transactions": 15,
      "total_amount": "425000.00",
      "new_users": 5,
      "active_users": 189,
      "created_at": "2026-04-25T23:59:00Z"
    }
  ]
}
```

---

### 22. **GET** - Métricas por Ubicación
```http
GET /api/v1/analytics/locations/
Authorization: Bearer <admin_token>
```

**Respuesta (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "location": 1,
      "location_name": "Centro Comercial Hayuelos",
      "total_products_handled": 542,
      "total_weight_rescued": 2854.5,
      "average_products_per_day": 18.1,
      "total_revenue": "1250000.00",
      "average_transaction_value": "14045.45",
      "unique_customers": 89,
      "repeat_customers": 34,
      "estimated_co2_saved": 285.45,
      "estimated_water_saved": 5700,
      "last_updated": "2026-04-25T10:30:00Z"
    }
  ]
}
```

---

### 23. **GET** - Métricas por Aliado
```http
GET /api/v1/analytics/partners/
Authorization: Bearer <admin_token>
```

**Respuesta (200 OK):**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "partner": 1,
      "partner_name": "Restaurante Colombiano",
      "total_products_donated": 125,
      "total_weight_donated": 456.8,
      "average_donation_per_day": 4.2,
      "total_products_sold": 315,
      "total_revenue_from_sales": "850000.00",
      "lives_impacted": 280,
      "total_waste_prevented": 672.0,
      "last_updated": "2026-04-25T10:30:00Z"
    }
  ]
}
```

---

## Guía para el Frontend

### 1. Iniciar Sesión y Guardar Tokens

```javascript
// 1. Login
async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/v1/auth/token/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  
  // Guardar tokens en localStorage
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
  localStorage.setItem('user', JSON.stringify(data.user));
  
  return data;
}
```

### 2. Realizar Peticiones Autenticadas

```javascript
// Función helper para peticiones con JWT
async function fetchAPI(endpoint, options = {}) {
  const token = localStorage.getItem('access_token');
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    ...options.headers
  };
  
  const response = await fetch(
    `http://localhost:8000/api/v1${endpoint}`,
    {
      ...options,
      headers
    }
  );
  
  // Si token expiró, refrescar
  if (response.status === 401) {
    await refreshAccessToken();
    return fetchAPI(endpoint, options); // Reintentar
  }
  
  return response.json();
}
```

### 3. Refrescar Token Expirado

```javascript
async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  const response = await fetch('http://localhost:8000/api/v1/auth/token/refresh/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh: refreshToken })
  });
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access);
}
```

### 4. Ejemplos de Uso

```javascript
// Obtener productos disponibles
async function getProducts() {
  return fetchAPI('/products/?status=available&product_type=sale');
}

// Crear compra
async function buyProduct(productId, paymentMethod) {
  return fetchAPI('/transactions/', {
    method: 'POST',
    body: JSON.stringify({
      product: productId,
      payment_method: paymentMethod
    })
  });
}

// Hacer reserva
async function reserveProduct(productId) {
  return fetchAPI('/reservations/', {
    method: 'POST',
    body: JSON.stringify({
      product: productId,
      expiration_date: new Date(Date.now() + 48 * 60 * 60 * 1000).toISOString()
    })
  });
}

// Obtener perfil
async function getProfile() {
  return fetchAPI('/auth/users/me/');
}
```

### 5. Configuración CORS

El backend ya está configurado para aceptar peticiones desde:
- `http://localhost:3000` (Frontend local)
- `http://127.0.0.1:3000`

**Si necesitas agregar más orígenes**, edita `.env`:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://otra-url.com
```

---

## Modelos de Datos

### User (Usuario)
```
- id: Identificador único
- username: Nombre de usuario único
- email: Email único
- password: Contraseña encriptada
- first_name: Nombre
- last_name: Apellido
- phone: Teléfono
- document_type: cc/passport
- document_id: Número de documento
- role: admin/partner/customer/driver/support
- is_verified: Verificado
- profile_picture: Imagen de perfil
- is_active: Usuario activo
- created_at: Fecha de creación
- updated_at: Fecha última actualización
```

### Product (Producto)
```
- id: Identificador
- name: Nombre del producto
- category: ForeignKey → FoodCategory
- description: Descripción
- provider: ForeignKey → BusinessPartner
- registered_by: ForeignKey → User
- status: available/reserved/collected/expired/removed
- product_type: donation/sale
- quantity: Cantidad disponible
- unit: kg/g/L/ml/unit
- original_price: Precio original
- discounted_price: Precio con descuento
- discount_percentage: % descuento (0-100)
- final_price: Calculado automáticamente
- required_temperature: Temp. ideal (°C)
- temperature_min: Temp. mínima
- temperature_max: Temp. máxima
- registration_date: Cuándo se registró
- expiration_date: Fecha de vencimiento
- compartment: ForeignKey → Compartment
- is_reserved: ¿Está reservado?
- reserved_by: ForeignKey → User
- image: Imagen del producto
- created_at, updated_at: Timestamps
```

### Transaction (Compra)
```
- id: Identificador
- transaction_id: ID único (TRX-YYYYMMDDXX)
- buyer: ForeignKey → User
- product: ForeignKey → Product
- amount: Monto pagado
- currency: Moneda (COP)
- payment_method: cash/card/mobile_payment/transfer
- status: pending/completed/failed/cancelled
- withdrawal_code: Código para retirar producto
- withdrawal_code_used: ¿Ya se retiró?
- withdrawal_date: Fecha de retiro
- created_at, updated_at: Timestamps
```

### Reservation (Reserva)
```
- id: Identificador
- user: ForeignKey → User
- product: ForeignKey → Product
- status: active/completed/cancelled/expired
- reservation_date: Cuándo se hizo
- expiration_date: Hasta cuándo está válida
- collection_date: Cuándo se recolectó
- created_at, updated_at: Timestamps
```

### SmartDevice (Dispositivo Food Loop Box)
```
- id: Identificador
- device_id: ID único del dispositivo (FLB-XXX-YYY)
- location: OneToOne → Location
- status: active/maintenance/inactive
- total_compartments: Compartimentos totales
- available_compartments: Disponibles ahora
- current_temperature: Temperatura actual (°C)
- refrigeration_power: Potencia de refrigeración
- is_online: ¿En línea?
- last_sync: Último sincronización
- last_maintenance: Último mantenimiento
- created_at, updated_at: Timestamps
```

---

## Ejemplos de Uso - cURL

### Obtener Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario@example.com",
    "password": "password123"
  }'
```

### Listar Productos
```bash
curl -X GET "http://localhost:8000/api/v1/products/?status=available" \
  -H "Authorization: Bearer <your_token>"
```

### Crear Compra
```bash
curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 15,
    "payment_method": "card"
  }'
```

---

## Roles y Permisos

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **admin** | Administrador del sistema | Todo: crear/editar/eliminar cualquier cosa |
| **partner** | Aliado (restaurante, supermercado) | Registrar productos, ver sus ventas |
| **customer** | Cliente | Ver productos, hacer reservas, comprar |
| **driver** | Conductor de recolección | Recolectar productos |
| **support** | Soporte técnico | Ver reportes, asistencia |

**Nota:** Los permisos están implementados en cada ViewSet con decoradores `@permission_classes`.

---

## Troubleshooting

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solución:** Edita `.env`:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Reinicia el servidor.

---

### Error: "Invalid token" o "Token is blacklisted"

**Solución:**
1. Obtén un nuevo token con login
2. Verifica que el token no esté expirado (duración: 1 hora)
3. Usa `/auth/token/refresh/` para refrescar

---

### Error: "User matching query does not exist"

**Solución:** Asegúrate de que el usuario existe:
```bash
python manage.py shell
>>> from apps.authentication.models import User
>>> User.objects.all()  # Ver todos los usuarios
```

---

### Database Error: "no such table"

**Solución:** Ejecuta migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Contacto y Soporte

- **Email**: equipo@foodloopbox.com
- **Documentación API**: Accesible en `/admin` con credenciales
- **Issues**: Reportar en el repositorio

---

## Licencia

Este proyecto es propiedad de Pontificia Universidad Javeriana - Programa de Construcción de Software.

---

**Última actualización**: 25 de abril de 2026  
**Versión**: 1.0.0  
**Estado**: Producción
