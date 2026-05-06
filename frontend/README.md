# Frontend Food Loop Box - React + Vite

## 📖 Descripción

Frontend del proyecto Food Loop Box desarrollado con **React 18** y **Vite**. Interfaz moderna y responsiva para gestionar la plataforma de rescate y distribución de excedentes alimentarios.

---

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **React** | 18+ | Librería UI |
| **Vite** | 5.0+ | Build tool y dev server |
| **JavaScript** | ES6+ | Lenguaje principal |
| **CSS** | 3 | Estilos |

### Herramientas Adicionales
- **ESLint**: Análisis de código
- **Axios** (recomendado): Cliente HTTP
- **React Router** (recomendado): Navegación SPA

---

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/              # Componentes reutilizables
│   ├── pages/                   # Páginas/vistas principales
│   ├── services/                # Llamadas a API
│   ├── hooks/                   # Custom hooks
│   ├── context/                 # Context API (estado global)
│   ├── utils/                   # Funciones auxiliares
│   ├── assets/                  # Imágenes y recursos
│   ├── App.jsx                  # Componente raíz
│   ├── main.jsx                 # Entry point
│   └── index.css                # Estilos globales
│
├── public/                       # Archivos públicos estáticos
├── .eslintrc.js                 # Configuración de ESLint
├── vite.config.js               # Configuración de Vite
├── package.json                 # Dependencias y scripts
├── package-lock.json
└── README.md                     # Este archivo
```

---

## ⚙️ Requisitos Previos

### Software Necesario
```bash
- Node.js 16+ (incluye npm)
- Git
```

### Verificar Instalación
```bash
node --version
npm --version
git --version
```

---

## 🚀 Instalación y Setup

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-repo/Food-Loop-Box.git
cd Food-Loop-Box/frontend
```

### 2. Instalar Dependencias
```bash
npm install
```

### 3. Crear Archivo de Configuración (opcional)
```bash
# Crear archivo .env
cp .env.example .env
```

### .env - Variables de Entorno

```bash
# ========== API BACKEND ==========
VITE_API_BASE_URL=http://localhost:8000/api/v1/

# ========== CONFIGURACIÓN APP ==========
VITE_APP_NAME=Food Loop Box
VITE_APP_VERSION=1.0.0

# ========== FEATURES (optional) ==========
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_NOTIFICATIONS=true
```

### 4. Iniciar Servidor de Desarrollo
```bash
npm run dev
```

**La aplicación estará disponible en**: `http://localhost:5173`

---

## 📦 Scripts Disponibles

```bash
# Iniciar servidor de desarrollo con HMR
npm run dev

# Construir para producción (optimizado)
npm run build

# Previsualizar build de producción localmente
npm run preview

# Ejecutar ESLint para analizar código
npm run lint

# Corregir automáticamente problemas de linting
npm run lint:fix
```




## 🐛 Troubleshooting

### Error: "Cannot find module 'react'"
```bash
npm install
```

### CORS error al conectar con backend
- Verificar que el backend está corriendo en `http://localhost:8000`
- Revisar `VITE_API_BASE_URL` en `.env`
- Asegurar que `CORS_ALLOWED_ORIGINS` en backend incluya `http://localhost:5173`

### HMR (Hot Module Replacement) no funciona
```bash
# Reiniciar servidor Vite
npm run dev
```

### Build falla
```bash
# Limpiar y reinstalar
rm -rf node_modules package-lock.json
npm install
npm run build
```


### Actualizar Dependencias
```bash
npm outdated          # Ver paquetes desactualizados
npm update            # Actualizar paquetes
npm audit fix         # Arreglar vulnerabilidades conocidas
```

---

## 📚 Recursos Útiles

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Axios Documentation](https://axios-http.com)
- [React Router](https://reactrouter.com)
- [MDN Web Docs](https://developer.mozilla.org)

---

## 🤝 Contribuciones

Este es un proyecto académico de la Universidad Distrital Francisco José de Caldas.

---

## 📝 Licencia

Proyecto de Construcción de Software 2026
