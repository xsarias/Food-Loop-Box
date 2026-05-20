import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './Inventario.css'

const STATUS_LABEL = {
  available:  'Disponible',
  reserved:   'Reservado',
  collected:  'Recolectado',
  expired:    'Vencido',
  removed:    'Retirado',
}

const STATUS_TABS = [
  { key: '',            label: 'Todos'        },
  { key: 'available',  label: 'Disponibles'  },
  { key: 'reserved',   label: 'Reservados'   },
  { key: 'collected',  label: 'Recolectados' },
  { key: 'expired',    label: 'Vencidos'     },
  { key: 'removed',    label: 'Retirados'    },
]

const TYPE_LABEL = { donation: 'Donación', sale: 'Venta' }

function fmtDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleString('es-CO', { dateStyle: 'medium', timeStyle: 'short' })
}

function ProductCard({ product, onAction, busy }) {
  const { id, name, product_type, status, category, quantity, unit, expiration_date, provider } = product
  const isBusy = busy === id

  const actions = []
  if (status === 'available' || status === 'reserved') {
    actions.push({ key: 'collected', label: '✓ Marcar recolectado', cls: 'btn-collect' })
  }
  if (status === 'available' || status === 'expired') {
    actions.push({ key: 'removed', label: 'Retirar', cls: 'btn-remove' })
  }

  return (
    <div className={`inv-card s-${status}`}>
      <div className="inv-card-head">
        <span className="inv-name">{name}</span>
        <div className="inv-badges">
          <span className={`badge tp-${product_type}`}>{TYPE_LABEL[product_type] ?? product_type}</span>
          <span className={`badge st-${status}`}>{STATUS_LABEL[status] ?? status}</span>
        </div>
      </div>
      <div className="inv-card-body">
        <span className="inv-meta">{category?.name ?? '—'}</span>
        <span className="inv-meta">{Number(quantity).toFixed(1)} {unit}</span>
        <span className="inv-meta">Vence: {fmtDate(expiration_date)}</span>
        {provider?.name && <span className="inv-meta">Aliado: {provider.name}</span>}
      </div>
      {actions.length > 0 && (
        <div className="inv-card-actions">
          {actions.map(a => (
            <button
              key={a.key}
              className={a.cls}
              disabled={isBusy}
              onClick={() => onAction(id, a.key)}
            >
              {isBusy ? 'Guardando…' : a.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function Inventario() {
  const navigate = useNavigate()
  const { user, isAuthenticated } = useAuth()

  const [products, setProducts] = useState([])
  const [statusTab, setStatusTab] = useState('')
  const [typeFilter, setTypeFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(null)
  const [toast, setToast] = useState(null)
  const [forbidden, setForbidden] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login'); return }
    if (!['admin', 'partner'].includes(user?.role)) {
      setForbidden(true)
      setLoading(false)
    }
  }, [isAuthenticated, user, navigate])

  const fetchProducts = useCallback(() => {
    if (!isAuthenticated || !['admin', 'partner'].includes(user?.role)) return
    setLoading(true)
    const params = new URLSearchParams()
    if (statusTab) params.set('status', statusTab)
    if (typeFilter) params.set('product_type', typeFilter)
    api.get(`/products/products/?${params}`)
      .then(res => setProducts(res.data.results ?? res.data))
      .catch(() => showToast('Error al cargar el inventario.', false))
      .finally(() => setLoading(false))
  }, [isAuthenticated, user, statusTab, typeFilter])

  useEffect(() => { fetchProducts() }, [fetchProducts])

  const showToast = (msg, ok = true) => {
    setToast({ msg, ok })
    setTimeout(() => setToast(null), 3000)
  }

  const handleAction = async (id, newStatus) => {
    setBusy(id)
    try {
      await api.patch(`/products/products/${id}/`, { status: newStatus })
      setProducts(prev => prev.map(p => p.id === id ? { ...p, status: newStatus } : p))
      showToast(
        newStatus === 'collected' ? 'Producto marcado como recolectado.' : 'Producto retirado del inventario.',
        true
      )
    } catch {
      showToast('No se pudo actualizar el estado.', false)
    } finally {
      setBusy(null)
    }
  }

  if (!isAuthenticated) return null

  if (forbidden) {
    return (
      <div className="inv-page">
        <div className="forbidden-box">
          <span>🔒</span>
          <h2>Acceso restringido</h2>
          <p>Esta sección es solo para aliados y administradores.</p>
          <button className="back-btn" onClick={() => navigate('/')}>← Volver al inicio</button>
        </div>
      </div>
    )
  }

  return (
    <div className="inv-page">
      <header className="inv-header">
        <div className="inv-brand">
          <img className="brand-icon" src="/LOGOflb.png" alt="Food Loop Box" />
          <div>
            <h2>Food Loop Box</h2>
            <p>Inventario de productos</p>
          </div>
        </div>
        <button className="back-btn" onClick={() => navigate('/')}>← Inicio</button>
      </header>

      <main className="inv-main">
        <div className="inv-title-row">
          <h1>Actualizar inventario</h1>
          <p>Gestiona el estado de los productos registrados en el sistema</p>
        </div>

        {/* Filtros */}
        <div className="inv-filters">
          <div className="status-tabs">
            {STATUS_TABS.map(t => (
              <button
                key={t.key}
                className={`tab-btn ${statusTab === t.key ? 'active' : ''}`}
                onClick={() => setStatusTab(t.key)}
              >
                {t.label}
              </button>
            ))}
          </div>
          <div className="type-pills">
            {[['', 'Todos'], ['donation', 'Donación'], ['sale', 'Venta']].map(([v, l]) => (
              <button
                key={v}
                className={`pill-btn ${typeFilter === v ? 'active' : ''}`}
                onClick={() => setTypeFilter(v)}
              >
                {l}
              </button>
            ))}
          </div>
        </div>

        {/* Contenido */}
        {loading ? (
          <div className="state-box">
            <div className="spinner" />
            <p>Cargando inventario…</p>
          </div>
        ) : products.length === 0 ? (
          <div className="state-box">
            <span className="empty-icon">📦</span>
            <p>No hay productos con este filtro.</p>
          </div>
        ) : (
          <>
            <p className="inv-count">{products.length} producto{products.length !== 1 ? 's' : ''}</p>
            <div className="inv-grid">
              {products.map(p => (
                <ProductCard key={p.id} product={p} onAction={handleAction} busy={busy} />
              ))}
            </div>
          </>
        )}
      </main>

      {toast && (
        <div className={`inv-toast ${toast.ok ? 'toast-ok' : 'toast-err'}`}>
          {toast.msg}
        </div>
      )}
    </div>
  )
}

export default Inventario
