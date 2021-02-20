$(document).ready(function () {
    // toggle active item over corresponding div
    $('#seg-1, #seg-2, #seg-3, #seg-4').visibility({
        once: false,
        onTopPassed: function() {
            $('.ui.top.fixed a[data-target=\'#' + $(this).attr('id') + '\']').toggleClass('active');
        },
        onBottomPassed: function() {
            $('.ui.top.fixed a[data-target=\'#' + $(this).attr('id') + '\']').toggleClass('active');
        },
        onTopPassedReverse: function() {
            $('.ui.top.fixed a[data-target=\'#' + $(this).attr('id') + '\']').toggleClass('active');
        },
        onBottomPassedReverse: function() {
            $('.ui.top.fixed a[data-target=\'#' + $(this).attr('id') + '\']').toggleClass('active');
        }
    });
    
    // fix menu when passed
    $(".masthead").visibility({
        once: false,
        onBottomPassed: function () {
            $(".ui.fixed.menu").transition("fade in");
        },
        onBottomPassedReverse: function () {
            $(".ui.fixed.menu").transition("fade out");
        }
    });

    // create sidebar and attach to menu open
    //$(".ui.sidebar").sidebar("attach events", ".toc.item");
});

$('a').click(function() {
    let target = $(this).data('target');
    if (target !== undefined) {
        window.scrollTo(0, $(target).offset().top);
    }
});