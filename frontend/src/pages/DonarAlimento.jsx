import ActionPage from "./ActionPage";

function DonarAlimento(){
    return(
        <ActionPage
            title="Donar Alimento"
            subtitle="Publica productos que aun estan en buen estado para que otras personas o fundaciones puedan recibirlos a tiempo."
            tags={["Comunidad", "Aprovechamiento", "Solidaridad"]}
            ctaPrimary="Publicar donacion"
            ctaSecondary="Ver solicitudes"
        />
    )
}
export default DonarAlimento