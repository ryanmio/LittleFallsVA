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

document.addEventListener('DOMContentLoaded', function () {
  // Petition form
  var petitionFormElement = document.getElementById('petition-form');
  if (petitionFormElement) {
    petitionFormElement.addEventListener('submit', submitForm);
  }

  // Subscription form
  var subscriptionFormElement = document.getElementById("subscription-form");
  var subscriptionMessageElement = document.getElementById("subscription-message");

  if (subscriptionFormElement && subscriptionMessageElement) {
    subscriptionFormElement.addEventListener("submit", function (event) {
      event.preventDefault();

      var formData = new FormData(event.target);

      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(formData).toString(),
      })
        .then(function (response) {
          if (response.ok) {
            subscriptionMessageElement.innerText = "Subscription successful!";
          } else {
            throw new Error("Form submission failed");
          }
        })
        .catch(function (error) {
          subscriptionMessageElement.innerText = "Subscription failed. Please try again.";
        });
    });
  }

  // Signatures counter
  var sheetUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSJ8pwb9De5aggU61jQwEP5SQs9VfnA7_YQPskQn0TzI6cIG7O_vHP9q2wL1F22wa9sleGhJor106EH/pub?gid=0&single=true&output=csv';
  var signaturesCountTopElement = document.getElementById('signaturesCount');
  var signaturesCountBottomElement = document.getElementById('signaturesCountBottom');

  function updateSignaturesCount() {
    fetch(sheetUrl)
      .then(function (response) {
        return response.text();
      })
      .then(function (csvData) {
        var signatures = csvData.trim().split('\n');
        var count = signatures.length - 1; // Subtract 1 to exclude the header row
        if (signaturesCountTopElement) {
          signaturesCountTopElement.innerText = count;
        }
        if (signaturesCountBottomElement) {
          signaturesCountBottomElement.innerText = count;
        }
      })
      .catch(function (error) {
        console.error('Error fetching signature count:', error);
      });
  }

  if (signaturesCountTopElement || signaturesCountBottomElement) {
    updateSignaturesCount();
    setInterval(updateSignaturesCount, 60000); // Update every 1 minute
  }
}); 

function submitForm(event) {
    event.preventDefault();
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;

    var sheetId = '1AgA0OYRkBZRK-MkkQWvnqjRbEyIO9nhflJ14htPgD4k';
    var sheetName = 'Sheet1';
    var apiKey = 'AIzaSyD1G33z5ybsx9XoKbqWqx2QvtHgY9s0pc0';

    var newRowData = {
        "range": sheetName,
        "majorDimension": "ROWS",
        "values": [
            [name, email]
        ]
    };

     fetch('https://sheets.googleapis.com/v4/spreadsheets/' + sheetId + '/values/' + sheetName + ':append?valueInputOption=RAW&insertDataOption=INSERT_ROWS&key=' + apiKey, {
        method: 'POST',
        body: JSON.stringify(newRowData),
        headers: new Headers({
            'Content-Type': 'application/json'
        })
    }).then(function(response) {
        if (response.ok) {
            alert('Petition signed!');
            document.getElementById('petition-form').reset();
        } else {
            alert('Error signing the petition. Please try again later.');
        }
    });
}