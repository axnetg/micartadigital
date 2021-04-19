(function($) {
    var $confirmDeletionCheckbox = $('input[name="user_confirm_delete"]');
    var $confirmDeletionSubmitButton = $('input[name="user_delete"]');
    
    $confirmDeletionCheckbox.on('click', function() {
        $confirmDeletionSubmitButton.toggleClass('disabled');
    });
})(jQuery);