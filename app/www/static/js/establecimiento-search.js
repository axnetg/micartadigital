(function($) {
    /* Filtrado de resultados por localidad cuando el resultado de búsqueda devuelva establecimientos de varias localidades */
    var $localidadFilterSelectors = $('#localidad-filter .label');
    var $searchResults = $('#search-results-wrapper .items');
    var activeClass = 'violet';
    
    /* Hacer click en una localidad aplica el filtro y se muestran solo los establecimientos de la localidad seleccionada */
    $localidadFilterSelectors.on('click', function () {
        var $label = $(this);
        /* Quitar clase activa a todas las localidades excepto la seleccionada */
        $localidadFilterSelectors.not($label).each(function () {
            $(this).removeClass(activeClass);
        });

        /* Conmutar la clase activa de la localidad seleccionada (por si se quiere volver a la vista sin filtrar) */
        $label.toggleClass(activeClass);
        var localidad = $label.hasClass(activeClass) ? $label.attr('data-localidad') : '';
        
        /* Por cada resultado de búsqueda, mostramos/ocultamos según el valor de localidad seleccionado */
        $searchResults.each(function () {
            var $item = $(this);
            if (!localidad || $item.attr('data-localidad') == localidad) {
                $item.show();
            } else {
                $item.hide();
            }
        })
    });
})(jQuery);