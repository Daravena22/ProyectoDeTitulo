function generarReporteVentas() {
    var url;


    fecha_desde = document.getElementById('fecha_desde').value
    fecha_hasta = document.getElementById('fecha_hasta').value
    url = '../api/reportes/reporteVentas/generar?fecha_desde='+fecha_desde+'&fecha_hasta='+fecha_hasta;

    // window.location.href = url;
    window.open(url, '_blank')
}