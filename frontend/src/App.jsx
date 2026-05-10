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
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
