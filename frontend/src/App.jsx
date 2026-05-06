import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import DonarAlimento from './pages/DonarAlimento'
import ObtenerAlimento from './pages/ObtenerAlimento'
import ReclamarAlimento from './pages/ReclamarAlimento'
import VenderAlimento from './pages/VenderAlimento'
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/obtener" element={<ObtenerAlimento />} />
        <Route path="/donar" element={<DonarAlimento />} />
        <Route path="/vender" element={<VenderAlimento />} />
        <Route path="/reclamar" element={<ReclamarAlimento />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App