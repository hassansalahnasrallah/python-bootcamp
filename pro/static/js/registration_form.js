$(function(){
		
		$( "#registration_form" ).validate({
			  rules: {
				  username: {
			      required: true,	      
			    },
	
			      email: {
				      required: true,	      
				},
				
				 password: {
				      required: true,	      
				},
				
				first_name: {
				      required: true,	      
				},
				
				last_name: {
				      required: true,	      
				},
				
				position: {
				      required: true,	      
				},
				
				date_of_birth: {
				      required: true,	      
				},
				
				picture: {
				      required: true,	      
				},
				   
		
			  },
			  
			  messages: {
				  username: {
					  required: "User name is required" 
				  },
				  
				  email: {
				      required: "Email is required"	      
				  },
				
				  password: {
				      required: "Password is required",	      
				  },
				
				  first_name: {
				      required: "First name is required"	      
				  },
				
				  last_name: {
				      required: "Last name is required"	      
				  },
				
				  position: {
				      required: "Position name is required"	      
				  },
				
				  date_of_birth: {
				      required: "Date of birth is required"	      
				  },
				
				  picture: {
				      required: "Picture is required"	      
				  },
			  
			  
			  
				  
			  } 
		});
		
		$("#register").click(function(){
			
			$("#registration_form").submit();
		});
		
		
		//$("#date_of_birth").datepicker({
			//'format':"dd/mm/yyyy",
		//});
		
	});
