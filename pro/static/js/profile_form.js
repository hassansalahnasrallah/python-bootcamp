
	$(function(){
		
		 $( "#profile_form" ).validate({
			  rules: {
				
				position: {
				      required: true,	      
				},
				
				date_of_birth: {
				      required: true,	      
				},
				
				profile_img: {
				      required: true,	      
				},
				   
		
			  },
			  
			  messages: {
		
				  position: {
				      required: "Position name is required"	      
				  },
				
				  date_of_birth: {
				      required: "Date of birth is required"	      
				  },
				
				  profile_img: {
				      required: "Picture is required"	      
				  },
			    
			  },
		
			  submitHandler: function(){
				  
				  var formData = new FormData();
				    
			    	formData.append('profile_img', $('input[name=profile_img]')[0].files[0]); 
			    	formData.append('date_of_birth', $('input[name=date_of_birth]').val());
			    	formData.append('position', $('input[name=position]').val());
			    	formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
				  
				  $.ajax({
						method:"POST",
						url:"{% url 'save_profile' %}",
						data: formData,
				        processData: false,
				        contentType: false,
						success: function(response){
							var response = JSON.parse(response)
							
							console.log(response.payload)
							if(response.status == 'OK'){
								toastr.success('Save success')
								$("#image_1").attr('src', '{{MEDIA_URL}}'+response.payload.image_url)
							}else{
								if(response.message == "SYSTEM_ERROR"){
									toastr.error('Fail to save')									
								}
							}	
					    }, 
					    error: function(){
					    	toastr.error('Error in save')
						}
					});

			  }
		
		 });
		
		
		 $("#save_profile").click(function(){
			 $("#profile_form").submit();
	
		 });		
		
		
		$("#date_of_birth").datepicker({
			'format':"dd/mm/yyyy",
	    });
		
	});
