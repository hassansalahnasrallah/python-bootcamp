
	$(function(){
		
		$("#save_profile").click(function(){

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
							alert("save success");
							$("#image_1").attr('src', '{{MEDIA_URL}}'+response.payload.image_url)
							
						}else{
							if(response.message == "FAIL"){
								alert("Fail to save");
							}else if(response.message == "NAME_EXISTS"){
								alert("This topic already found");											
							}else if(response.message == "MISSING_REQUIRED_PARAMETERS"){
								alert("You have missing parameters");
							}
						}	
				    }, 
				    error: function(){
				    	alert("Error in save")
					}
				});
			 
		});	
	});

