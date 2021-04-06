$(function(){
		
		$("#date_from").datepicker({
			'format': "dd/mm/yyyy",
			 startDate: new Date(),
		}).on('changeDate', function(ev) {
		    //Get actual date objects from both
		    var dt1 = $('#date_from').data('datepicker').viewDate;
		    var dt2 = $('#date_to').data('datepicker').viewDate;
		    if (dt2 < dt1) {
		        //If #dateEnd is before #dateStart, set #dateEnd to #dateStart
		        $('#date_to').datepicker('update', $('#date_from').val());
		    }
		    //Always limit #dateEnd's starting date to #dateStart's value
		    $('#date_to').datepicker('setStartDate', $('#date_from').val());
		    
		    calculationDuration();
		});
		
		$("#date_to").datepicker({
			'format': "dd/mm/yyyy",
			startDate: new Date(),
		}).on('changeDate', function(ev) {
		    //Get actual date objects from both
		    var dt1 = $('#date_from').data('datepicker').viewDate;
		    var dt2 = $('#date_to').data('datepicker').viewDate;
		    if (dt2 < dt1) {
		        //If #dateEnd is before #dateStart, set #dateEnd to #dateStart
		        $('#date_to').datepicker('update', $('#date_from').val());
		    }
		    //Always limit #dateEnd's starting date to #dateStart's value
		    $('#date_to').datepicker('setStartDate', $('#date_from').val());
		    
		    calculationDuration();
		});
		
		$("#date_from").change(function(){
			calculationDuration();
		});
		
		$("#date_to").change(function(){
			calculationDuration();
		});
		
		$("#vacation_form").validate({
			  rules: {
				  description: {
			      	required: true,	      
			      },
			      date_from: {
			    	  required: true,
			      },
			      date_to: {
			    	  required: true,
			      },
			      duration: {
			    	  required: true,
			      }
			  },
			  
			  messages: {
				  description: {
					  required: "Description is required" 
				  },
				  date_from:{
					  required: "Date from is required"
				  },
				  date_to: {
			    	  required: "Date to is required"
			      },
			      duration: {
			    	  required: "Duration is required",
			      }
				  
			  },
			  submitHandler: function(){
				  
				  $.ajax({
						type:"POST",
						url: $("form[name=vacation_form]").attr('action'),
						data:{
							description: $("input[name=description]").val(),
							date_from: $("input[name=date_from]").val(),
							date_to: $("input[name=date_to]").val(),
							duration: $("input[name=duration]").val(),
							vacation_id: $("input[name=vacation_id]").val(),
							csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
						},
						dataType: 'json',//json bcz data is dictionary
						success: function(response){
							console.log(response)
							
							if(response.status == 'OK'){
								toastr.success('Vacation Saved')
								var vacation_id = response.payload.id;
								$("input[name=vacation_id]").val(vacation_id);
							}else{
								if(response.message == "VACATION_NOT_FOUND"){
									toastr.error('Vacation not found')
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
			  }
		});
		
		
		$("#save_vacation").click(function(){
			$("#vacation_form").submit();
		});
	});
	
	function calculationDuration(){
		var date_from = $("#date_from").data('datepicker').viewDate;
		var date_to = $("#date_to").data('datepicker').viewDate;
		
		if(date_from && date_to){
			var duration = moment(date_to).diff(moment(date_from), 'days');
			
			$("input[name=duration]").val(duration);
		}
		
	}