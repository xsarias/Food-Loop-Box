import ActionPage from "./ActionPage";

function VenderAlimento(){
    return(
        <ActionPage
            title="Vender Alimento"
            subtitle="Ofrece excedentes a precio justo para evitar desperdicio y recuperar parte de tus costos operativos."
            tags={["Precio justo", "Excedentes", "Comercio local"]}
            ctaPrimary="Crear oferta"
            ctaSecondary="Ver mercado"
        />
    )
}
export default VenderAlimento