import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Login.css'
import './Register.css'

const INITIAL = {
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  document_id: '',
  document_type: 'cc',
  role: 'customer',
  password: '',
  password_confirm: '',
}

function Register() {
  const navigate = useNavigate()
  const { register } = useAuth()
  const [form, setForm] = useState(INITIAL)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== form.password_confirm) {
      setError('Las contraseñas no coinciden')
      return
    }
    setLoading(true)
    try {
      await register(form)
      navigate('/')
    } catch (err) {
      const data = err.response?.data
      if (data && typeof data === 'object') {
        const first = Object.values(data)[0]
        setError(Array.isArray(first) ? first[0] : String(first))
      } else {
        setError('Error al crear la cuenta')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <header className="auth-header">
        <div className="auth-brand" onClick={() => navigate('/')}>
          <div className="brand-icon">FLB</div>
          <div>
            <h2>Food Loop Box</h2>
            <p>Red local contra el desperdicio</p>
          </div>
        </div>
      </header>

      <main className="auth-main">
        <div className="auth-card register-card">
          <h1>Crear cuenta</h1>
          <p className="auth-subtitle">Únete a la red de rescate alimentario.</p>

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-row">
              <div className="field-group">
                <label htmlFor="first_name">Nombre</label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  value={form.first_name}
                  onChange={handleChange}
                  placeholder="Ana"
                  required
                />
              </div>
              <div className="field-group">
                <label htmlFor="last_name">Apellido</label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  value={form.last_name}
                  onChange={handleChange}
                  placeholder="García"
                  required
                />
              </div>
            </div>

            <div className="field-group">
              <label htmlFor="username">Nombre de usuario</label>
              <input
                id="username"
                name="username"
                type="text"
                value={form.username}
                onChange={handleChange}
                placeholder="ana_garcia"
                required
                autoComplete="username"
              />
            </div>

            <div className="field-group">
              <label htmlFor="email">Correo electrónico</label>
              <input
                id="email"
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                placeholder="ana@ejemplo.com"
                required
                autoComplete="email"
              />
            </div>

            <div className="form-row">
              <div className="field-group">
                <label htmlFor="phone">Teléfono</label>
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  value={form.phone}
                  onChange={handleChange}
                  placeholder="3001234567"
                />
              </div>
              <div className="field-group">
                <label htmlFor="document_id">Número de documento</label>
                <input
                  id="document_id"
                  name="document_id"
                  type="text"
                  value={form.document_id}
                  onChange={handleChange}
                  placeholder="1234567890"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="field-group">
                <label htmlFor="document_type">Tipo de doc.</label>
                <select
                  id="document_type"
                  name="document_type"
                  value={form.document_type}
                  onChange={handleChange}
                >
                  <option value="cc">Cédula</option>
                  <option value="passport">Pasaporte</option>
                </select>
              </div>
              <div className="field-group">
                <label htmlFor="role">Tipo de cuenta</label>
                <select
                  id="role"
                  name="role"
                  value={form.role}
                  onChange={handleChange}
                >
                  <option value="customer">Cliente</option>
                  <option value="partner">Aliado (proveedor)</option>
                </select>
              </div>
            </div>

            <div className="field-group">
              <label htmlFor="password">Contraseña</label>
              <input
                id="password"
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                placeholder="Mínimo 8 caracteres"
                required
                minLength={8}
                autoComplete="new-password"
              />
            </div>

            <div className="field-group">
              <label htmlFor="password_confirm">Confirmar contraseña</label>
              <input
                id="password_confirm"
                name="password_confirm"
                type="password"
                value={form.password_confirm}
                onChange={handleChange}
                placeholder="Repite la contraseña"
                required
                minLength={8}
                autoComplete="new-password"
              />
            </div>

            {error && <p className="auth-error">{error}</p>}

            <button type="submit" className="auth-submit" disabled={loading}>
              {loading ? 'Creando cuenta…' : 'Registrarse'}
            </button>
          </form>

          <p className="auth-switch">
            ¿Ya tienes cuenta?{' '}
            <Link to="/login">Inicia sesión</Link>
          </p>
        </div>
      </main>
    </div>
  )
}

export default Register
