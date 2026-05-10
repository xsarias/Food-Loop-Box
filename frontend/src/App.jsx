import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Perfil from './pages/Perfil'
import DonarAlimento from './pages/DonarAlimento'
import ObtenerAlimento from './pages/ObtenerAlimento'
import ReclamarAlimento from './pages/ReclamarAlimento'
import VenderAlimento from './pages/VenderAlimento'
import Dashboard from './pages/Dashboard'
import Inventario from './pages/Inventario'
import Alertas from './pages/Alertas'
import Usuarios from './pages/Usuarios'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/perfil" element={<Perfil />} />
          <Route path="/obtener" element={<ObtenerAlimento />} />
          <Route path="/donar" element={<DonarAlimento />} />
          <Route path="/vender" element={<VenderAlimento />} />
          <Route path="/reclamar" element={<ReclamarAlimento />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/inventario" element={<Inventario />} />
          <Route path="/alertas" element={<Alertas />} />
          <Route path="/usuarios" element={<Usuarios />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
