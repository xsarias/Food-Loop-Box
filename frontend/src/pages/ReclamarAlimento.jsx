import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import './ReclamarAlimento.css'

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('es-CO', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

function timeLeft(dateStr) {
  const diff = new Date(dateStr) - Date.now()
  if (diff <= 0) return 'Expirada'
  const hours = Math.floor(diff / 3_600_000)
  if (hours < 24) return `Vence en ${hours}h`
  return `Vence en ${Math.floor(hours / 24)}d`
}

const STATUS_LABEL = {
  active: 'Activa',
  completed: 'Completada',
  cancelled: 'Cancelada',
  expired: 'Expirada',
  pending: 'Pendiente',
  failed: 'Fallida',
}

/* ── Tarjeta de reserva ── */
function ReservationCard({ reservation, onCancel, cancelling }) {
  const isActive = reservation.status === 'active'
  const expiring = isActive && new Date(reservation.expiration_date) - Date.now() < 8 * 3_600_000

  return (
    <div className={`claim-card ${!isActive ? 'card-inactive' : ''}`}>
      <div className="claim-card-top">
        <div>
          <h3 className="claim-product">{reservation.product_name}</h3>
          <span className={`status-chip status-${reservation.status}`}>
            {STATUS_LABEL[reservation.status] ?? reservation.status}
          </span>
        </div>
        {isActive && (
          <button
            className="cancel-btn"
            onClick={() => onCancel(reservation.id)}
            disabled={cancelling === reservation.id}
          >
            {cancelling === reservation.id ? 'Cancelando…' : 'Cancelar'}
          </button>
        )}
      </div>

      <div className="claim-meta">
        <span>Reservado: {formatDate(reservation.reservation_date)}</span>
        {isActive && (
          <span className={expiring ? 'text-warn' : ''}>
            ⏱ {timeLeft(reservation.expiration_date)}
          </span>
        )}
      </div>
    </div>
  )
}

/* ── Tarjeta de compra ── */
function TransactionCard({ transaction }) {
  const [code, setCode] = useState(null)
  const [loadingCode, setLoadingCode] = useState(false)
  const [showCode, setShowCode] = useState(false)

  const fetchCode = async () => {
    if (code) { setShowCode(true); return }
    setLoadingCode(true)
    try {
      const { data } = await api.get(`/transactions/transactions/${transaction.id}/`)
      setCode(data.withdrawal_code)
      setShowCode(true)
    } catch {
      setCode('Error al obtener código')
      setShowCode(true)
    } finally {
      setLoadingCode(false)
    }
  }

  return (
    <div className="claim-card">
      <div className="claim-card-top">
        <div>
          <h3 className="claim-product">{transaction.product_name}</h3>
          <span className={`status-chip status-${transaction.status}`}>
            {STATUS_LABEL[transaction.status] ?? transaction.status}
          </span>
        </div>
        {transaction.status === 'completed' && (
          <button className="code-btn" onClick={fetchCode} disabled={loadingCode}>
            {loadingCode ? 'Cargando…' : showCode ? 'Ocultar código' : 'Ver código'}
          </button>
        )}
      </div>

      {showCode && code && (
        <div className="withdrawal-code-box">
          <p className="code-label">Código de retiro</p>
          <p className="code-value">{code}</p>
          <p className="code-hint">Muéstralo en la pantalla del locker para retirar tu producto.</p>
        </div>
      )}

      <div className="claim-meta">
        <span>Método: {transaction.payment_method}</span>
        <span>Fecha: {formatDate(transaction.created_at)}</span>
      </div>
    </div>
  )
}

/* ── Página principal ── */
function ReclamarAlimento() {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()

  const [reservations, setReservations] = useState([])
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)
  const [cancelling, setCancelling] = useState(null)
  const [toast, setToast] = useState(null)
  const [tab, setTab] = useState('reservas')

  useEffect(() => {
    if (!isAuthenticated) { navigate('/login'); return }
    Promise.all([
      api.get('/transactions/reservations/'),
      api.get('/transactions/transactions/'),
    ]).then(([res, trx]) => {
      setReservations(res.data.results ?? [])
      setTransactions(trx.data.results ?? [])
    }).catch(() => {}).finally(() => setLoading(false))
  }, [isAuthenticated, navigate])

  const showToast = (msg, isError = false) => {
    setToast({ msg, isError })
    setTimeout(() => setToast(null), 3000)
  }

  const handleCancel = async (id) => {
    setCancelling(id)
    try {
      await api.post(`/transactions/reservations/${id}/cancel/`)
      setReservations((prev) =>
        prev.map((r) => r.id === id ? { ...r, status: 'cancelled' } : r)
      )
      showToast('Reserva cancelada.')
    } catch (err) {
      showToast(err.response?.data?.detail || 'No se pudo cancelar.', true)
    } finally {
      setCancelling(null)
    }
  }

  const activeReservations = reservations.filter((r) => r.status === 'active')
  const otherReservations = reservations.filter((r) => r.status !== 'active')

  return (
    <div className="reclamar-page">
      <header className="reclamar-header">
        <div className="reclamar-brand">
          <div className="brand-icon">FLB</div>
          <div>
            <h2>Food Loop Box</h2>
            <p>Mis pedidos</p>
          </div>
        </div>
        <button className="back-btn" onClick={() => navigate('/')}>← Inicio</button>
      </header>

      <main className="reclamar-main">
        <div className="reclamar-title-row">
          <h1>Reclamar Alimento</h1>
          <p>Gestiona tus reservas y compras. Usa el código de retiro en el locker.</p>
        </div>

        {/* Tabs */}
        <div className="tabs">
          <button
            className={`tab-btn ${tab === 'reservas' ? 'active' : ''}`}
            onClick={() => setTab('reservas')}
          >
            Reservas
            {activeReservations.length > 0 && (
              <span className="tab-badge">{activeReservations.length}</span>
            )}
          </button>
          <button
            className={`tab-btn ${tab === 'compras' ? 'active' : ''}`}
            onClick={() => setTab('compras')}
          >
            Compras
            {transactions.length > 0 && (
              <span className="tab-badge">{transactions.length}</span>
            )}
          </button>
        </div>

        {loading && (
          <div className="state-box">
            <div className="spinner" />
            <p>Cargando…</p>
          </div>
        )}

        {!loading && tab === 'reservas' && (
          <>
            {reservations.length === 0 ? (
              <div className="state-box">
                <span className="empty-icon">📦</span>
                <p>No tienes reservas aún.</p>
                <button className="go-btn" onClick={() => navigate('/obtener')}>
                  Ver productos disponibles
                </button>
              </div>
            ) : (
              <div className="cards-list">
                {activeReservations.length > 0 && (
                  <>
                    <p className="section-label">Activas ({activeReservations.length})</p>
                    {activeReservations.map((r) => (
                      <ReservationCard
                        key={r.id}
                        reservation={r}
                        onCancel={handleCancel}
                        cancelling={cancelling}
                      />
                    ))}
                  </>
                )}
                {otherReservations.length > 0 && (
                  <>
                    <p className="section-label">Historial</p>
                    {otherReservations.map((r) => (
                      <ReservationCard
                        key={r.id}
                        reservation={r}
                        onCancel={handleCancel}
                        cancelling={cancelling}
                      />
                    ))}
                  </>
                )}
              </div>
            )}
          </>
        )}

        {!loading && tab === 'compras' && (
          <>
            {transactions.length === 0 ? (
              <div className="state-box">
                <span className="empty-icon">🛒</span>
                <p>No tienes compras aún.</p>
                <button className="go-btn" onClick={() => navigate('/obtener')}>
                  Ver productos disponibles
                </button>
              </div>
            ) : (
              <div className="cards-list">
                {transactions.map((t) => (
                  <TransactionCard key={t.id} transaction={t} />
                ))}
              </div>
            )}
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

export default ReclamarAlimento
