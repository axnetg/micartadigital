$('a').on('click', function () {
    let idTarget = $(this).data('target');
    if (idTarget !== undefined) {
        window.scrollTo(0, Math.ceil($(idTarget).offset().top) - 12);
    }
});

$('.alergenos.modal').modal('attach events', '.alergenos.open', 'show');


var $goToTopBtn = $('#go-to-top-btn');

$goToTopBtn.on('click', function() {
    $(window).scrollTop(0);
});

$('#establecimiento-detalles').visibility({
    once: false,
    onTopPassed: function() {
        $goToTopBtn.toggle();
    },
    onTopPassedReverse: function() {
        $goToTopBtn.toggle();
    }
});