(function($) {
    $('a').on('click', function () {
        let idTarget = $(this).data('target');
        if (idTarget !== undefined) {
            window.scrollTo(0, Math.ceil($(idTarget).offset().top) - 12);
        }
    });


    var $modalAlergenosInfo = $('.alergenos.modal');
    var $goToTopBtn = $('#go-to-top-btn');
    var $divEstablecimientoDetalles = $('#establecimiento-detalles');
    
    $modalAlergenosInfo.modal('attach events', '.alergenos.open', 'show');
    
    $goToTopBtn.on('click', function() {
        $(window).scrollTop(0);
    });

    $divEstablecimientoDetalles.visibility({
        once: false,
        onTopPassed: function() {
            $goToTopBtn.toggle();
        },
        onTopPassedReverse: function() {
            $goToTopBtn.toggle();
        }
    });
})(jQuery);