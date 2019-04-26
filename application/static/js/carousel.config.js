$(document).ready(function(){
    $('.owl-carousel').owlCarousel({
      items: 4,
      loop: true,
      nav: true,
      navText: ['<<','>>'],
      slideBy: 4,
      dots: false,
      margin: 20,
      responsiveClass:true,
      responsive:{
          300:{
              items:2,
              dots:true,
              nav:false
          },
          700:{
              items:3,
              dots:true,
              nav:false
          },
          1000:{
              items:4
          }
      }
    });
});
