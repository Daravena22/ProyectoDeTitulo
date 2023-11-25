function generarReporteVentas() {
    var url;


    fecha_desde = document.getElementById('fecha_desde').value
    fecha_hasta = document.getElementById('fecha_hasta').value

    if(!isValidDate(fecha_desde)||!isValidDate(fecha_hasta)){

        toastr.warning('Debe ingresar un rango fecha para generar reporte')
        return
    }

    url = '../api/reportes/reporteVentas/generar?fecha_desde='+fecha_desde+'&fecha_hasta='+fecha_hasta;

    // window.location.href = url;
    window.open(url, '_blank')
}

function isValidDate(dateString) {
    var regEx = /^\d{4}-\d{2}-\d{2}$/;
    if(!dateString.match(regEx)) return false;  // Invalid format
    var d = new Date(dateString);
    var dNum = d.getTime();
    if(!dNum && dNum !== 0) return false; // NaN value, Invalid date
    return d.toISOString().slice(0,10) === dateString;
  }