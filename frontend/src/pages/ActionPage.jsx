import { useNavigate } from "react-router-dom";
import logo from "../assets/FLP_log.png";
import "./ActionPage.css";

function ActionPage({ title, subtitle, tags, ctaPrimary, ctaSecondary }) {
  const navigate = useNavigate();

  return (
    <div className="action-page">
      <header className="action-header">
        <div className="action-brand">
          <img src={logo} alt="Food Loop Box" className="action-brand-logo" />
          <div>
            <h2>Food Loop Box</h2>
            <p>Interfaz inicial</p>
          </div>
        </div>

        <div className="action-head-buttons">
          <button type="button" className="head-btn">Iniciar Sesion</button>
          <button type="button" className="head-btn home" onClick={() => navigate("/")}>Inicio</button>
        </div>
      </header>

      <main className="action-main">
        <section className="action-card">
          <h1>{title}</h1>
          <p>{subtitle}</p>

          <div className="tag-list">
            {tags.map((tag) => (
              <span key={tag} className="tag-item">{tag}</span>
            ))}
          </div>

          <div className="cta-block">
            <button type="button" className="action-cta primary">{ctaPrimary}</button>
            <button type="button" className="action-cta secondary">{ctaSecondary}</button>
          </div>

          <small>Vista de interfaz por ahora. Los botones no tienen logica conectada.</small>
        </section>
      </main>
    </div>
  );
}

export default ActionPage;