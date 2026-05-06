import logo from "../assets/FLP_log.png"
import { FaHandPaper } from "react-icons/fa";
import { FaHandHoldingHeart } from "react-icons/fa";
import { MdSell } from "react-icons/md";
import { FiBox } from "react-icons/fi";
import { useNavigate } from 'react-router-dom';


import "./Home.css" 
function Home(){
    const navigate = useNavigate()
    return(
        <div className="home-page">
            <header className="home-header">
                <div className="brand-block">
                    <img src={logo} alt="Food Loop Box" className="brand-logo" />
                    <div>
                        <h2>Food Loop Box</h2>
                        <p>Red local contra el desperdicio</p>
                    </div>
                </div>
                <button className="login-btn" type="button">Iniciar Sesion</button>
            </header>

            <main className="home-main">
                <section className="hero-card">
                    <img src={logo} alt="Food Loop Box" className="logo" />
                    <h1>Food Loop Box</h1>
                    <p>Lo que sobra, alimenta. Dona, comparte, recupera y mueve alimentos en tu comunidad.</p>
                </section>

                <section className="actions-card">
                    <h3>Que deseas hacer hoy?</h3>
                    <div className="actions-grid">
                        <button className="boton1" onClick={()=>navigate('/obtener')}><FaHandPaper /> Obtener Alimento</button>
                        <button className="boton2" onClick={()=>navigate('/donar')}><FaHandHoldingHeart /> Donar Alimento</button>
                        <button className="boton1" onClick={()=>navigate('/vender')}><MdSell /> Vender Alimento</button>
                        <button className="boton2" onClick={()=>navigate('/reclamar')}><FiBox /> Reclamar Alimento</button>
                    </div>
                </section>
            </main>
        </div>
    )
}

export default Home