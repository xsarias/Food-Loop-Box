import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './ObtenerAlimento.css'

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

function ProductCard({ product, onReserve, reserving }) {
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
          <button
            className="reserve-btn"
            onClick={() => onReserve(product.id)}
            disabled={product.is_reserved || reserving === product.id}
          >
            {product.is_reserved
              ? 'Reservado'
              : reserving === product.id
              ? 'Reservando…'
              : isDonation
              ? 'Obtener'
              : 'Reservar'}
          </button>
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
    </div>
  )
}

export default ObtenerAlimento
