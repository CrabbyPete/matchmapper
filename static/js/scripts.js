$(document).ready(function() { 

	"use strict";

	// Close mobile menu once link is clicked
	$('.menu li a').click(function(){
		if($('nav').hasClass('nav-open')){
			$('nav').removeClass('nav-open');
		}
	});

    $(window).scroll(function() {
        if ($(window).scrollTop() > 0) {
            $('nav').addClass('fixed');
        } else {
            $('nav').removeClass('fixed');
        }
    });

    // Mobile nav
    $('.mobile-toggle').click(function() {
        $(this).closest('nav').toggleClass('nav-open');
        if ($(this).closest('nav').hasClass('nav-3')) {
            $(this).toggleClass('active');
        }
    });

    $('form.form-search').submit(function(e){
        if (e.preventDefault)
            e.preventDefault();
        else
            e.returnValue = false;

        var error = validateFields(this);
        if (error === 1)
        {
			$(this).closest('form').find('.form-error').fadeIn(200);
		}
		else
		{
	        jQuery.ajax({ type: "POST",
	                      url: "/search",
	                      data: $('form').serialize(),
	                      success: function(e){
                            if('lat' in e && 'lng' in e)
                                window.location = "?lat="+e['lat']+"&lng="+e['lng'];
	                      }

	                   });
		}
    });

    // Contact form code
    $('form.form-email').submit(function(e) {
       
        // return false so form submits through jQuery rather than reloading page.
        if (e.preventDefault)
            e.preventDefault();
        else
            e.returnValue = false;

		jQuery.ajax({
			type: "POST",
			url: "/user/signup",
			data: $('form').serialize(),
			success: function(response)
			{
			}
		});
    });
}); 

$(window).load(function() { 

	"use strict";
	
	// Sticky nav

    if (!$('nav').hasClass('overlay')) {
    	$('.nav-container').css('min-height', $('.navbar').height());
    }

}); 


// Custom JS
function validateFields(form) {
    var error;
    $(form).find('.validate-required').each(function() {
        if ($(this).val() === '')
        {
            $(this).addClass('field-error');
                error = 1;
        } else
        {
                $(this).removeClass('field-error');
                error = 0;
        }
    });
    return error;
};

$(function () {
    $('.list-group.checked-list-box .list-group-item').each(function () {
        
        // Settings
        var $widget = $(this),
            $checkbox = $('<input type="checkbox" class="hidden" />'),
            color = ($widget.data('color') ? $widget.data('color') : "primary"),
            style = ($widget.data('style') == "button" ? "btn-" : "list-group-item-"),
            settings = {
                on: {
                    icon: 'glyphicon glyphicon-check'
                },
                off: {
                    icon: 'glyphicon glyphicon-unchecked'
                }
            };
            
        $widget.css('cursor', 'pointer')
        $widget.append($checkbox);

        // Event Handlers
        $widget.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });
          

        // Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $widget.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $widget.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$widget.data('state')].icon);

            // Update the button's color
            if (isChecked) {
                $widget.addClass(style + color + ' active');
            } else {
                $widget.removeClass(style + color + ' active');
            }
        }

        // Initialization
        function init() {
            
            if ($widget.data('checked') == true) {
                $checkbox.prop('checked', !$checkbox.is(':checked'));
            }
            
            updateDisplay();

            // Inject the icon if applicable
            if ($widget.find('.state-icon').length == 0) {
                $widget.prepend('<span class="state-icon ' + settings[$widget.data('state')].icon + '"></span>');
            }
        }
        init();
    });
    
    $('#get-checked-data').on('click', function(event) {
        event.preventDefault(); 
        var checkedItems = {}, counter = 0;
        $("#check-list-box li.active").each(function(idx, li) {
            checkedItems[counter] = $(li).text();
            counter++;
        });
        $('#display-json').html(JSON.stringify(checkedItems, null, '\t'));
    });
});