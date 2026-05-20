import { useState, useEffect } from 'react';
import { FaHandPaper } from "react-icons/fa";
import { FaHandHoldingHeart } from "react-icons/fa";
import { MdSell } from "react-icons/md";
import { FiBox } from "react-icons/fi";
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import "./Home.css"

function Home() {
  const navigate = useNavigate()
  const { user, isAuthenticated, logout } = useAuth()
  const [expiringCount, setExpiringCount] = useState(0)
  const logoSrc = '/LOGOflb.png'

  useEffect(() => {
    if (!isAuthenticated || !['admin', 'partner'].includes(user?.role)) return
    api.get('/products/products/expiring_soon/')
      .then(res => setExpiringCount(res.data.count ?? (res.data.products?.length ?? 0)))
      .catch(() => {})
  }, [isAuthenticated, user])

  const handleLogout = async () => {
    await logout()
  }

  return (
    <div className="home-page">
      <header className="home-header">
        <div className="brand-block">
          <img className="brand-logo" src={logoSrc} alt="Food Loop Box" />
          <div>
            <h2>Food Loop Box</h2>
            <p>Red local contra el desperdicio</p>
          </div>
        </div>

        {isAuthenticated ? (
          <div className="user-block">
            <span
              className="user-greeting"
              onClick={() => navigate('/perfil')}
              style={{ cursor: 'pointer' }}
            >
              Hola, <strong>{user.first_name || user.username}</strong>
            </span>
            {['admin', 'partner'].includes(user.role) && (
              <button className="inventario-btn" type="button" onClick={() => navigate('/inventario')}>
                Inventario
              </button>
            )}
            {['admin', 'partner'].includes(user.role) && (
              <button className="alertas-btn" type="button" onClick={() => navigate('/alertas')}>
                Alertas
                {expiringCount > 0 && <span className="alert-badge">{expiringCount}</span>}
              </button>
            )}
            {user.role === 'admin' && (
              <button className="usuarios-btn" type="button" onClick={() => navigate('/usuarios')}>
                Usuarios
              </button>
            )}
            {user.role === 'admin' && (
              <button className="dashboard-btn" type="button" onClick={() => navigate('/dashboard')}>
                Dashboard
              </button>
            )}
            <button className="login-btn" type="button" onClick={handleLogout}>
              Cerrar sesión
            </button>
          </div>
        ) : (
          <div className="user-block">
            <button
              className="login-btn"
              type="button"
              onClick={() => navigate('/login')}
            >
              Iniciar sesión
            </button>
            <button
              className="register-btn"
              type="button"
              onClick={() => navigate('/register')}
            >
              Registrarse
            </button>
          </div>
        )}
      </header>

      <main className="home-main">
        <section className="hero-card">
          <img className="hero-logo" src={logoSrc} alt="Food Loop Box" />
          <h1>Food Loop Box</h1>
          <p>Lo que sobra, alimenta. Dona, comparte, recupera y mueve alimentos en tu comunidad.</p>
        </section>

        <section className="actions-card">
          <h3>¿Qué deseas hacer hoy?</h3>
          <div className="actions-grid">
            <button className="boton1" onClick={() => navigate('/obtener')}>
              <FaHandPaper /> Obtener Alimento
            </button>
            <button className="boton2" onClick={() => navigate('/donar')}>
              <FaHandHoldingHeart /> Donar Alimento
            </button>
            <button className="boton1" onClick={() => navigate('/vender')}>
              <MdSell /> Vender Alimento
            </button>
            <button className="boton2" onClick={() => navigate('/reclamar')}>
              <FiBox /> Reclamar Alimento
            </button>
          </div>
        </section>
      </main>
    </div>
  )
}

export default Home
