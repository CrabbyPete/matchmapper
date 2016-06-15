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
	

	$('.drop-sports').click(function(){
	  $('.drop-sports-check').slideToggle();
	 });
	 

	$('.map-pop-icon').hover(function(){
		$('.map-pop').fadeIn();
	},function(){
		$('.map-pop').fadeOut();
	});
		
	
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
	
	$("#sign-in-form").bind( "submit", function() 
	{
    	$.ajax({ type : "POST",
                 cache : false,
                 url: "/signin",
                 data: $(this).serializeArray(),
                 success:function(data)
                 { 
                 	$.fancybox(data); 
                 }
              });
        return false;
	});
	
	
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
	 
	 
	 
	$('.map-pop-icon').hover(function(){
		$('.map-pop').fadeIn();
	},function(){
		$('.map-pop').fadeOut();
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


