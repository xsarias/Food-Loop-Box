import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './Usuarios.css'

const ROLES = ['customer', 'partner', 'driver', 'support', 'admin']

const ROLE_LABEL = {
  admin:    'Administrador',
  partner:  'Aliado',
  customer: 'Cliente',
  driver:   'Conductor',
  support:  'Soporte',
}

const ROLE_FILTER_TABS = [
  { key: '', label: 'Todos' },
  { key: 'customer', label: 'Clientes' },
  { key: 'partner',  label: 'Aliados'  },
  { key: 'driver',   label: 'Conductores' },
  { key: 'support',  label: 'Soporte'  },
  { key: 'admin',    label: 'Admins'   },
]

function initials(u) {
  const f = u.first_name?.[0] ?? ''
  const l = u.last_name?.[0] ?? ''
  return (f + l).toUpperCase() || u.username?.[0]?.toUpperCase() || '?'
}

function UserRow({ u, onRoleChange, onVerify, onToggleActive, busy }) {
  const isBusy = busy === u.id
  const [role, setRole] = useState(u.role)

  const handleRoleChange = (e) => {
    setRole(e.target.value)
    onRoleChange(u.id, e.target.value)
  }

  return (
    <div className={`user-row ${!u.is_active ? 'row-inactive' : ''}`}>
      <div className="user-avatar">{initials(u)}</div>

      <div className="user-main">
        <span className="user-fullname">
          {u.first_name || u.last_name
            ? `${u.first_name} ${u.last_name}`.trim()
            : u.username}
        </span>
        <span className="user-username">@{u.username}</span>
        <span className="user-email">{u.email || '—'}</span>
      </div>

      <div className="user-meta">
        <span className={`verified-chip ${u.is_verified ? 'chip-yes' : 'chip-no'}`}>
          {u.is_verified ? '✓ Verificado' : '✗ Sin verificar'}
        </span>
        <span className={`active-chip ${u.is_active ? 'chip-active' : 'chip-inactive'}`}>
          {u.is_active ? 'Activo' : 'Inactivo'}
        </span>
      </div>

      <div className="user-actions">
        <select
          className="role-select"
          value={role}
          disabled={isBusy}
          onChange={handleRoleChange}
        >
          {ROLES.map(r => (
            <option key={r} value={r}>{ROLE_LABEL[r]}</option>
          ))}
        </select>

        {!u.is_verified && (
          <button
            className="btn-verify"
            disabled={isBusy}
            onClick={() => onVerify(u.id)}
          >
            Verificar
          </button>
        )}

        <button
          className={`btn-toggle ${u.is_active ? 'btn-deactivate' : 'btn-activate'}`}
          disabled={isBusy}
          onClick={() => onToggleActive(u.id)}
        >
          {isBusy ? '…' : u.is_active ? 'Desactivar' : 'Activar'}
        </button>
      </div>
    </div>
  )
}

function Usuarios() {
  const navigate = useNavigate()
  const { user, isAuthenticated } = useAuth()

  const [users, setUsers]       = useState([])
  const [roleTab, setRoleTab]   = useState('')
  const [search, setSearch]     = useState('')
  const [loading, setLoading]   = useState(true)
  const [busy, setBusy]         = useState(null)
  const [toast, setToast]       = useState(null)

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login'); return }
    if (user?.role !== 'admin') { navigate('/'); }
  }, [isAuthenticated, user, navigate])

  const fetchUsers = useCallback(() => {
    if (!isAuthenticated || user?.role !== 'admin') return
    setLoading(true)
    const params = new URLSearchParams()
    if (roleTab) params.set('role', roleTab)
    if (search)  params.set('search', search)
    api.get(`/auth/users/?${params}`)
      .then(res => setUsers(res.data.results ?? res.data))
      .catch(() => showToast('Error al cargar usuarios.', false))
      .finally(() => setLoading(false))
  }, [isAuthenticated, user, roleTab, search])

  useEffect(() => {
    const t = setTimeout(() => fetchUsers(), search ? 400 : 0)
    return () => clearTimeout(t)
  }, [fetchUsers, search])

  const showToast = (msg, ok = true) => {
    setToast({ msg, ok })
    setTimeout(() => setToast(null), 3000)
  }

  const handleRoleChange = async (id, newRole) => {
    setBusy(id)
    try {
      await api.patch(`/auth/users/${id}/`, { role: newRole })
      setUsers(prev => prev.map(u => u.id === id ? { ...u, role: newRole } : u))
      showToast(`Rol actualizado a ${ROLE_LABEL[newRole]}.`)
    } catch {
      showToast('No se pudo cambiar el rol.', false)
      fetchUsers()
    } finally {
      setBusy(null)
    }
  }

  const handleVerify = async (id) => {
    setBusy(id)
    try {
      const { data } = await api.post(`/auth/users/${id}/verify/`)
      setUsers(prev => prev.map(u => u.id === id ? { ...u, is_verified: true } : u))
      showToast('Usuario verificado correctamente.')
    } catch {
      showToast('No se pudo verificar el usuario.', false)
    } finally {
      setBusy(null)
    }
  }

  const handleToggleActive = async (id) => {
    setBusy(id)
    try {
      const { data } = await api.post(`/auth/users/${id}/toggle_active/`)
      setUsers(prev => prev.map(u => u.id === id ? { ...u, is_active: data.is_active } : u))
      showToast(data.is_active ? 'Usuario activado.' : 'Usuario desactivado.')
    } catch {
      showToast('No se pudo cambiar el estado.', false)
    } finally {
      setBusy(null)
    }
  }

  if (!isAuthenticated || user?.role !== 'admin') return null

  return (
    <div className="usuarios-page">
      <header className="usuarios-header">
        <div className="usuarios-brand">
          <div className="brand-icon">FLB</div>
          <div>
            <h2>Food Loop Box</h2>
            <p>Gestión de usuarios</p>
          </div>
        </div>
        <button className="back-btn" onClick={() => navigate('/')}>← Inicio</button>
      </header>

      <main className="usuarios-main">
        <div className="usuarios-title-row">
          <h1>Asignar roles</h1>
          <p>Administra los usuarios y sus permisos en el sistema</p>
        </div>

        {/* Controles */}
        <div className="usuarios-controls">
          <input
            className="search-input"
            type="search"
            placeholder="Buscar por nombre, usuario o correo…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <div className="role-tabs">
            {ROLE_FILTER_TABS.map(t => (
              <button
                key={t.key}
                className={`rtab-btn ${roleTab === t.key ? 'active' : ''}`}
                onClick={() => setRoleTab(t.key)}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Lista */}
        {loading ? (
          <div className="state-box">
            <div className="spinner" />
            <p>Cargando usuarios…</p>
          </div>
        ) : users.length === 0 ? (
          <div className="state-box">
            <span className="empty-icon">👤</span>
            <p>No se encontraron usuarios.</p>
          </div>
        ) : (
          <>
            <p className="usuarios-count">{users.length} usuario{users.length !== 1 ? 's' : ''}</p>
            <div className="users-list">
              {users.map(u => (
                <UserRow
                  key={u.id}
                  u={u}
                  onRoleChange={handleRoleChange}
                  onVerify={handleVerify}
                  onToggleActive={handleToggleActive}
                  busy={busy}
                />
              ))}
            </div>
          </>
        )}
      </main>

      {toast && (
        <div className={`usuarios-toast ${toast.ok ? 'toast-ok' : 'toast-err'}`}>
          {toast.msg}
        </div>
      )}
    </div>
  )
}

export default Usuarios
