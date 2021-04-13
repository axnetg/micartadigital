(function($) {
    $('.ui.dropdown:not(.selection)').dropdown();

    $('.tabular.menu .item').tab();

    $('.message .close').on('click', function () {
        $(this).closest('.message').transition('fade');
    });
})(jQuery);