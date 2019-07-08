$(document).ready(function() { 

	"use strict";

    // Disable default click on a with blank href

    $('a').click(function() {
        if ($(this).attr('href') === '#') {
            return false;
        }
    });
    
    // Smooth scroll to inner links
    if($('.inner-link').length){
    	$('.inner-link').smoothScroll({
    		offset: -59,
    		speed: 800
    	});
    }
	
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


    if($('.slider').length){
        $('.slider').flexslider({
            directionNav: false
        });
    }

    $('form.form-search').submit(function(e)
    {
        error = validateFields(this);
        if (error === 1)
        {
			$(this).closest('form').find('.form-error').fadeIn(200);
		}
		else
		{
	        jQuery.ajax({ type: "POST", url: "/event/search", data: this.serialize() });
		}
    });

    // Contact form code
    $('form.form-email').submit(function(e) {
       
        // return false so form submits through jQuery rather than reloading page.
        if (e.preventDefault)
            e.preventDefault();
        else
            e.returnValue = false;

        var thisForm = $(this).closest('form.form-email'),
            error = 0,
            originalError = thisForm.attr('original-error'),
            loadingSpinner, iFrame, userEmail, userFullName, userFirstName, userLastName, successRedirect;

		iFrame = $(thisForm).find('iframe.mail-list-form');
		
        thisForm.find('.form-error, .form-success').remove();
        thisForm.append('<div class="form-error" style="display: none;">' + thisForm.attr('data-error') + '</div>');
        thisForm.append('<div class="form-success" style="display: none;">' + thisForm.attr('data-success') + '</div>');


		if( (iFrame.length) && (typeof iFrame.attr('srcdoc') !== "undefined") && (iFrame.attr('srcdoc') !== "") )
		{
			console.log('Mail list form signup detected.');
            userEmail = $(thisForm).find('.signup-email-field').val();
            userFullName = $(thisForm).find('.signup-name-field').val();
            if ($(thisForm).find('input.signup-first-name-field').length) {
                userFirstName = $(thisForm).find('input.signup-first-name-field').val();
            } else {
                userFirstName = $(thisForm).find('.signup-name-field').val();
            }
            userLastName = $(thisForm).find('.signup-last-name-field').val();

			// validateFields returns 1 on error;
			if (validateFields(thisForm) !== 1) {
				console.log('Mail list signup form validation passed.');
				console.log(userEmail);
				console.log(userLastName);
				console.log(userFirstName);
				console.log(userFullName);
				
				iFrame.contents().find('#mce-EMAIL, #fieldEmail').val(userEmail);
				iFrame.contents().find('#mce-LNAME, #fieldLastName').val(userLastName);
				iFrame.contents().find('#mce-FNAME, #fieldFirstName').val(userFirstName);
				iFrame.contents().find('#mce-NAME, #fieldName').val(userFullName);
				iFrame.contents().find('form').attr('target', '_blank').submit();
                successRedirect = thisForm.attr('success-redirect');
                // For some browsers, if empty `successRedirect` is undefined; for others,
                // `successRedirect` is false.  Check for both.
                if (typeof successRedirect !== typeof undefined && successRedirect !== false && successRedirect !== "") {
                    window.location = successRedirect;
                }
			}else {
                thisForm.find('.form-error').fadeIn(1000);
                setTimeout(function() {
                    thisForm.find('.form-error').fadeOut(500);
                }, 5000);
            }
		} else {
			console.log('Send email form detected.');
			if (typeof originalError !== typeof undefined && originalError !== false) {
				thisForm.find('.form-error').text(originalError);
			}

			error = validateFields(thisForm);

			if (error === 1) {
				$(this).closest('form').find('.form-error').fadeIn(200);
				setTimeout(function() {
					$(thisForm).find('.form-error').fadeOut(500);
				}, 3000);
			} else {
				// Hide the error if one was shown
				$(this).closest('form').find('.form-error').fadeOut(200);
				// Create a new loading spinner while hiding the submit button.
				loadingSpinner = jQuery('<div />').addClass('form-loading').insertAfter($(thisForm).find('input[type="submit"]'));
				$(thisForm).find('input[type="submit"]').hide();

				jQuery.ajax({
					type: "POST",
					url: "/event/search",
					data: thisForm.serialize(),
					success: function(response)
					{
						$(thisForm).find('.form-loading').remove();

                        successRedirect = thisForm.attr('success-redirect');
                        // For some browsers, if empty `successRedirect` is undefined; for others,
                        // `successRedirect` is false.  Check for both.
                        if (typeof successRedirect !== typeof undefined && successRedirect !== false && successRedirect !== "")
                        {
                            window.location = successRedirect;
                        }

						$(thisForm).find('input[type="submit"]').show();
						if ($.isNumeric(response)) {
							if (parseInt(response) > 0) {
								thisForm.find('input[type="text"]').val("");
                                thisForm.find('textarea').val("");
                                thisForm.find('.form-success').fadeIn(1000);
								
                                thisForm.find('.form-error').fadeOut(1000);
								setTimeout(function() {
									thisForm.find('.form-success').fadeOut(500);
								}, 5000);
							}
						}
						// If error text was returned, put the text in the .form-error div and show it.
						else {
							// Keep the current error text in a data attribute on the form
							thisForm.find('.form-error').attr('original-error', thisForm.find('.form-error').text());
							// Show the error with the returned error text.
							thisForm.find('.form-error').text(response).fadeIn(1000);
							thisForm.find('.form-success').fadeOut(1000);
						}
					},
					error: function(errorObject, errorText, errorHTTP) {
						// Keep the current error text in a data attribute on the form
						thisForm.find('.form-error').attr('original-error', thisForm.find('.form-error').text());
						// Show the error with the returned error text.
						thisForm.find('.form-error').text(errorHTTP).fadeIn(1000);
						thisForm.find('.form-success').fadeOut(1000);
						$(thisForm).find('.form-loading').remove();
						$(thisForm).find('input[type="submit"]').show();
					}
				});
			}
		}
		return false;
    });

    // End Contact Form Code

    // Get referrer from URL string 
    if (getURLParameter("ref")) {
        $('form.form-email').append('<input type="text" name="referrer" class="hidden" value="' + getURLParameter("ref") + '"/>');
    }

    function getURLParameter(name) {
        return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [, ""])[1].replace(/\+/g, '%20')) || null;
    }


    $('.validate-required, .validate-email').on('blur change', function() {
        validateFields($(this).closest('form'));
    });

    $('form').each(function() {
        if ($(this).find('.form-error').length) {
            $(this).attr('original-error', $(this).find('.form-error').text());
        }
    });

    function validateFields(form) {
        var name, error, originalErrorMessage;

        $(form).find('.validate-required[type="checkbox"]').each(function()
        {
            if (!$('[name="' + $(this).attr('name') + '"]:checked').length) {
                error = 1;
                name = $(this).attr('name').replace('[]', '');
                form.find('.form-error').text('Please tick at least one ' + name + ' box.');
            }
        });

        $(form).find('.validate-required').each(function() {
            if ($(this).val() === '') {
                $(this).addClass('field-error');
                error = 1;
            } else {
                $(this).removeClass('field-error');
            }
        });

        $(form).find('.validate-email').each(function() {
            if (!(/(.+)@(.+){2,}\.(.+){2,}/.test($(this).val()))) {
                $(this).addClass('field-error');
                error = 1;
            } else {
                $(this).removeClass('field-error');
            }
        });

       $(form).find('.validate-search').each(function() {
            if (!(/(.+)@(.+){2,}\.(.+){2,}/.test($(this).val()))) {
                $(this).addClass('field-error');
                error = 1;
            } else {
                $(this).removeClass('field-error');
            }
        });


        if (!form.find('.field-error').length) {
            form.find('.form-error').fadeOut(1000);
        }

        return error;
    }

}); 

$(window).load(function() { 

	"use strict";
	
	// Sticky nav

    if (!$('nav').hasClass('overlay')) {
    	$('.nav-container').css('min-height', $('.navbar').height());
    }

}); 

function scrollHoverGallery(gallery){
	var nextActiveSlide = $(gallery).find('li.active').next();

	if (nextActiveSlide.length === 0) {
		nextActiveSlide = $(gallery).find('li:first-child');
	}

	$(gallery).find('li.active').removeClass('active');
	nextActiveSlide.addClass('active');
}


// Custom JS
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