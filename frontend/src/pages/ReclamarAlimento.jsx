import ActionPage from "./ActionPage";

function ReclamarAlimento(){
    return(
        <ActionPage
            title="Reclamar Alimento"
            subtitle="Confirma una solicitud y coordina la entrega de forma clara para que los alimentos lleguen a destino."
            tags={["Solicitudes", "Entrega", "Seguimiento"]}
            ctaPrimary="Reclamar lote"
            ctaSecondary="Historial"
        />
    )
}
export default ReclamarAlimento