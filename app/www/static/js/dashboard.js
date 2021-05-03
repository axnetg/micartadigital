(function($) {
    var $tablaEstablecimientos = $('#table-establecimientos');
    var $tablaCartas = $('#table-cartas');

    var spanishDatatablesStrings = "https://cdn.datatables.net/plug-ins/1.10.22/i18n/Spanish.json";

    
    $tablaEstablecimientos.DataTable({
        language: {
            url: spanishDatatablesStrings
        },
        paging: false,
        pageLength: 3,
        lengthChange: false,
        info: false,
        autoWidth: false,
        columnDefs: [
            { type: "html", targets: [0, 3] },
            { width: "50%", targets: 0 },
            { orderable: false, targets: -1 },
            { searchable: false, targets: -1 }
        ]
    });

    $tablaCartas.DataTable({
        language: {
            url: spanishDatatablesStrings
        },
        paging: false,
        pageLength: 3,
        lengthChange: false,
        info: false,
        autoWidth: false,
        columnDefs: [
            { type: "html", targets: [0, 1] },
            { width: "25%", targets: [0, 2] },
            { orderable: false, targets: [1, -1] },
            { searchable: false, targets: -1 }
        ]
    });


    // modal de confirmación de eliminación de establecimientos y cartas
    var $modal = $('.ui.modal');
    var $modalForm = $modal.find('form');
    var $confirmDeletionCheckbox = $modalForm.find('input[type="checkbox"');
    var $confirmDeletionSubmitButton = $modalForm.find('input[type="submit"]');
    var $establecimientoText = $modal.find('#is-establecimiento');
    var $cartaText = $modal.find('#is-carta');
    var $cartaTextWarning = $modal.find('#is-carta-warning');

    // coloca form.action adecuado, resetea el checkbox, coloca el título en el texto y abre el modal
    var callbackDeleteBtn = ($button) => {
        var actionUrl = $button.attr('data-url');
        var objectName = $button.attr('data-nombre');

        $modalForm.attr('action', actionUrl);
        $confirmDeletionCheckbox.prop('checked', false);
        $confirmDeletionSubmitButton.addClass('disabled');

        $modal.find('.delete-confirm-title').text(objectName);
        $modal.modal('show');
    };

    // prepara el modal para mostrarse con la información de establecimiento
    $('.delete-establecimiento-btn').on('click', function () {
        $establecimientoText.show();
        $cartaText.hide();
        callbackDeleteBtn($(this));
    });

    // prepara el modal para mostrarse con la información de carta
    $('.delete-carta-btn').on('click', function () {
        var $clickedBtn = $(this);
        var related = $clickedBtn.data('related');
        
        if (related.length > 0) {
            $cartaTextWarning.show();
            var $list = $cartaTextWarning.find('ul');
            $list.empty();
            related.forEach(el => {
               $list.append(`<li>${el}</li>`);
            });
        } else {
            $cartaTextWarning.hide();
        }
    
        $cartaText.show();
        $establecimientoText.hide();
        callbackDeleteBtn($clickedBtn);
    });

    // hacer click sobre el checkbox deshabilita o habilita el botón de eliminar
    $confirmDeletionCheckbox.on('click', function() {
        $confirmDeletionSubmitButton.toggleClass('disabled');
    });
})(jQuery);