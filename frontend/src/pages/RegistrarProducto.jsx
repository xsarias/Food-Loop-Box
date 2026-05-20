import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './RegistrarProducto.css'

const UNITS = [
  { value: 'kg', label: 'Kilogramos (kg)' },
  { value: 'g', label: 'Gramos (g)' },
  { value: 'L', label: 'Litros (L)' },
  { value: 'ml', label: 'Mililitros (ml)' },
  { value: 'unit', label: 'Unidad' },
]

const INITIAL = {
  name: '',
  category: '',
  provider: '',
  description: '',
  quantity: '',
  unit: 'kg',
  original_price: '',
  discounted_price: '',
  expiration_date: '',
  compartment: '',
  notes: '',
  image: null,
}

function RegistrarProducto({ tipo }) {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()

  const isSale = tipo === 'sale'
  const title = isSale ? 'Vender Alimento' : 'Donar Alimento'
  const submitLabel = isSale ? 'Publicar oferta' : 'Registrar donación'
  const backPath = isSale ? '/vender' : '/donar'

  const [form, setForm] = useState(INITIAL)
  const [categories, setCategories] = useState([])
  const [partners, setPartners] = useState([])
  const [compartments, setCompartments] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    Promise.all([
      api.get('/products/categories/'),
      api.get('/core/partners/'),
      api.get('/core/compartments/?status=available'),
    ]).then(([cats, parts, comps]) => {
      setCategories(cats.data.results ?? [])
      setPartners(parts.data.results ?? [])
      setCompartments(comps.data.results ?? [])
    }).catch(() => {})
  }, [isAuthenticated, navigate])

  const discountPct =
    form.original_price && form.discounted_price
      ? Math.max(0, Math.round((1 - form.discounted_price / form.original_price) * 100))
      : 0

  const handleChange = (e) => {
    const { name, value, files } = e.target
    setError('')
    if (name === 'image') {
      setForm((prev) => ({ ...prev, image: files[0] ?? null }))
    } else {
      setForm((prev) => ({ ...prev, [name]: value }))
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const payload = new FormData()
      payload.append('name', form.name)
      payload.append('category', form.category)
      payload.append('provider', form.provider)
      payload.append('product_type', tipo)
      payload.append('quantity', form.quantity)
      payload.append('unit', form.unit)
      payload.append('expiration_date', new Date(form.expiration_date).toISOString())
      if (form.description) payload.append('description', form.description)
      if (form.notes) payload.append('notes', form.notes)
      if (form.compartment) payload.append('compartment', form.compartment)
      if (form.image) payload.append('image', form.image)

      if (isSale) {
        payload.append('original_price', form.original_price)
        payload.append('discounted_price', form.discounted_price)
        payload.append('discount_percentage', discountPct)
      }

      await api.post('/products/products/', payload, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setSuccess(true)
    } catch (err) {
      const data = err.response?.data
      if (data && typeof data === 'object') {
        const first = Object.entries(data)[0]
        setError(`${first[0]}: ${Array.isArray(first[1]) ? first[1][0] : first[1]}`)
      } else {
        setError('No se pudo registrar el producto. Intenta de nuevo.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleNuevo = () => {
    setForm(INITIAL)
    setSuccess(false)
  }

  if (success) {
    return (
      <div className="reg-page">
        <div className="reg-success-card">
          <span className="success-icon">{isSale ? '🛒' : '🤝'}</span>
          <h2>¡{isSale ? 'Oferta publicada' : 'Donación registrada'}!</h2>
          <p>El producto ya está disponible en el sistema.</p>
          <div className="success-actions">
            <button className="reg-btn-primary" onClick={handleNuevo}>
              Registrar otro
            </button>
            <button className="reg-btn-secondary" onClick={() => navigate('/obtener')}>
              Ver productos
            </button>
            <button className="reg-btn-secondary" onClick={() => navigate('/')}>
              Inicio
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="reg-page">
      <header className="reg-header">
        <div className="reg-brand">
          <img className="brand-icon" src="/LOGOflb.png" alt="Food Loop Box" />
          <div>
            <h2>Food Loop Box</h2>
            <p>{isSale ? 'Venta de excedentes' : 'Donación de alimentos'}</p>
          </div>
        </div>
        <button className="back-btn" onClick={() => navigate('/')}>← Inicio</button>
      </header>

      <main className="reg-main">
        <div className="reg-title-row">
          <h1>{title}</h1>
          <p>
            {isSale
              ? 'Publica excedentes a precio justo para reducir el desperdicio.'
              : 'Registra alimentos en buen estado para que otros los aprovechen.'}
          </p>
        </div>

        <form className="reg-form" onSubmit={handleSubmit}>

          {/* Información básica */}
          <div className="form-section">
            <h3 className="section-title">Información del producto</h3>

            <div className="field-group full">
              <label htmlFor="name">Nombre del producto *</label>
              <input
                id="name" name="name" type="text"
                value={form.name} onChange={handleChange}
                placeholder="Ej: Pechuga de pollo fresca"
                required
              />
            </div>

            <div className="form-row">
              <div className="field-group">
                <label htmlFor="category">Categoría *</label>
                <select id="category" name="category" value={form.category} onChange={handleChange} required>
                  <option value="">Selecciona una categoría</option>
                  {categories.map((c) => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>

              <div className="field-group">
                <label htmlFor="provider">Proveedor / Aliado *</label>
                <select id="provider" name="provider" value={form.provider} onChange={handleChange} required>
                  <option value="">Selecciona un aliado</option>
                  {partners.map((p) => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="field-group full">
              <label htmlFor="description">Descripción</label>
              <textarea
                id="description" name="description"
                value={form.description} onChange={handleChange}
                placeholder="Descripción del producto, estado, características..."
                rows={3}
              />
            </div>
          </div>

          {/* Cantidad y unidad */}
          <div className="form-section">
            <h3 className="section-title">Cantidad y vencimiento</h3>

            <div className="form-row">
              <div className="field-group">
                <label htmlFor="quantity">Cantidad *</label>
                <input
                  id="quantity" name="quantity" type="number"
                  value={form.quantity} onChange={handleChange}
                  placeholder="1.5" min="0.01" step="0.01" required
                />
              </div>

              <div className="field-group">
                <label htmlFor="unit">Unidad *</label>
                <select id="unit" name="unit" value={form.unit} onChange={handleChange} required>
                  {UNITS.map((u) => (
                    <option key={u.value} value={u.value}>{u.label}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="field-group full">
              <label htmlFor="expiration_date">Fecha y hora de vencimiento *</label>
              <input
                id="expiration_date" name="expiration_date" type="datetime-local"
                value={form.expiration_date} onChange={handleChange}
                required
              />
            </div>
          </div>

          {/* Precio (solo venta) */}
          {isSale && (
            <div className="form-section">
              <h3 className="section-title">Precio</h3>

              <div className="form-row">
                <div className="field-group">
                  <label htmlFor="original_price">Precio original (COP) *</label>
                  <input
                    id="original_price" name="original_price" type="number"
                    value={form.original_price} onChange={handleChange}
                    placeholder="45000" min="0" required={isSale}
                  />
                </div>

                <div className="field-group">
                  <label htmlFor="discounted_price">Precio con descuento (COP) *</label>
                  <input
                    id="discounted_price" name="discounted_price" type="number"
                    value={form.discounted_price} onChange={handleChange}
                    placeholder="22500" min="0" required={isSale}
                  />
                </div>
              </div>

              {discountPct > 0 && (
                <p className="discount-hint">
                  Descuento calculado: <strong>{discountPct}%</strong>
                </p>
              )}
            </div>
          )}

          {/* Almacenamiento */}
          <div className="form-section">
            <h3 className="section-title">Almacenamiento (opcional)</h3>

            <div className="form-row">
              <div className="field-group">
                <label htmlFor="compartment">Compartimiento Food Loop Box</label>
                <select id="compartment" name="compartment" value={form.compartment} onChange={handleChange}>
                  <option value="">Sin asignar</option>
                  {compartments.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.device_name} — #{c.compartment_number}
                    </option>
                  ))}
                </select>
              </div>

              <div className="field-group">
                <label htmlFor="image">Foto del producto</label>
                <input
                  id="image" name="image" type="file"
                  accept="image/*" onChange={handleChange}
                  className="file-input"
                />
              </div>
            </div>

            <div className="field-group full">
              <label htmlFor="notes">Notas adicionales</label>
              <textarea
                id="notes" name="notes"
                value={form.notes} onChange={handleChange}
                placeholder="Información adicional relevante..."
                rows={2}
              />
            </div>
          </div>

          {error && <p className="reg-error">{error}</p>}

          <div className="form-actions">
            <button type="button" className="reg-btn-secondary" onClick={() => navigate('/')}>
              Cancelar
            </button>
            <button type="submit" className="reg-btn-primary" disabled={loading}>
              {loading ? 'Registrando…' : submitLabel}
            </button>
          </div>
        </form>
      </main>
    </div>
  )
}

export default RegistrarProducto
