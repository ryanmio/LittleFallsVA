/* global window, document, console, fetch, URLSearchParams, $, jQuery */

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

document.getElementById("petition-form").addEventListener("submit", function (event) {
  event.preventDefault();

  var firstName = document.getElementById("first-name").value;
  var email = document.getElementById("email").value;
  var zipCode = document.getElementById("zip-code").value;

  var data = {
    api_key: "V3llrOygSJMujjCNQ8k9Q1px",
    key: "ywPjjLTOwbzGf2kojonJBTBROiYlFSNKWxeAh48GTfE",
    json: JSON.stringify({
      sequential: 1,
      contact_type: "Individual",
      first_name: firstName,
      email: email,
      location_type_id: 1,
      postal_code: zipCode,
    }),
  };

  fetch("http://crm.littlefallsva.com/civicrm/extern/rest.php?entity=Contact&action=create", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams(data),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.is_error) {
        // eslint-disable-next-line no-console  
        console.error("Error creating contact:", data.error_message);
      } else {
        // eslint-disable-next-line no-console
          console.log("Contact created successfully:", data);
        // Add your code to update the counter here
      }
    })
    .catch(function (error) {
      // eslint-disable-next-line no-console
      console.error("Error submitting form:", error);
    });
});
