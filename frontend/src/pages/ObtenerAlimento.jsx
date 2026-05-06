import ActionPage from "./ActionPage";

function ObtenerAlimento(){
    return(
        <ActionPage
            title="Obtener Alimento"
            subtitle="Encuentra alimentos disponibles cerca de ti y organiza una recoleccion rapida para reducir perdidas."
            tags={["Busqueda local", "Recoleccion", "Disponibilidad"]}
            ctaPrimary="Buscar opciones"
            ctaSecondary="Filtrar por zona"
        />
    )
}

export default ObtenerAlimento