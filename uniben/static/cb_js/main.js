/*-------------------------------
[  Table of contents  ]
---------------------------------
  01. jQuery MeanMenu
  02. wow js active
  03. Portfolio  Masonry (width)
  04. Sticky Header
  05. ScrollUp
  06. Tooltip
  07. ScrollReveal Js Init
  08. Fixed Footer bottom script ( Newsletter )
  09. Search Bar
  10. Toogle Menu
  11. Shopping Cart Area
  12. Filter Area
  13. User Menu
  14. Overlay Close
  15. Home Slider
  16. Popular Product Wrap
  17. Testimonial Wrap
  18. Magnific Popup
  19. Price Slider Active
  20. Plus Minus Button
  21. jQuery scroll Nav

/*--------------------------------
[ End table content ]
-----------------------------------*/

(function ($) {
	'use strict';

	/*-------------------------------------------
	  01. jQuery MeanMenu
	--------------------------------------------- */

	$('.mobile-menu nav').meanmenu({
		meanMenuContainer: '.mobile-menu-area',
		meanScreenWidth: "991",
		meanRevealPosition: "right",
	});

	/*-------------------------------------------
	  02. wow js active
	--------------------------------------------- */

	new WOW().init();

	/*-------------------------------------------
	  03. Product  Masonry (width)
	--------------------------------------------- */

	$('.htc__product__container').imagesLoaded(function () {

		// filter items on button click
		$('.product__menu').on('click', 'button', function () {
			var filterValue = $(this).attr('data-filter');
			$grid.isotope({
				filter: filterValue
			});
		});
		// init Isotope
		var $grid = $('.product__list').isotope({
			itemSelector: '.single__pro',
			percentPosition: true,
			transitionDuration: '0.7s',
			layoutMode: 'fitRows',
			masonry: {
				// use outer width of grid-sizer for columnWidth
				columnWidth: 1,
			}
		});

	});

	$('.product__menu button').on('click', function (event) {
		$(this).siblings('.is-checked').removeClass('is-checked');
		$(this).addClass('is-checked');
		event.preventDefault();
	});

	/*-------------------------------------------
	  04. Sticky Header
	--------------------------------------------- */

	var win = $(window);
	var sticky_id = $("#sticky-header-with-topbar");
	win.on('scroll', function () {
		var scroll = win.scrollTop();
		if (scroll < 245) {
			sticky_id.removeClass("scroll-header");
		} else {
			sticky_id.addClass("scroll-header");
		}
	});

	/*--------------------------
	  05. ScrollUp
	---------------------------- */
	$.scrollUp({
		scrollText: '<i class="zmdi zmdi-chevron-up"></i>',
		easingType: 'linear',
		scrollSpeed: 900,
		animation: 'fade'
	});

	/*---------------------------
	  06. Tooltip
	------------------------------*/
	$('[data-toggle="tooltip"]').tooltip({
		animated: 'fade',
		placement: 'top',
		container: 'body'
	});

	/*-----------------------------------
	  07. ScrollReveal Js Init
	-------------------------------------- */

	window.sr = ScrollReveal({
		duration: 800,
		reset: true
	});
	sr.reveal('.foo');
	sr.reveal('.bar');

	/*-------------------------------------------------------
	  08. Fixed Footer bottom script ( Newsletter )
	--------------------------------------------------------*/

	var $newsletter_height = $(".htc__foooter__area");
	$('.fixed__footer').css({
		'margin-bottom': $newsletter_height.height() + 'px'
	});

	/*------------------------------------
	  10. Toogle Menu
	--------------------------------------*/

	$('.toggle__menu').on('click', function () {
		$('.offsetmenu').addClass('offsetmenu__on');
		$('.body__overlay').addClass('is-visible');

	});

	$('.offsetmenu__close__btn').on('click', function () {
		$('.offsetmenu').removeClass('offsetmenu__on');
		$('.body__overlay').removeClass('is-visible');
	});

	/*------------------------------------
	  12. Filter Area
	--------------------------------------*/

	$('.filter__menu').on('click', function () {
		$('.filter__wrap').addClass('filter__menu__on');
		$('.body__overlay').addClass('is-visible');

	});

	$('.filter__menu__close__btn').on('click', function () {
		$('.filter__wrap').removeClass('filter__menu__on');
		$('.body__overlay').removeClass('is-visible');
	});

	/*------------------------------------
	  13. User Menu
	--------------------------------------*/

	$('.user__menu').on('click', function () {
		$('.user__meta').addClass('user__meta__on');
		$('.body__overlay').addClass('is-visible');

	});

	$('.offsetmenu__close__btn').on('click', function () {
		$('.user__meta').removeClass('user__meta__on');
		$('.body__overlay').removeClass('is-visible');
	});

	/*------------------------------------
	  14. Overlay Close
	--------------------------------------*/
	$('.body__overlay').on('click', function () {
		$(this).removeClass('is-visible');
		$('.offsetmenu').removeClass('offsetmenu__on');
		$('.shopping__cart').removeClass('shopping__cart__on');
		$('.filter__wrap').removeClass('filter__menu__on');
		$('.user__meta').removeClass('user__meta__on');
	});

	/*-----------------------------------------------
	  15. Home Slider
	-------------------------------------------------*/

	if ($('.slider__activation__wrap').length) {
		$('.slider__activation__wrap').owlCarousel({
			loop: true,
			margin: 0,
			nav: true,
			autoplay: false,
			navText: ['<i class="zmdi zmdi-chevron-left"></i>', '<i class="zmdi zmdi-chevron-right"></i>'],
			autoplayTimeout: 10000,
			items: 1,
			dots: false,
			lazyLoad: true,
			responsive: {
				0: {
					items: 1
				},
				1920: {
					items: 1
				}
			}
		});
	}

	if ($('.slider__activation__02').length) {
		$('.slider__activation__02').owlCarousel({
			loop: true,
			margin: 0,
			nav: false,
			autoplay: false,
			autoplayTimeout: 10000,
			items: 1,
			dots: false,
			lazyLoad: true,
			responsive: {
				0: {
					items: 1
				},
				1920: {
					items: 1
				}
			}
		});
	}

	/*-----------------------------------------------
	  16. Popular Product Wrap
	-------------------------------------------------*/

	$('.popular__product__wrap').owlCarousel({
		loop: true,
		margin: 0,
		nav: true,
		autoplay: false,
		navText: ['<i class="zmdi zmdi-chevron-left"></i>', '<i class="zmdi zmdi-chevron-right"></i>'],
		autoplayTimeout: 10000,
		items: 3,
		dots: false,
		lazyLoad: true,
		responsive: {
			0: {
				items: 1
			},
			600: {
				items: 2
			},
			800: {
				items: 2
			},
			1024: {
				items: 3
			},
			1200: {
				items: 3
			},
			1400: {
				items: 3
			},
			1920: {
				items: 3
			}
		}
	});

	/*-----------------------------------------------
	  17. Testimonial Wrap
	-------------------------------------------------*/

	$('.testimonial__wrap').owlCarousel({
		loop: true,
		margin: 0,
		nav: false,
		autoplay: false,
		navText: false,
		autoplayTimeout: 10000,
		items: 1,
		dots: false,
		lazyLoad: true,
		responsive: {
			0: {
				items: 1
			},
			600: {
				items: 1
			},
			800: {
				items: 1
			},
			1024: {
				items: 1
			},
			1200: {
				items: 1
			},
			1400: {
				items: 1
			},
			1920: {
				items: 1
			}
		}
	});

	/*--------------------------------
	  18. Magnific Popup
	----------------------------------*/

	$('.video-popup').magnificPopup({
		type: 'iframe',
		mainClass: 'mfp-fade',
		removalDelay: 160,
		preloader: false,
		zoom: {
			enabled: true,
		}
	});

	$('.image-popup').magnificPopup({
		type: 'image',
		mainClass: 'mfp-fade',
		removalDelay: 100,
		gallery: {
			enabled: true,
		}
	});

	/*-------------------------------
	  19. Price Slider Active
	--------------------------------*/
	$("#slider-range").slider({
		range: true,
		min: 10,
		max: 500,
		values: [110, 400],
		slide: function (event, ui) {
			$("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
		}
	});
	$("#amount").val("$" + $("#slider-range").slider("values", 0) +
		" - $" + $("#slider-range").slider("values", 1));

	/*-------------------------------
	  20.  Plus Minus Button
	--------------------------------*/

	$(".cart-plus-minus").append('<div class="dec qtybutton">-</i></div><div class="inc qtybutton">+</div>');

	$(".qtybutton").on("click", function () {
		var $button = $(this);
		var oldValue = $button.parent().find("input").val();
		if ($button.text() == "+") {
			var newVal = parseFloat(oldValue) + 1;
		} else {
			// Don't allow decrementing below zero
			if (oldValue > 1) {
				var newVal = parseFloat(oldValue) - 1;
			} else {
				newVal = 1;
			}
		}
		$button.parent().find("input").val(newVal);
	});

	/*--------------------------
	  21. jQuery scroll Nav
	---------------------------- */
	$('.onepage--menu').onePageNav({
		scrollOffset: 0
	});

})(jQuery);

// Placeholder and Label Animation
$('input, textarea').focus(function () {
	$(this).parents('.form--group').addClass('focused');
});

$('input, textarea').blur(function () {
	var inputValue = $(this).val();
	if (inputValue == "") {
		$(this).removeClass('filled');
		$(this).parents('.form--group').removeClass('focused');
	} else {
		$(this).addClass('filled');
	}
})

//Show Hidden Password
$(".toggle--password").click(function () {

	$(this).toggleClass("zmdi-eye zmdi-eye-off");
	var input = $($(this).attr("toggle"));
	if (input.attr("type") == "password") {
		input.attr("type", "text");
	} else {
		input.attr("type", "password");
	}
});

//Show update status for merchant page
$(".commit--changes__personal").click(function () {

	$("#change--effected__account").toggleClass("hide view");
});
$(".commit--changes__business").click(function () {

	$("#change--effected__business").toggleClass("hide view");
});
$(".commit--changes__login").click(function () {

	$("#change--effected__login").toggleClass("hide view");
});
$(".commit--changes__delete").click(function () {

	$("#change--effected__delete").toggleClass("hide view");
});

//Toast Notification on Load
$(document).ready(function () {
	$("#openToast").toggleClass("hide view");

	$('a.exit--toast').click(function () {
		$("#openToast").fadeOut(1000, 0);
	});

	$(document).on('click', function (e) {
		if ($(e.target).closest(".notification--reminder").length === 0) {
			$("#openToast").fadeOut(1000, 0);
		}
	});
});

//Update Product
$(function () {
	$('.show').click(function () {
		$('.toast').addClass('on');
		setTimeout(function () {
			$('.toast').removeClass('on')
		}, 1500);
	});
});

//Logout
$(function () {
	$('.show--logout').click(function () {
		$('.login-out').addClass('on');
		setTimeout(function () {
			window.location.replace.assign("./index.html");
		}, 2000)
	});
});

//Delete Product
$(function () {
	$('.delete__pro').click(function () {
		$('.delete--product').addClass('on');
		setTimeout(function () {
			window.location.replace.assign("./merchant.html");
		}, 2000)
	});
});

//FAQ Accordion
;(function($) {
	var flatAccordion = function() {
		var speed= {duration: 600};
		$('.toggle-content').hide();
		$('.flat-accordion .toggle-title.active').siblings('.toggle-content').show();

		$('.flat-accordion .toggle-title').on('click', function(){
		if(!$(this).is('.active')) {
			$(this).closest('.flat-accordion').find('.toggle-title.active').toggleClass('active').next().slideToggle(speed);
			$(this).toggleClass('active');
			$(this).next().slideToggle(speed);
		}else {
			$(this).toggleClass('active');
			$(this).next().slideToggle(speed);
		}
		});
	};
	$(function() {
		flatAccordion();
	 });
})(jQuery);