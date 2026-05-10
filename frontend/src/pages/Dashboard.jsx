import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './Dashboard.css'

const fmt = (n) => Number(n ?? 0).toLocaleString('es-CO')
const fmtKg = (n) => `${Number(n ?? 0).toFixed(1)} kg`
const fmtCOP = (n) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(n ?? 0)

function KpiCard({ icon, label, value, sub }) {
  return (
    <div className="kpi-card">
      <span className="kpi-icon">{icon}</span>
      <p className="kpi-value">{value}</p>
      <p className="kpi-label">{label}</p>
      {sub && <p className="kpi-sub">{sub}</p>}
    </div>
  )
}

function Dashboard() {
  const navigate = useNavigate()
  const { user, isAuthenticated } = useAuth()

  const [overview, setOverview] = useState(null)
  const [products, setProducts] = useState({ total: 0, donation: 0, sale: 0, expiring: 0 })
  const [loading, setLoading] = useState(true)
  const [forbidden, setForbidden] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login'); return }

    Promise.all([
      api.get('/analytics/dashboard/overview/'),
      api.get('/products/products/?only_available=true'),
      api.get('/products/products/?only_available=true&product_type=donation'),
      api.get('/products/products/?only_available=true&product_type=sale'),
      api.get('/products/products/expiring_soon/'),
    ])
      .then(([ov, all, don, sal, exp]) => {
        setOverview(ov.data)
        setProducts({
          total: all.data.count ?? 0,
          donation: don.data.count ?? 0,
          sale: sal.data.count ?? 0,
          expiring: exp.data.count ?? 0,
        })
      })
      .catch((err) => {
        if (err.response?.status === 403) setForbidden(true)
      })
      .finally(() => setLoading(false))
  }, [isAuthenticated, navigate])

  if (!isAuthenticated) return null

  if (forbidden) {
    return (
      <div className="dash-page">
        <div className="forbidden-box">
          <span>🔒</span>
          <h2>Acceso restringido</h2>
          <p>Esta sección es solo para administradores.</p>
          <button className="back-btn" onClick={() => navigate('/')}>← Volver al inicio</button>
        </div>
      </div>
    )
  }

  const week = overview?.this_week ?? {}
  const today = overview?.today ?? {}
  const impact = overview?.environmental_impact
  const topPartners = overview?.top_partners ?? []
  const topLocations = overview?.top_locations ?? []

  return (
    <div className="dash-page">
      <header className="dash-header">
        <div className="dash-brand">
          <div className="brand-icon">FLB</div>
          <div>
            <h2>Food Loop Box</h2>
            <p>Panel de administración</p>
          </div>
        </div>
        <button className="back-btn" onClick={() => navigate('/')}>← Inicio</button>
      </header>

      <main className="dash-main">
        <div className="dash-title-row">
          <h1>Dashboard de Impacto</h1>
          <p>Resumen de actividad y métricas del sistema</p>
        </div>

        {loading ? (
          <div className="state-box">
            <div className="spinner" />
            <p>Cargando métricas…</p>
          </div>
        ) : (
          <>
            {/* KPIs semana */}
            <section className="dash-section">
              <h2 className="section-title">Esta semana</h2>
              <div className="kpi-grid">
                <KpiCard icon="📦" label="Productos registrados" value={fmt(week.total_products)} />
                <KpiCard icon="⚖️" label="Peso rescatado" value={fmtKg(week.total_weight)} />
                <KpiCard icon="🛒" label="Transacciones" value={fmt(week.total_transactions)} />
                <KpiCard icon="💰" label="Ingresos" value={fmtCOP(week.total_amount)} />
              </div>
            </section>

            {/* Productos en tiempo real */}
            <section className="dash-section">
              <h2 className="section-title">Productos disponibles ahora</h2>
              <div className="kpi-grid">
                <KpiCard icon="🥗" label="Disponibles" value={fmt(products.total)} />
                <KpiCard icon="🤝" label="Donaciones" value={fmt(products.donation)} />
                <KpiCard icon="🏷️" label="En venta" value={fmt(products.sale)} />
                <KpiCard
                  icon="⚠️"
                  label="Vencen pronto"
                  value={fmt(products.expiring)}
                  sub="Menos de 24h"
                />
              </div>
            </section>

            {/* Hoy */}
            <section className="dash-section">
              <h2 className="section-title">Hoy</h2>
              <div className="today-grid">
                <div className="today-item">
                  <span className="today-val">{fmt(today.total_products_registered)}</span>
                  <span className="today-label">Registrados</span>
                </div>
                <div className="today-item">
                  <span className="today-val">{fmt(today.total_products_donated)}</span>
                  <span className="today-label">Donados</span>
                </div>
                <div className="today-item">
                  <span className="today-val">{fmt(today.total_products_sold)}</span>
                  <span className="today-label">Vendidos</span>
                </div>
                <div className="today-item">
                  <span className="today-val">{fmt(today.total_products_expired)}</span>
                  <span className="today-label">Vencidos</span>
                </div>
                <div className="today-item">
                  <span className="today-val">{fmt(today.new_users)}</span>
                  <span className="today-label">Nuevos usuarios</span>
                </div>
                <div className="today-item">
                  <span className="today-val">{fmt(today.active_users)}</span>
                  <span className="today-label">Usuarios activos</span>
                </div>
              </div>
            </section>

            {/* Impacto ambiental */}
            {impact ? (
              <section className="dash-section impact-section">
                <h2 className="section-title">Impacto ambiental acumulado</h2>
                <div className="impact-grid">
                  <div className="impact-card">
                    <span className="impact-icon">🌱</span>
                    <p className="impact-val">{fmtKg(impact.estimated_co2_avoided_kg)}</p>
                    <p className="impact-label">CO₂ evitado</p>
                  </div>
                  <div className="impact-card">
                    <span className="impact-icon">💧</span>
                    <p className="impact-val">{fmt(impact.estimated_water_saved_liters)} L</p>
                    <p className="impact-label">Agua ahorrada</p>
                  </div>
                  <div className="impact-card">
                    <span className="impact-icon">🍽️</span>
                    <p className="impact-val">{fmt(impact.people_fed)}</p>
                    <p className="impact-label">Personas alimentadas</p>
                  </div>
                  <div className="impact-card">
                    <span className="impact-icon">👨‍👩‍👧</span>
                    <p className="impact-val">{fmt(impact.families_supported)}</p>
                    <p className="impact-label">Familias apoyadas</p>
                  </div>
                </div>
              </section>
            ) : (
              <section className="dash-section">
                <h2 className="section-title">Impacto ambiental</h2>
                <p className="empty-hint">Aún no hay reportes de impacto generados.</p>
              </section>
            )}

            {/* Top aliados */}
            <section className="dash-section">
              <h2 className="section-title">Top aliados por peso donado</h2>
              {topPartners.length === 0 ? (
                <p className="empty-hint">Sin datos de aliados aún.</p>
              ) : (
                <div className="rank-table">
                  <div className="rank-header">
                    <span>#</span>
                    <span>Aliado</span>
                    <span>Kg donados</span>
                    <span>Vidas impactadas</span>
                    <span>Ingresos</span>
                  </div>
                  {topPartners.map((p, i) => (
                    <div key={p.id} className="rank-row">
                      <span className="rank-num">{i + 1}</span>
                      <span className="rank-name">{p.partner_name}</span>
                      <span>{fmtKg(p.total_weight_donated)}</span>
                      <span>{fmt(p.lives_impacted)}</span>
                      <span>{fmtCOP(p.total_revenue_from_sales)}</span>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Top ubicaciones */}
            <section className="dash-section">
              <h2 className="section-title">Top ubicaciones por actividad</h2>
              {topLocations.length === 0 ? (
                <p className="empty-hint">Sin datos de ubicaciones aún.</p>
              ) : (
                <div className="rank-table">
                  <div className="rank-header">
                    <span>#</span>
                    <span>Ubicación</span>
                    <span>Kg rescatados</span>
                    <span>Clientes únicos</span>
                    <span>Ingresos</span>
                  </div>
                  {topLocations.map((l, i) => (
                    <div key={l.id} className="rank-row">
                      <span className="rank-num">{i + 1}</span>
                      <span className="rank-name">{l.location_name}</span>
                      <span>{fmtKg(l.total_weight_rescued)}</span>
                      <span>{fmt(l.unique_customers)}</span>
                      <span>{fmtCOP(l.total_revenue)}</span>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  )
}

export default Dashboard
