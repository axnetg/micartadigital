function toggleTopMenuVisibility() {
    $topMenu = $(".ui.fixed.menu");
    $(".masthead").visibility({
        once: false,
        onBottomPassed: function () {
            $topMenu.transition("fade in");
        },
        onBottomPassedReverse: function () {
            $topMenu.transition("fade out");
        }
    });
}

function toggleActiveMenuItemOnScroll() {
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
}

function scrollToSegmentOnMenuItemClick() {
    $('a').on('click', function() {
        let idTarget = $(this).data('target');
        if (idTarget !== undefined) {
            window.scrollTo(0, Math.ceil($(idTarget).offset().top));
        }
    });
}

function initHomePage() {
    toggleTopMenuVisibility();
    toggleActiveMenuItemOnScroll();
    scrollToSegmentOnMenuItemClick();
}

initHomePage();

// create sidebar and attach to menu open
//$(".ui.sidebar").sidebar("attach events", ".toc.item");
