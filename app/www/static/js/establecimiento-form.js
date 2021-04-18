(function($) {
    /* Establecer texto de no resultados del dropdown de localidad y carta */
    $.fn.dropdown.settings.message.noResults = 'No se han encontrado resultados.';

    // ----------------- imagen field -----------------
    var $imageSegmentField = $('#header-pic');
    var $imageChangeButton = $imageSegmentField.find('#imagen-change-btn');
    var $imageClearButton = $imageSegmentField.find('#imagen-clear-btn');
    var $imageField = $('input[name=imagen]');
    var $imageClearField = $('input[name=imagen-clear]');
    var $image = $imageSegmentField.find('img');

    var originalImgSrc = $image.attr('src');

    // efecto dimmer cuando se pasa el ratón por encima del segmento imagen
    $imageSegmentField.dimmer({ on: 'hover', opacity: 0.5 });

    // hacer click en el botón de cambiar imagen equivale a abrir el diálogo para cargar una imagen
    $imageChangeButton.on('click', () => $imageField.click());

    // hacer click en el botón de eliminar imagen establece el checkbox a true y coloca la imagen por defecto
    $imageClearButton.on('click', () => {
        $imageClearField.prop('checked', true);
        $imageField.val('');
        $image.attr('src', 'https://i.stack.imgur.com/y9DpT.jpg');
    });

    // cuando el input de imagen cambia de valor se comprueba si es una imagen real y se coloca en el segmento imagen
    $imageField.on('change', (event) => {
        let file = event.target.files[0];
        if (typeof file !== "undefined") {
            let image = new Image();
            image.onload = () => {
                $imageClearField.prop('checked', false);
                $image.attr('src', URL.createObjectURL(file));
            };
            image.onerror = () => {
                $imageField.val('');
                $imageClearField.prop('checked', false);
                $image.attr('src', originalImgSrc);
                alert('Envíe una imagen válida. El fichero que ha enviado no era una imagen o se trataba de una imagen corrupta.');
            }
            image.src = URL.createObjectURL(file);
        }
        else {
            $imageField.val('');
            $imageClearField.prop('checked', false);
            $image.attr('src', originalImgSrc);
        }
    });

    // ocultar de la vista el campo del input real de la imagen
    $imageField.parents('.field').attr('hidden', 'hidden');   //.hide();



    // ----------------- dirección field -----------------
    var $codigoPostalField = $('input[name=codigo_postal]');
    var $provinciaField = $('input[name=provincia]');
    var $localidadField = $('select[name=localidad]');
    
    var $localidadDiv = $localidadField.parents('.ui.dropdown');
    $localidadDiv.dropdown({ fullTextSearch: true });

    // escribir el código postal desencadena la búsqueda de localidades posibles y autocompleta el nombre de provincia
    $codigoPostalField.on('input', function () {
        $provinciaField.val('');
        $localidadField.empty();
        $localidadField.siblings('.text').empty();

        if (this.value.match('^(0[1-9]|[1-4][0-9]|5[0-2])[0-9]{3}$')) {
            $localidadDiv.toggleClass('loading');

            $.getJSON('http://www.geonames.org/postalCodeLookupJSON?&country=ES&maxRows=100&callback=?',
                { postalcode: this.value }, (response) => {
                    if (response && response.postalcodes.length) {
                        $provinciaField.val(response.postalcodes[0].adminName2);

                        response.postalcodes.forEach(place => {
                            let localidad = place.placeName;
                            let $option = $("<option>").text(localidad).val(localidad);
                            $localidadField.append($option);
                        });
                    }
                    $localidadDiv.toggleClass('loading');
                }
            );
        }
    });



    // ----------------- slug field -----------------
    var $nombreField = $('input[name=nombre]');
    var $slugField = $('input[name=slug]');
    var slugLocked = $slugField.val().trim() ? true : false;

    var slugify = (text) => {
        return text.toLowerCase()
                    .normalize('NFD')
                    .replace(/[\u0300-\u036f]/g, '')
                    .replace(/&/g, '-and-')
                    .replace(/ /g,'-')
                    .replace(/[-]+/g, '-')
                    .replace(/[^\w-]+/g,'');
    };

    // escribir en el campo nombre autocompletará el slug siempre que no esté en estado locked
    $nombreField.on('input', function () {
        if (slugLocked) return;

        var text = $(this).val().trim();
        text = slugify(text);
        $slugField.val(text);
    });

    // escribir en el campo slug lo marcará como locked, excepto si se ha borrado por completo
    $slugField.on('input', function () {
        slugLocked = $(this).val().trim() ? true : false;
    });

    // quitarle el focus al campo slug convertirá cualquier texto escrito a formato slug
    $slugField.on('blur', function () {
        var $input = $(this);
        var text = $input.val().trim();
        text = slugify(text);
        $input.val(text);
    });



    // ----------------- carta field -----------------
    var $cartaDiv = $('select[name=carta]').parents('.ui.dropdown');
    $cartaDiv.dropdown({ fullTextSearch: true, clearable: true });

})(jQuery);