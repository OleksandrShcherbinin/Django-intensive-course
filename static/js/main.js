(function ($) {
    "use strict";

    /*--------------------------
     Background Image JS
    ---------------------------*/
    const bgSelector = $("[data-bg]");
    bgSelector.each(function (index, elem) {
        var element = $(elem),
            bgSource = element.data('bg');
        element.css('background-image', 'url(' + bgSource + ')');
    });

    /*--
        Menu Sticky
    -----------------------------------*/
    var windows = $(window);
    var screenSize = windows.width();
    var sticky = $('.header-sticky');

    windows.on('scroll', function () {
        var scroll = windows.scrollTop();
        if (scroll < 300) {
            sticky.removeClass('is-sticky');
        } else {
            sticky.addClass('is-sticky');
        }
    });

    /*--
        Sidebar Menu
    -----------------------------------*/
    var menuToggle = $('.menu-toggle');
    var sideMenuClose = $('.side-menu-close');
    var sideMenuWrap = $('.side-menu-wrap');
    var sideMenuOverlay = $('.side-menu-overlay');

    menuToggle.on('click', function () {

        sideMenuWrap.addClass('side-menu-open');
        sideMenuOverlay.addClass('side-menu-open');

    });
    sideMenuClose.on('click', function () {

        sideMenuWrap.removeClass('side-menu-open');
        sideMenuOverlay.removeClass('side-menu-open');

    });
    sideMenuOverlay.on('click', function () {

        sideMenuWrap.removeClass('side-menu-open');
        sideMenuOverlay.removeClass('side-menu-open');

    });

    /*--
        Sidebar Submenu
    ------------------------*/
    $('.side-menu .menu-item-has-children > a').prepend('<i class="expand menu-expand fa fa-angle-down"></i>');
    $('.side-menu .menu-item-has-children ul').slideUp();

    /*-- Category Sub Menu --*/
    $('.side-menu').on('click', 'li a, li a .menu-expand', function (e) {
        var $a = $(this).hasClass('menu-expand') ? $(this).parent() : $(this);
        if ($a.parent().hasClass('menu-item-has-children')) {
            if ($a.attr('href') === '#' || $(this).hasClass('menu-expand')) {
                if ($a.siblings('ul:visible').length > 0) {
                    $a.find('.menu-expand').removeClass('fa-angle-up').addClass('fa-angle-down');
                    $a.siblings('ul').slideUp();
                } else {
                    $(this).parents('li').siblings('li').find('.menu-expand').removeClass('fa-angle-up').addClass('fa-angle-down');
                    $(this).parents('li').siblings('li').find('ul:visible').slideUp();
                    $a.find('.menu-expand').removeClass('fa-angle-down').addClass('fa-angle-up');
                    $a.siblings('ul').slideDown();
                }
            }
        }
        if ($(this).hasClass('menu-expand') || $a.attr('href') === '#') {
            e.preventDefault();
            return false;
        }
    });

    /*--
        Mobile Menu
    ------------------------*/
    var mainMenuNav = $('.main-menu nav');
    mainMenuNav.meanmenu({
        meanScreenWidth: '991',
        meanMenuContainer: '.mobile-menu',
        meanMenuClose: '<span class="menu-close"></span>',
        meanMenuOpen: '<span class="menu-bar"></span>',
        meanRevealPosition: 'right',
        meanMenuCloseSize: '0',
    });

    /*--
        Hero Slider
    --------------------------------------------*/
    var heroSlider = $('.slider-wrapper');
    heroSlider.slick({
        arrows: true,
        autoplay: false,
        autoplaySpeed: 5000,
        dots: true,
        pauseOnFocus: false,
        pauseOnHover: false,
        fade: true,
        infinite: true,
        slidesToShow: 1,
        prevArrow: '<button type="button" class="slick-prev"><i class="fa fa-long-arrow-left"></i></button>',
        nextArrow: '<button type="button" class="slick-next"><i class="fa fa-long-arrow-right"></i></button>',
        responsive: [
            {
                breakpoint: 767,
                settings: {
                    adaptiveHeight: true,
                }
            }
        ]
    });

    /*--
        Product Slider
    -----------------------------------*/
    $('.product-slider').slick({
        arrows: true,
        dots: false,
        autoplay: false,
        infinite: true,
        slidesToShow: 4,
        prevArrow: '<button type="button" class="slick-prev"><i class="icofont icofont-long-arrow-left"></i></button>',
        nextArrow: '<button type="button" class="slick-next"><i class="icofont icofont-long-arrow-right"></i></button>',
        responsive: [
            {
                breakpoint: 1199,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 767,
                settings: {
                    autoplay: true,
                    slidesToShow: 1,
                    arrows: false,
                }
            }
        ]
    });

    /*--
        MailChimp
    -----------------------------------*/
    $('#mc-form').ajaxChimp({
        language: 'en',
        callback: mailChimpResponse,
        // ADD YOUR MAILCHIMP URL BELOW HERE!
        url: 'http://devitems.us11.list-manage.com/subscribe/post?u=6bbb9b6f5827bd842d9640c82&amp;id=05d85f18ef'

    });

    function mailChimpResponse(resp) {

        if (resp.result === 'success') {
            $('.mailchimp-success').html('' + resp.msg).fadeIn(900);
            $('.mailchimp-error').fadeOut(400);

        } else if (resp.result === 'error') {
            $('.mailchimp-error').html('' + resp.msg).fadeIn(900);
        }
    }

    /*--
        Scroll Up
    -----------------------------------*/
    $.scrollUp({
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade',
        scrollText: '<i class="fa fa-angle-up"></i>',
    });

    /*--
        Price Range Slider
    ------------------------*/
    $('#price-range').slider({
        range: true,
        min: 0,
        max: 2000,
        values: [25, 970],
        slide: function (event, ui) {
            $('#price-amount').val('$' + ui.values[0] + ' - $' + ui.values[1]);
        }
    });
    $('#price-amount').val('$' + $('#price-range').slider('values', 0) +
        ' - $' + $('#price-range').slider('values', 1));

    /*--
        Product Quantity
    -----------------------------------*/
    $('.product-quantity').append('<span class="dec qtybtn">-</span><span class="inc qtybtn">+</span>');
    $('.qtybtn').on('click', function () {
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        $button.parent().find('input').val(newVal);
    });

    /*-----
        Shipping Form Toggle
    --------------------------------*/
    $('[data-shipping]').on('click', function () {
        if ($('[data-shipping]:checked').length > 0) {
            $('#shipping-form').slideDown();
        } else {
            $('#shipping-form').slideUp();
        }
    });

    /*-----
        Payment Method Select
    --------------------------------*/
    $('[name="payment-method"]').on('click', function () {

        var $value = $(this).attr('value');

        $('.single-method p').slideUp();
        $('[data-method="' + $value + '"]').slideDown();

    });

    /*-----
        Product Zoom
    --------------------------------*/
    $(".product-zoom").elevateZoom({
        zoomType: "inner",
        cursor: "crosshair",
        gallery: 'pro-thumb-img',
        galleryActiveClass: "active",
    });

    /*--
        Nice Select
    ------------------------*/
    $('.nice-select').niceSelect();

    /*--
        Nice Scroll
    ------------------------*/
    $(".nice-scroll").niceScroll({
        cursorcolor: "#373b3e",
        cursorborder: "0px solid #ffffff",
        cursorwidth: "3px",
    });


    $(".btn-src").on('click', function () {
        $(".header-search").addClass("show");
    });

    $(".btn-close").on('click', function () {
        $(".header-search").removeClass("show");
    });

    $(window).on('load', function () {
        $(".banner-masonry").masonry({
            columnWidth: '.resizer'
        });
    });

})(jQuery);	
