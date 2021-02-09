$(document).ready(function () {
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