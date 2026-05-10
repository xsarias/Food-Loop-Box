import { useState, useEffect, useCallback, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './ObtenerAlimento.css'

const PAYMENT_METHODS = [
  { key: 'cash',           label: 'Efectivo',        icon: '💵' },
  { key: 'card',           label: 'Tarjeta',          icon: '💳' },
  { key: 'mobile_payment', label: 'Pago Móvil',       icon: '📱' },
  { key: 'transfer',       label: 'Transferencia',    icon: '🏦' },
]

function PaymentModal({ product, onClose, onSuccess }) {
  const [method, setMethod] = useState('cash')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  const overlayRef = useRef(null)

  const price = parseFloat(product.final_price) || 0

  const handleOverlayClick = (e) => {
    if (e.target === overlayRef.current && !result) onClose()
  }

  const handlePay = async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await api.post('/transactions/transactions/', {
        product: product.id,
        amount: price,
        payment_method: method,
      })
      setResult(data)
      onSuccess(product.id)
    } catch (err) {
      const d = err.response?.data
      setError(
        d && typeof d === 'object'
          ? Object.values(d).flat()[0]
          : 'No se pudo procesar el pago. Intenta de nuevo.'
      )
    } finally {
      setLoading(false)
    }
  }

  const fmt = (n) =>
    new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(n)

  return (
    <div className="modal-overlay" ref={overlayRef} onClick={handleOverlayClick}>
      <div className="payment-modal">
        {result ? (
          /* ── Éxito ── */
          <div className="modal-success">
            <span className="success-icon">✅</span>
            <h2>¡Pago exitoso!</h2>
            <p className="success-product">{product.name}</p>
            <p className="success-amount">{fmt(price)}</p>
            <div className="code-box">
              <p className="code-label">Código de retiro</p>
              <p className="code-value">{result.withdrawal_code}</p>
              <p className="code-hint">Preséntalo en el locker para retirar tu producto</p>
            </div>
            <button className="btn-done" onClick={onClose}>Listo</button>
          </div>
        ) : (
          /* ── Formulario ── */
          <>
            <div className="modal-header">
              <h2>Confirmar compra</h2>
              <button className="modal-close" onClick={onClose}>✕</button>
            </div>

            <div className="modal-product">
              <span className="modal-product-name">{product.name}</span>
              <span className="modal-product-meta">
                {product.category_name} · {product.quantity} {product.unit}
              </span>
              <span className="modal-price">{fmt(price)}</span>
            </div>

            <p className="modal-section-label">Método de pago</p>
            <div className="method-grid">
              {PAYMENT_METHODS.map(m => (
                <button
                  key={m.key}
                  className={`method-btn ${method === m.key ? 'method-active' : ''}`}
                  onClick={() => setMethod(m.key)}
                >
                  <span className="method-icon">{m.icon}</span>
                  <span>{m.label}</span>
                </button>
              ))}
            </div>

            {error && <p className="modal-error">{error}</p>}

            <button
              className="btn-pay"
              disabled={loading}
              onClick={handlePay}
            >
              {loading ? 'Procesando…' : `Pagar ${fmt(price)}`}
            </button>
          </>
        )}
      </div>
    </div>
  )
}

function timeUntilExpiry(dateStr) {
  const diff = new Date(dateStr) - Date.now()
  if (diff <= 0) return 'Vencido'
  const hours = Math.floor(diff / 3_600_000)
  if (hours < 1) return 'Vence en < 1h'
  if (hours < 24) return `Vence en ${hours}h`
  return `Vence en ${Math.floor(hours / 24)}d`
}

function formatPrice(price) {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0,
  }).format(price)
}

function ProductCard({ product, onReserve, onBuy, reserving }) {
  const expiry = timeUntilExpiry(product.expiration_date)
  const isExpiringSoon = new Date(product.expiration_date) - Date.now() < 8 * 3_600_000
  const isDonation = product.product_type === 'donation'

  return (
    <div className="product-card">
      {product.image ? (
        <img src={product.image} alt={product.name} className="product-img" />
      ) : (
        <div className="product-img-placeholder">
          {isDonation ? '🤝' : '🛒'}
        </div>
      )}

      <div className="product-body">
        <div className="product-badges">
          <span className={`badge ${isDonation ? 'badge-donation' : 'badge-sale'}`}>
            {isDonation ? 'Donación' : 'Venta'}
          </span>
          <span className="badge badge-cat">{product.category_name}</span>
        </div>

        <h3 className="product-name">{product.name}</h3>
        <p className="product-provider">{product.provider_name}</p>

        <div className="product-meta">
          <span className="product-qty">{product.quantity} {product.unit}</span>
          <span className={`product-expiry ${isExpiringSoon ? 'expiry-soon' : ''}`}>
            ⏱ {expiry}
          </span>
        </div>

        <div className="product-footer">
          <span className="product-price">
            {isDonation ? 'GRATIS' : formatPrice(product.final_price)}
          </span>
          {isDonation ? (
            <button
              className="reserve-btn"
              onClick={() => onReserve(product.id)}
              disabled={product.is_reserved || reserving === product.id}
            >
              {product.is_reserved ? 'Reservado' : reserving === product.id ? 'Reservando…' : 'Obtener'}
            </button>
          ) : (
            <button
              className="buy-btn"
              onClick={() => onBuy(product)}
              disabled={product.is_reserved}
            >
              {product.is_reserved ? 'No disponible' : 'Comprar'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

function ObtenerAlimento() {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()

  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [typeFilter, setTypeFilter] = useState('all')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reserving, setReserving] = useState(null)
  const [toast, setToast] = useState(null)
  const [payProduct, setPayProduct] = useState(null)

  const fetchProducts = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const params = new URLSearchParams({ only_available: 'true' })
      if (typeFilter !== 'all') params.append('product_type', typeFilter)
      if (categoryFilter) params.append('category', categoryFilter)
      if (search.trim()) params.append('search', search.trim())

      const { data } = await api.get(`/products/products/?${params}`)
      setProducts(data.results ?? [])
    } catch {
      setError('No se pudieron cargar los productos. Verifica tu conexión.')
    } finally {
      setLoading(false)
    }
  }, [typeFilter, categoryFilter, search])

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  useEffect(() => {
    api.get('/products/categories/')
      .then(({ data }) => setCategories(data.results ?? []))
      .catch(() => {})
  }, [])

  const showToast = (msg, isError = false) => {
    setToast({ msg, isError })
    setTimeout(() => setToast(null), 3000)
  }

  const handleBuy = (product) => {
    if (!isAuthenticated) { navigate('/login'); return }
    setPayProduct(product)
  }

  const handlePaySuccess = (productId) => {
    setProducts(prev => prev.map(p => p.id === productId ? { ...p, is_reserved: true } : p))
  }

  const handleReserve = async (productId) => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    setReserving(productId)
    try {
      await api.post(`/products/products/${productId}/reserve/`)
      setProducts((prev) =>
        prev.map((p) => (p.id === productId ? { ...p, is_reserved: true } : p))
      )
      showToast('¡Producto reservado exitosamente!')
    } catch (err) {
      showToast(err.response?.data?.detail || 'No se pudo reservar el producto', true)
    } finally {
      setReserving(null)
    }
  }

  return (
    <div className="obtener-page">
      <header className="obtener-header">
        <div className="obtener-brand">
          <div className="brand-icon">FLB</div>
          <div>
            <h2>Food Loop Box</h2>
            <p>Productos disponibles</p>
          </div>
        </div>
        <button className="back-btn" onClick={() => navigate('/')}>← Inicio</button>
      </header>

      <main className="obtener-main">
        <div className="obtener-title-row">
          <h1>Obtener Alimento</h1>
          <p>Encuentra excedentes disponibles cerca de ti</p>
        </div>

        <div className="filters-bar">
          <div className="type-filters">
            {[
              { value: 'all', label: 'Todos' },
              { value: 'sale', label: 'Venta' },
              { value: 'donation', label: 'Donación' },
            ].map(({ value, label }) => (
              <button
                key={value}
                className={`filter-btn ${typeFilter === value ? 'active' : ''}`}
                onClick={() => setTypeFilter(value)}
              >
                {label}
              </button>
            ))}
          </div>

          <div className="search-row">
            {categories.length > 0 && (
              <select
                className="cat-select"
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
              >
                <option value="">Todas las categorías</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            )}
            <input
              className="search-input"
              type="search"
              placeholder="Buscar producto o proveedor…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        {loading && (
          <div className="state-box">
            <div className="spinner" />
            <p>Cargando productos…</p>
          </div>
        )}

        {!loading && error && (
          <div className="state-box error-box">
            <p>{error}</p>
            <button className="retry-btn" onClick={fetchProducts}>Reintentar</button>
          </div>
        )}

        {!loading && !error && products.length === 0 && (
          <div className="state-box">
            <span className="empty-icon">🥗</span>
            <p>No hay productos disponibles en este momento.</p>
            {!isAuthenticated && (
              <p className="hint-text">
                <button className="link-btn" onClick={() => navigate('/login')}>
                  Inicia sesión
                </button>{' '}
                para ver todos los productos.
              </p>
            )}
          </div>
        )}

        {!loading && !error && products.length > 0 && (
          <>
            <p className="results-count">{products.length} producto{products.length !== 1 ? 's' : ''} encontrado{products.length !== 1 ? 's' : ''}</p>
            <div className="products-grid">
              {products.map((p) => (
                <ProductCard
                  key={p.id}
                  product={p}
                  onReserve={handleReserve}
                  onBuy={handleBuy}
                  reserving={reserving}
                />
              ))}
            </div>
          </>
        )}
      </main>

      {toast && (
        <div className={`toast ${toast.isError ? 'toast-error' : 'toast-success'}`}>
          {toast.msg}
        </div>
      )}

      {payProduct && (
        <PaymentModal
          product={payProduct}
          onClose={() => setPayProduct(null)}
          onSuccess={handlePaySuccess}
        />
      )}
    </div>
  )
}

export default ObtenerAlimento
