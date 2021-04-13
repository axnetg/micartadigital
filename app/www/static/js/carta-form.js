(function($) {
    $.fn.djangoFormset.Form.prototype.getDeleteButton = function () {
        return $('<button type="button" class="ui icon button"><i class="trash icon"></i></button>');
    };

    var $seccionFormset = $("div.seccion").djangoFormset({
        on: {
            formInitialized: function (event, form) {
                /* Init inner formset */
                var $platoFormsetContainer = form.elem.children('table').first();
                var $platoFormset = $platoFormsetContainer.find('tbody tr').djangoFormset();
                var $addNewPlatoButton = $platoFormsetContainer.siblings('[data-action=add-plato-form]');

                $addNewPlatoButton.on('click', function (event) {
                    $platoFormset.addForm();
                    $('.ui.dropdown.selection').dropdown({useLabels: false});
                });
            }
        }
    });
    /* Add new outer form on add button click */
    $('form').on('click', '[data-action=add-seccion-form]', function (event) {
        $seccionFormset.addForm();
        $('.ui.dropdown.selection').dropdown({useLabels: false});
    });
})(jQuery);

function sortSeccionesByOrder() {
    var $secciones = $('form > .ui.segment');

    $secciones.sort(function (secc1, secc2) {
        var orderSecc1 = $(secc1).children('input[name$="orden"]').val();
        var orderSecc2 = $(secc2).children('input[name$="orden"]').val();

        return (parseInt(orderSecc1) < parseInt(orderSecc2) ? -1 : 1);
    });

    $.each($secciones, function (index, div) {
        $('form > button[data-action=add-seccion-form]').before(div);
    });
}

function sortPlatosByOrder() {
    var $secciones = $('form > .ui.segment');

    $secciones.each(function () {
        var $seccion = $(this);
        var $platos = $seccion.children('table').find('tbody tr').get();

        $platos.sort(function (row1, row2) {
            var orderRow1 = $(row1).find('input[name$="orden"]').val();
            var orderRow2 = $(row2).find('input[name$="orden"]').val();

            return (parseInt(orderRow1) < parseInt(orderRow2) ? -1 : 1);
        });

        $.each($platos, function (index, row) {
            $seccion.children('table').find('tbody').append(row);
        });
    });
}