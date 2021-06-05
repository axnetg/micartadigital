(function($) {
    /* Establecer configuraciones (texto y conteo) del dropdown de alérgenos */
    $.fn.dropdown.settings.message.count = 'Alérgenos: {count}';
    $('.ui.selection.dropdown').dropdown({
        placeholder: 'Seleccionar alérgenos',
        useLabels: false
    });

    /* Inicializar plugin para el render de los formsets de secciones y de platos */
    var $secciones = $('div.seccion');
    var $seccionFormset = $secciones.djangoFormset({
        on: {
            formInitialized: function (event, form) {
                /* Inicializar los formsets de plato anidados en cada sección */
                var $seccionContainer = form.elem;
                var $platoFormset = $seccionContainer.find('div.plato').djangoFormset();

                /* Añadir nuevo form al formset de platos al pulsar sobre el botón de nuevo plato */
                var $addNewPlatoButton = $seccionContainer.find('[data-action=add-plato-form]');
                $addNewPlatoButton.on('click', function (event) {
                    var newInnerForm = $platoFormset.addForm();
                    var $newPlato = newInnerForm.elem;

                    /* Colocar este $newPlato al final de la lista de platos.
                    * Motivo: el plugin de formsets mantiene en memoria una estructura de datos
                    * que hace que al añadir un nuevo form al formset lo hace justo después
                    * del último form inicializado (mediante un insertAfter()).
                    * Esto da conflictos si se permite reordenar los forms. */
                    var $wrapper = $newPlato.closest('.wrapper-seccion-platos');
                    $wrapper.append($newPlato);

                    $newPlato.find('.ui.dropdown.selection').dropdown({useLabels: false});
                });
            }
        }
    });

    /* Reordenar los tabs de secciones _después_ de haber inicializado el plugin de formsets */
    var $seccionesMenu = $('#secciones-switcher');
    var $seccionesTab = $seccionesMenu.find('.item');

    $seccionesTab.sort(function (tab1, tab2) {
        var dataTabString1 = $(tab1).attr('data-tab');
        var $secc1 = $secciones.filter(`[data-tab=${dataTabString1}]`);
        var orderSecc1 = $secc1.find('.wrapper-seccion input[name$="orden"]').val();
        
        var dataTabString2 = $(tab2).attr('data-tab');
        var $secc2 = $secciones.filter(`[data-tab=${dataTabString2}]`);
        var orderSecc2 = $secc2.find('input[name$="orden"]').val();

        return (parseInt(orderSecc1) < parseInt(orderSecc2) ? -1 : 1);
    });

    $.each($seccionesTab, function (index, div) {
        $seccionesMenu.append(div);
    });

    /* Reordenar los platos _después_ de haber inicializado el plugin de formsets */
    $secciones.each(function () {
        var $seccion = $(this);
        var $platos = $seccion.find('div.plato');

        $platos.sort(function (row1, row2) {
            var orderRow1 = $(row1).find('input[name$="orden"]').val();
            var orderRow2 = $(row2).find('input[name$="orden"]').val();

            return (parseInt(orderRow1) < parseInt(orderRow2) ? -1 : 1);
        });

        $.each($platos, function (index, row) {
            $seccion.find('.wrapper-seccion-platos').append(row);
        });
    });

    /* Colocar como activo el primer tab (tras la ordenación) de una sección _visible_ */
    $seccionesTab.first().click();

    /* Inicializar plugin SortableJS para la reordenación de platos y secciones */
    var seccionSortOptions = {
        delay: 100,
        delayOnTouchOnly: true,
        animation: 250,
        easing: 'cubic-bezier(0.37, 0, 0.63, 1)',
        ghostClass: 'ghost',
        swapThreshold: 0.5,
    };
    var platoSortOptions = {
        animation: 250,
        easing: 'cubic-bezier(0.37, 0, 0.63, 1)',
        handle: '.sortable-handler',
        ghostClass: 'ghost',
        swapThreshold: 0.5,
    };

    Sortable.create($seccionesMenu[0], seccionSortOptions);
    
    $secciones.each(function () {
        var wrapperPlatoElement = $(this).find('.wrapper-seccion-platos')[0];
        Sortable.create(wrapperPlatoElement, platoSortOptions);
    });

    /* Añadir nuevo form al formset de secciones tras pulsar sobre el botón de nueva sección */
    var $form = $('form');
    $form.on('click', '[data-action=add-seccion-form]', function (event) {
        var $newSeccion = $seccionFormset.addForm().elem;
        var index = $newSeccion.prev().attr('data-tab').replace('secciones-', '');

        var dataTabString = $newSeccion.attr('data-tab').replace('__prefix__', parseInt(index) + 1);
        $newSeccion.attr('data-tab', dataTabString);

        var $newItem = $('<a class="item">sin título</a>');
        $newItem.attr('data-tab', dataTabString);
        $seccionesMenu.append($newItem);

        var wrapperPlatoElement = $newSeccion.find('.wrapper-seccion-platos')[0];
        Sortable.create(wrapperPlatoElement, platoSortOptions);

        $newSeccion.find('.ui.dropdown.selection').dropdown({useLabels: false});
        $('.tabular.menu .item').tab('change tab', dataTabString);

        $seccionesMenu.scrollLeft($seccionesMenu.width());
    });

    /* Actualizar título del tab tras modificar el nombre de una sección */
    $form.on('input', 'div.seccion .wrapper-seccion input[name$=titulo]', function () {
        var $input = $(this);
        var seccionTitulo = $input.val().trim() || "sin título";

        var dataTabString = $input.closest('div.seccion').attr('data-tab');
        var $tab = $(`#secciones-switcher .item[data-tab=${dataTabString}]`);
        $tab.text(seccionTitulo);
    });

    /* Dar estilo rojo al tab si alguno de sus input está marcado como 'error field' */
    $secciones.find('.error.field').each(function () {
        var $errorInput = $(this);
        var dataTabString = $errorInput.closest('div.seccion').attr('data-tab');

        var $tab = $(`#secciones-switcher .item[data-tab=${dataTabString}]`);
        $tab.addClass('error');
    });

    /* Eliminar el tab cuando se elimina una sección */
    $form.on('click', '.wrapper-seccion .seccion-delete-btn', function () {
        if ($seccionesMenu.find('.item').length <= 1) return;

        var $clickedButton = $(this);
        var $deleteButton = $clickedButton.siblings('.hidden.seccion-delete-btn');

        var dataTabString = $clickedButton.closest('div.seccion').attr('data-tab');
        var $tab = $(`#secciones-switcher .item[data-tab=${dataTabString}]`);
        $tab.remove();

        $seccionesMenu.find('.item').first().click();
        $deleteButton.click();
    });

    /* Eliminar el plato cuando se elimina su form */
    $form.on('click', '.wrapper-seccion-platos .plato-delete-btn', function () {
        var $clickedButton = $(this); 
        var $platoSegment = $clickedButton.parents('.plato');
        if ($platoSegment.siblings('.plato:visible').length == 0) return;

        var $deleteButton = $clickedButton.siblings('.hidden.seccion-delete-btn');
        $deleteButton.click();
    });

    /* Prevenir el envío del form cuando el usuario pulsa la tecla enter */
    $form.on('keydown', function(e) {
        return e.key != "Enter";
    });

    /* Asignar valor de orden a todas las entidades tras hacer click en alguno de los botones de submit */
    $form.on('submit', function (e) {
        /* Prevenir el envío del form para rellenar primero los inputs de orden */
        e.preventDefault();

        /* Ordenar platos recorriendo el formset de platos ('div.plato') por cada sección */
        var $secciones = $('div.seccion');
        $secciones.each(function () {
            var $platos = $(this).find('div.plato');
            $platos.each(function (index) {
                var $platoOrderInput = $(this).find('input[name$="orden"]');
                $platoOrderInput.val(index);
            });
        });

        /* Ordenar secciones recorriendo el menú de tabs inicial (el formset no se ordena, sino los tabs) */
        var $seccionesTab = $seccionesMenu.find('.item');
        $seccionesTab.each(function (index) {
            var $tab = $(this);
            var dataTabString = $tab.attr('data-tab');

            var $seccion = $secciones.filter(`[data-tab=${dataTabString}]`);
            var $seccionOrderInput = $seccion.find('.wrapper-seccion input[name$="orden"]');
            $seccionOrderInput.val(index + 1);
        });

        /* Hacer trim sobre todos los input para no enviar espacios de más */
        $('input').val(function(_, value) {
            return $.trim(value);
         });

        /* Enviar el form una vez cubiertos los inputs de orden 
        * El form necesita un parámetro extra para determinar si pulsamos save-and-exit
        * o save-and-continue, ya que al prevenir el envío del form se pierde esa información */
        $(this).find('#submit-redirect').attr('name', e.originalEvent.submitter.name);
        this.submit();
    });

    /* Escribir sobre cualquier campo marcado como error le quitará la sombra roja */
    $('.field.error').find('input, select').on('input change', function () {
        var $input = $(this)
        $input.parents('.error').removeClass('error');

        $seccion = $input.closest('div.seccion');
        if ($seccion.find('.error').length == 0) {
            var dataTabString = $seccion.attr('data-tab');
            var $tab = $(`#secciones-switcher .item[data-tab=${dataTabString}]`);
            $tab.removeClass('error');
        }        
    });
})(jQuery);