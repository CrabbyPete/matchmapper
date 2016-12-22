$(function(){
	
	//equalheight jquery start
	equalHeight($(".team-two-block li h4"));
				
	
	//form jquery start	
	$('form input[type=text],form input[type=email], form textarea').each(function(){
		var textVal = $(this).val();
		var idVal = $(this).attr('id');
		
		$('#'+idVal).focus(function(){
			if($(this).val() == textVal)
				$(this).val('');
		});
		
		$('#'+idVal).blur(function(){
			if($(this).val() == '')
				$(this).val(textVal);
		});
		
	});	
		
});

$(window).resize(function() {
			 
	$(".team-two-block li h4").css('height','auto');
			 
	equalHeight($(".team-two-block li h4 "));
		
		
});

function equalHeight(group) {
	 var tallest = 0;
	 group.each(function() 
	 {
	 	var thisHeight = jQuery(this).height();
	 	if(thisHeight > tallest) 
	 	{ 
	 		tallest = thisHeight;
	 	}
	 });
	 group.height(tallest);
}



// JavaScript Document

$(function(){
	
	//equalheight jquery start
	equalHeight($(".team-two-block li h4"));
				
	
	//form jquery start	
	$('form input[type=text],form input[type=email], form textarea').each(function(){
		var textVal = $(this).val();
		var idVal = $(this).attr('id');
		
		$('#'+idVal).focus(function(){
			if($(this).val() == textVal)
				$(this).val('');
		});
		
		$('#'+idVal).blur(function(){
			if($(this).val() == '')
				$(this).val(textVal);
		});
		
	});	
	
	function send_ajax(e){
		$.ajax({ type : "POST",
            cache : false,
            url: "/signin",
            data: $(this).serialize(),
            success:function(data)
            { 	
            	parent.jQuery.fancybox(data);
            }
        });
	 
	   	return false;		
	}
	
	$("#sign-in-form").on( "submit", send_ajax ); 

	
	$("#sign-up-form").bind( "submit", function() 
	{
    	$.ajax({ type : "POST",
                 cache : false,
                 url: "/signup",
                 data: $(this).serializeArray(),
                 success:function(data)
                 { 
                 	$.fancybox(data); 
                 }
              });
        return false;
	});
	
	$('.drop-sports').click(function(){
	  $('.drop-sports-check').slideToggle();
	 });
	 
	$('.drop-sports-check ul li label').on('click', function() {
  		$(".drop-sports-check").hide();
	});
	 

	//Fancy jquery start		 
	$('.fancybox').fancybox();
	
});

$(window).resize(function() {
			 
	$(".team-two-block li h4").css('height','auto');
			 
	equalHeight($(".team-two-block li h4 "));
		
		
});

function equalHeight(group) {
	 var tallest = 0;
	 group.each(function() {
	 var thisHeight = jQuery(this).height();
	 if(thisHeight > tallest) {
	 tallest = thisHeight;
	 }
	 });
	 group.height(tallest);
}


