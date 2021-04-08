$(function(){
		
		$( "#login_form" ).validate({
			  rules: {
				  username: {
			      required: true,	      
			    },
	
				 password: {
				      required: true,	      
				},
					
			  }, 
			  
			  messages: {
				  username: {
					  required: "User name is required" 
				  },
				  
				  password: {
				      required: "Password is required",	      
				  },
						  
			  } 
		});
		
		$("#login").click(function(){
			$("#login_form").submit();
		});
		
	});