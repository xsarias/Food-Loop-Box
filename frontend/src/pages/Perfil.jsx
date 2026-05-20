import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './Perfil.css'

const ROLE_LABEL = {
  admin: 'Administrador',
  partner: 'Aliado',
  customer: 'Cliente',
  driver: 'Conductor',
  support: 'Soporte',
}

function Perfil() {
  const navigate = useNavigate()
  const { user, isAuthenticated, logout, updateUser } = useAuth()

  const [infoForm, setInfoForm] = useState({
    first_name: user?.first_name ?? '',
    last_name: user?.last_name ?? '',
    phone: user?.phone ?? '',
  })
  const [infoLoading, setInfoLoading] = useState(false)
  const [infoMsg, setInfoMsg] = useState(null)

  const [pwForm, setPwForm] = useState({
    old_password: '',
    new_password: '',
    new_password_confirm: '',
  })
  const [pwLoading, setPwLoading] = useState(false)
  const [pwMsg, setPwMsg] = useState(null)

  if (!isAuthenticated) {
    navigate('/login')
    return null
  }

  const handleInfoChange = (e) => {
    setInfoForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
    setInfoMsg(null)
  }

  const handleInfoSubmit = async (e) => {
    e.preventDefault()
    setInfoLoading(true)
    setInfoMsg(null)
    try {
      const { data } = await api.patch(`/auth/users/${user.id}/`, infoForm)
      updateUser(data)
      setInfoMsg({ text: 'Datos actualizados correctamente.', ok: true })
    } catch (err) {
      const d = err.response?.data
      const text = d && typeof d === 'object'
        ? Object.values(d).flat()[0]
        : 'Error al actualizar los datos.'
      setInfoMsg({ text, ok: false })
    } finally {
      setInfoLoading(false)
    }
  }

  const handlePwChange = (e) => {
    setPwForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
    setPwMsg(null)
  }

  const handlePwSubmit = async (e) => {
    e.preventDefault()
    if (pwForm.new_password !== pwForm.new_password_confirm) {
      setPwMsg({ text: 'Las contraseñas nuevas no coinciden.', ok: false })
      return
    }
    setPwLoading(true)
    setPwMsg(null)
    try {
      await api.post('/auth/users/change_password/', pwForm)
      setPwMsg({ text: 'Contraseña actualizada. Vuelve a iniciar sesión.', ok: true })
      setPwForm({ old_password: '', new_password: '', new_password_confirm: '' })
      setTimeout(() => logout().then(() => navigate('/login')), 2000)
    } catch (err) {
      const d = err.response?.data
      const text = d && typeof d === 'object'
        ? Object.values(d).flat()[0]
        : 'Error al cambiar la contraseña.'
      setPwMsg({ text, ok: false })
    } finally {
      setPwLoading(false)
    }
  }

  const initials = `${user.first_name?.[0] ?? ''}${user.last_name?.[0] ?? ''}`.toUpperCase() || user.username?.[0]?.toUpperCase()

  return (
    <div className="perfil-page">
      <header className="perfil-header">
        <div className="perfil-brand">
          <img className="brand-icon" src="/LOGOflb.png" alt="Food Loop Box" />
          <div>
            <h2>Food Loop Box</h2>
            <p>Mi perfil</p>
          </div>
        </div>
        <button className="back-btn" onClick={() => navigate('/')}>← Inicio</button>
      </header>

      <main className="perfil-main">

        {/* Avatar + info de solo lectura */}
        <div className="perfil-hero">
          <div className="avatar">{initials}</div>
          <div>
            <h1 className="perfil-name">
              {user.first_name || user.last_name
                ? `${user.first_name} ${user.last_name}`.trim()
                : user.username}
            </h1>
            <p className="perfil-username">@{user.username}</p>
            <span className={`role-chip role-${user.role}`}>
              {ROLE_LABEL[user.role] ?? user.role}
            </span>
          </div>
        </div>

        {/* Información de solo lectura */}
        <div className="perfil-section">
          <h2 className="section-title">Información de la cuenta</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Correo</span>
              <span className="info-value">{user.email || '—'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Usuario</span>
              <span className="info-value">{user.username}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Verificado</span>
              <span className="info-value">{user.is_verified ? '✓ Sí' : '✗ No'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Rol</span>
              <span className="info-value">{ROLE_LABEL[user.role] ?? user.role}</span>
            </div>
          </div>
        </div>

        {/* Editar datos personales */}
        <div className="perfil-section">
          <h2 className="section-title">Editar datos personales</h2>
          <form className="perfil-form" onSubmit={handleInfoSubmit}>
            <div className="form-row">
              <div className="field-group">
                <label htmlFor="first_name">Nombre</label>
                <input
                  id="first_name" name="first_name" type="text"
                  value={infoForm.first_name} onChange={handleInfoChange}
                  placeholder="Ana"
                />
              </div>
              <div className="field-group">
                <label htmlFor="last_name">Apellido</label>
                <input
                  id="last_name" name="last_name" type="text"
                  value={infoForm.last_name} onChange={handleInfoChange}
                  placeholder="García"
                />
              </div>
            </div>

            <div className="field-group">
              <label htmlFor="phone">Teléfono</label>
              <input
                id="phone" name="phone" type="tel"
                value={infoForm.phone} onChange={handleInfoChange}
                placeholder="3001234567"
              />
            </div>

            {infoMsg && (
              <p className={`form-msg ${infoMsg.ok ? 'msg-ok' : 'msg-err'}`}>
                {infoMsg.text}
              </p>
            )}

            <div className="form-actions">
              <button type="submit" className="btn-primary" disabled={infoLoading}>
                {infoLoading ? 'Guardando…' : 'Guardar cambios'}
              </button>
            </div>
          </form>
        </div>

        {/* Cambiar contraseña */}
        <div className="perfil-section">
          <h2 className="section-title">Cambiar contraseña</h2>
          <form className="perfil-form" onSubmit={handlePwSubmit}>
            <div className="field-group">
              <label htmlFor="old_password">Contraseña actual</label>
              <input
                id="old_password" name="old_password" type="password"
                value={pwForm.old_password} onChange={handlePwChange}
                placeholder="••••••••" required autoComplete="current-password"
              />
            </div>
            <div className="form-row">
              <div className="field-group">
                <label htmlFor="new_password">Nueva contraseña</label>
                <input
                  id="new_password" name="new_password" type="password"
                  value={pwForm.new_password} onChange={handlePwChange}
                  placeholder="Mínimo 8 caracteres" required minLength={8}
                  autoComplete="new-password"
                />
              </div>
              <div className="field-group">
                <label htmlFor="new_password_confirm">Confirmar nueva</label>
                <input
                  id="new_password_confirm" name="new_password_confirm" type="password"
                  value={pwForm.new_password_confirm} onChange={handlePwChange}
                  placeholder="Repite la contraseña" required minLength={8}
                  autoComplete="new-password"
                />
              </div>
            </div>

            {pwMsg && (
              <p className={`form-msg ${pwMsg.ok ? 'msg-ok' : 'msg-err'}`}>
                {pwMsg.text}
              </p>
            )}

            <div className="form-actions">
              <button type="submit" className="btn-danger" disabled={pwLoading}>
                {pwLoading ? 'Cambiando…' : 'Cambiar contraseña'}
              </button>
            </div>
          </form>
        </div>

        {/* Cerrar sesión */}
        <div className="perfil-section logout-section">
          <button className="btn-logout" onClick={() => logout().then(() => navigate('/login'))}>
            Cerrar sesión
          </button>
        </div>

      </main>
    </div>
  )
}

export default Perfil
