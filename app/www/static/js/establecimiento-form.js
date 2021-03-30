function initImagenField() {
    // ----------------- imagen field -----------------
    $imageSegmentField = $('#header-pic');
    $imageChangeButton = $imageSegmentField.find('#imagen-change-btn');
    $imageClearButton = $imageSegmentField.find('#imagen-clear-btn');
    $imageField = $('input[name=imagen]');
    $imageClearField = $('input[name=imagen-clear]');
    $image = $imageSegmentField.find('img');

    originalImgSrc = $image.attr('src');

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
                $image.attr('src', originalImgSrc);
                alert('Envíe una imagen válida. El fichero que ha enviado no era una imagen o se trataba de una imagen corrupta.');
            }
            image.src = URL.createObjectURL(file);
        }
        else {
            $imageField.val('');
            $image.attr('src', originalImgSrc);
        }
    });

    // ocultar de la vista el campo del input real de la imagen
    $imageField.parents('.field').attr('hidden', 'hidden');   //.hide();
}

function initDireccionField() {
    // ----------------- dirección field -----------------
    $codigoPostalField = $('input[name=codigo_postal]');
    $provinciaField = $('input[name=provincia]');
    $localidadField = $('select[name=localidad]');
    
    $localidadDiv = $localidadField.parents('.ui.dropdown');
    $localidadDiv.dropdown({fullTextSearch: true});

    $codigoPostalField.on('input', function() {
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
}

function initEstablecimientoForm() {
    initImagenField();
    initDireccionField();
}


initEstablecimientoForm();