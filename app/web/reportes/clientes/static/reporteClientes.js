function generarReporteClientes(tipo){
    var url;
    
    url = '../api/reportes/reporteClientes/generar?tipo='+tipo;
    
    // window.location.href = url;
    window.open(url,'_blank')
}


