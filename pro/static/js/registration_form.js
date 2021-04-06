$(function(){
		
		$( "#registration_form" ).validate({
			  rules: {
				  username: {
			      required: true,	      
			    }
			  },
			  
			  messages: {
				  username: {
					  required: "User name is required" 
				  }
				  
			  } 
		});
		
		$("#register").click(function(){
			
			$("#registration_form").submit();
		});
		
	});