# Frontend - Sistema Educativo

## Instalación

Las dependencias ya están instaladas. Si necesitas reinstalar:

```bash
npm install
```

## Ejecutar en desarrollo

```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

## Estructura

- **pages/** - Componentes de página (Login, Dashboard, etc.)
- **components/** - Componentes reutilizables (Input, Button, etc.)
- **store/** - Estado global con Zustand (useAuthStore)
- **types/** - Tipos TypeScript
- **api/** - Configuración de Axios

## Flujo de autenticación

1. Usuario ingresa credenciales en Login.tsx
2. Se validan con el backend en `/auth/login`
3. El token se guarda en localStorage
4. useAuthStore gestiona el estado de autenticación
5. Las rutas protegidas redirigen al login si no está autenticado

## Credenciales de prueba

- Email: `director@example.com`
- Contraseña: `director123`

## Dependencias principales

- **React 19** - Framework
- **Vite** - Bundler
- **Tailwind CSS** - Estilos
- **Zustand** - Estado global
- **Sonner** - Notificaciones
- **Axios** - HTTP client
- **React Router** - Enrutamiento
