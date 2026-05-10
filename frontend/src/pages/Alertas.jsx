import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './Alertas.css'

function fmtDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleString('es-CO', { dateStyle: 'medium', timeStyle: 'short' })
}

function timeLeft(d) {
  if (!d) return ''
  const diff = new Date(d) - Date.now()
  if (diff <= 0) return 'Vencido'
  const h = Math.floor(diff / 3600000)
  const m = Math.floor((diff % 3600000) / 60000)
  if (h > 0) return `${h}h ${m}m restantes`
  return `${m} min restantes`
}

function AlertCard({ product, onRemove, busy }) {
  const expired = new Date(product.expiration_date) <= Date.now()
  return (
    <div className={`alert-card ${expired ? 'card-expired' : 'card-expiring'}`}>
      <div className="alert-card-left">
        <span className="alert-icon">{expired ? '🚨' : '⚠️'}</span>
        <div className="alert-info">
          <span className="alert-name">{product.name}</span>
          <span className="alert-provider">{product.provider?.name ?? '—'}</span>
          <span className="alert-meta">{product.category?.name ?? '—'} · {Number(product.quantity).toFixed(1)} {product.unit}</span>
        </div>
      </div>
      <div className="alert-card-right">
        <span className={`time-chip ${expired ? 'chip-red' : 'chip-orange'}`}>
          {timeLeft(product.expiration_date)}
        </span>
        <span className="alert-date">{fmtDate(product.expiration_date)}</span>
        <button
          className="btn-retire"
          disabled={busy === product.id}
          onClick={() => onRemove(product.id)}
        >
          {busy === product.id ? 'Retirando…' : 'Retirar'}
        </button>
      </div>
    </div>
  )
}

function Alertas() {
  const navigate = useNavigate()
  const { user, isAuthenticated } = useAuth()

  const [expiring, setExpiring] = useState([])
  const [expired, setExpired] = useState([])
  const [tab, setTab] = useState('expiring')
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(null)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login'); return }
    if (!['admin', 'partner'].includes(user?.role)) { navigate('/'); return }
  }, [isAuthenticated, user, navigate])

  const fetchAll = useCallback(() => {
    if (!isAuthenticated || !['admin', 'partner'].includes(user?.role)) return
    setLoading(true)
    Promise.all([
      api.get('/products/products/expiring_soon/'),
      api.get('/products/products/expired/'),
    ])
      .then(([expRes, expdRes]) => {
        setExpiring(expRes.data.products ?? expRes.data.results ?? [])
        setExpired(expdRes.data.products ?? expdRes.data.results ?? [])
      })
      .catch(() => showToast('Error al cargar las alertas.', false))
      .finally(() => setLoading(false))
  }, [isAuthenticated, user])

  useEffect(() => { fetchAll() }, [fetchAll])

  const showToast = (msg, ok = true) => {
    setToast({ msg, ok })
    setTimeout(() => setToast(null), 3000)
  }

  const handleRemove = async (id) => {
    setBusy(id)
    try {
      await api.patch(`/products/products/${id}/`, { status: 'removed' })
      setExpiring(prev => prev.filter(p => p.id !== id))
      setExpired(prev => prev.filter(p => p.id !== id))
      showToast('Producto retirado del inventario.')
    } catch {
      showToast('No se pudo retirar el producto.', false)
    } finally {
      setBusy(null)
    }
  }

  if (!isAuthenticated) return null

  const list = tab === 'expiring' ? expiring : expired

  return (
    <div className="alertas-page">
      <header className="alertas-header">
        <div className="alertas-brand">
          <div className="brand-icon">FLB</div>
          <div>
            <h2>Food Loop Box</h2>
            <p>Alertas de vencimiento</p>
          </div>
        </div>
        <button className="back-btn" onClick={() => navigate('/')}>← Inicio</button>
      </header>

      <main className="alertas-main">
        <div className="alertas-title-row">
          <h1>Alertas de vencimiento</h1>
          <p>Productos que requieren acción inmediata</p>
        </div>

        {/* Resumen */}
        {!loading && (
          <div className="alert-summary">
            <div className={`summary-card ${expiring.length > 0 ? 'summary-warn' : 'summary-ok'}`}>
              <span className="summary-num">{expiring.length}</span>
              <span className="summary-label">Vencen en las próximas 24h</span>
            </div>
            <div className={`summary-card ${expired.length > 0 ? 'summary-danger' : 'summary-ok'}`}>
              <span className="summary-num">{expired.length}</span>
              <span className="summary-label">Ya vencidos</span>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div className="alert-tabs">
          <button
            className={`atab-btn ${tab === 'expiring' ? 'active' : ''}`}
            onClick={() => setTab('expiring')}
          >
            ⚠️ Próximos a vencer
            {expiring.length > 0 && <span className="tab-badge">{expiring.length}</span>}
          </button>
          <button
            className={`atab-btn ${tab === 'expired' ? 'active' : ''}`}
            onClick={() => setTab('expired')}
          >
            🚨 Ya vencidos
            {expired.length > 0 && <span className="tab-badge tab-badge-red">{expired.length}</span>}
          </button>
        </div>

        {/* Lista */}
        {loading ? (
          <div className="state-box">
            <div className="spinner" />
            <p>Cargando alertas…</p>
          </div>
        ) : list.length === 0 ? (
          <div className="state-box">
            <span className="empty-icon">✅</span>
            <p>{tab === 'expiring' ? 'No hay productos próximos a vencer.' : 'No hay productos vencidos.'}</p>
          </div>
        ) : (
          <div className="alert-list">
            {list.map(p => (
              <AlertCard key={p.id} product={p} onRemove={handleRemove} busy={busy} />
            ))}
          </div>
        )}
      </main>

      {toast && (
        <div className={`alertas-toast ${toast.ok ? 'toast-ok' : 'toast-err'}`}>
          {toast.msg}
        </div>
      )}
    </div>
  )
}

export default Alertas
