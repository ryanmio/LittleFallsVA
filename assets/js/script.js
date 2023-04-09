/* global window, document, console, fetch, URLSearchParams, $, jQuery */
/* eslint no-unused-vars: "off", no-undef: "off" */

// Preloader js    
$(window).on('load', function () {
  $('.preloader').fadeOut(100);
});

(function ($) {
  'use strict';

  
  // product Slider
  $('.product-image-slider').slick({
    autoplay: false,
    infinite: true,
    arrows: false,
    dots: true,
    customPaging: function (slider, i) {
      var image = $(slider.$slides[i]).data('image');
      return '<img class="img-fluid" src="' + image + '" alt="product-image">';
    }
  });

  // Product slider
  $('.product-slider').slick({
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    dots: false,
    arrows: false,
    responsive: [{
        breakpoint: 1024,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1
        }
      }
    ]
  });

})(jQuery);

var sheetUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSJ8pwb9De5aggU61jQwEP5SQs9VfnA7_YQPskQn0TzI6cIG7O_vHP9q2wL1F22wa9sleGhJor106EH/pub?gid=0&single=true&output=csv';
    var signaturesCountElement = document.getElementById('signaturesCount');

    function updateSignaturesCount() {
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          var lines = xhr.responseText.split('\n');
          var signaturesCount = lines.length - 1; // Subtract the header line
          signaturesCountElement.innerText = signaturesCount;
        }
      };
      xhr.open('GET', sheetUrl, true);
      xhr.send();
    }

    updateSignaturesCount();
    setInterval(updateSignaturesCount, 60000); // Update every 1 minute