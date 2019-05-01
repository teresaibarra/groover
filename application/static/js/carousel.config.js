$(document).ready(function(){
    $('.owl-carousel').owlCarousel({
      items: 4,
      loop: true,
      nav: true,
      navText: ['←','→'],
      slideBy: 4,
      dots: false,
      margin: 20,
      responsiveClass:true,
      responsive:{
          0:{
              items:1,
              dots:true,
              nav:false
          },
          500:{
              items:2,
              dots:true,
              nav:false
          },
          900:{
              items:3
          },
          1100:{
              items:4
          }
      }
    });
});
