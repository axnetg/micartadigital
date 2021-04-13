(function($) {
    var $topMenu = $(".ui.fixed.menu");
    $(".masthead").visibility({
        once: false,
        onBottomPassed: function () {
            $topMenu.transition("fade in");
        },
        onBottomPassedReverse: function () {
            $topMenu.transition("fade out");
        }
    });

    $('#seg-1, #seg-2, #seg-3, #seg-4').visibility({
        once: false,
        onTopPassed: function() {
            $topMenu.find(`a[data-target='#${$(this).attr('id')}']`).toggleClass('active');
        },
        onBottomPassed: function() {
            $topMenu.find(`a[data-target='#${$(this).attr('id')}']`).toggleClass('active');
        },
        onTopPassedReverse: function() {
            $topMenu.find(`a[data-target='#${$(this).attr('id')}']`).toggleClass('active');
        },
        onBottomPassedReverse: function() {
            $topMenu.find(`a[data-target='#${$(this).attr('id')}']`).toggleClass('active');
        }
    });

    $('a').on('click', function() {
        var idTarget = $(this).data('target');
        if (idTarget !== undefined) {
            window.scrollTo(0, Math.ceil($(idTarget).offset().top));
        }
    });

})(jQuery);

// create sidebar and attach to menu open
//$(".ui.sidebar").sidebar("attach events", ".toc.item");