$(document).ready(function(){
  //HamBurger
  var forEach=function(t,o,r){if("[object Object]"===Object.prototype.toString.call(t))for(var c in t)Object.prototype.hasOwnProperty.call(t,c)&&o.call(r,t[c],c,t);else for(var e=0,l=t.length;l>e;e++)o.call(r,t[e],e,t)};
  var hamburgers = document.querySelectorAll(".hamburger");
  if (hamburgers.length > 0) {
    forEach(hamburgers, function(hamburger) {
      hamburger.addEventListener("click", function() {
        this.classList.toggle("is-active");
      }, false);
    });
  }

  //WOW
  new WOW().init();

  //padding-top
  $('.inner-page').css('padding-top', $('#main-header').height() + 'px');


  var pageURL = window.location.href;
  var lastURLSegment = pageURL.substr(pageURL.lastIndexOf('/') + 1);
  $("body").attr('id', lastURLSegment.split('.')[0]);


  $('.navbar-toggler').click(function(){
    $('#navbarNav').toggleClass('menu-show');
    $(this).toggleClass('collapsed');
    $('body').toggleClass('menu-open');
  });

  var equalWidthHeight = $('.equal-wh').width();
  $('.equal-wh').css({'min-height':equalWidthHeight+'px'});

  $('.owl-carousel-blogs').owlCarousel({
      autoplay: true,
      animateOut: 'fadeOut',
      animateIn: 'fadeIn',
      autoWidth: false,
      loop: false,
      margin: 24,
      nav: false,
      dots: false,
      pag: true,
      responsive: {
        320: {
          items: 1
        },
        600: {
          items: 2
        },
        800: {
          items: 2
        },
        1024: {
          items: 2
        },
        1366: {
          items: 3
        },
        1440: {
          items: 3
        }
      }
    });

});


$(window).scroll(function() {
  //padding-top
  $('.inner-page').css('padding-top', $('#main-header').height() + 'px');

  //Top
  $('.nav-item.dropdown .dropdown-menu').css('top', $('#main-header').height() + 'px');

});

$(window).resize( function() {
  //padding-top
  $('.inner-page').css('padding-top', $('#main-header').height() + 'px');

  //Top
  $('.nav-item.dropdown .dropdown-menu').css('top', $('#main-header').height() + 'px');

  var equalWidthHeight = $('.equal-wh').width();
  $('.equal-wh').css({'min-height':equalWidthHeight+'px'});
});

