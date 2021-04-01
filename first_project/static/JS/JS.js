$(document).ready(function(){
var startdate,enddate;
var formattedDate,formattedDate2;
var DateFirst;
var DateSecond;

$("#date_from").datetimepicker({ 
        format: "Y-m-d", 
          timepicker:false,
        onSelectDate: function(){
            startdate = new Date($("#date_from").val());
            var data =$('#date_from').val();
            var arr = data.split('-');
            DateFirst = new Date(arr[0],arr[1],arr[2]);
     formattedDate =  startdate.getFullYear()+ "-" +(startdate.getMonth() + 1 ) + "-" + (startdate.getDate());
       console.log(DateFirst);
       console.log(formattedDate);
        }
      
         
    });

$("#date_to").datetimepicker({ 
        format: "Y-m-d", 
          timepicker:false,
        onSelectDate: function(){
            enddate = new Date($("#date_to").val());
    	   var data =$('#date_to').val();
            var arr1 = data.split('-');
          DateSecond= new Date(arr1[0],arr1[1],arr1[2]);
           console.log(moment(enddate).format("MMM Do YY"));
           formattedDate2= enddate.getFullYear()+ "-" +( enddate.getMonth() + 1 ) + "-" + ( enddate.getDate());
           console.log(DateSecond);
           console.log(formattedDate2);
        }
      
         
    });

$("#ButtonCal").click(function(){
	  var data =$('#date_from').val();
      var arr = data.split('-');
      DateFirst = new Date(arr[0],arr[1],arr[2])
	 var data =$('#date_to').val();
     var arr1 = data.split('-');
      DateSecond= new Date(arr1[0],arr1[1],arr1[2]);
      
	var timediff =  DateSecond.getTime() - DateFirst.getTime();
	console.log(timediff);
	var days = timediff/(1000*3600*24);
	console.log(days);
	$("#durationField").val(parseInt(days));
	
	});

$("#vacation_grid").DataTable({
	
     ajax : {
		url:$("#vacation_grid").attr('data-url'),
		dataSrc: 'data',
		type:'POST',
	    data: function(d){
		d.csrfmiddlewaretoken=$("input[name=csrfmiddlewaretoken]").val();
	}
	},
	
	lengthMenu: [5,10,25,50],
    pageLength: 10,
	
   
	processing:true,
	serverSide:true,
	
	columns:[{'data':'description','name':'description'}],
	
	
});
$("#SignUpForm").validate({
	rules:{
		email:{required:true,
		      email:true},
	},
	 messages:{
		email:"Please enter a valid email",
	},
	
});
$("#loginForm").validate({
	
	rules:{
		
	   username:{required:true},
	   password:{required:true},
			
	},
	 messages:{
		 username:"this field is required",
	     password:"this field is required",
	},
	
});
$("#savedHomePage").click(function(){
	
	$.ajax({
		type:"POST",
		url:$("form[name=HomePageView]").attr('action'),
		data:{
			idOfVaca:$("input[name=idOfVaca]").val(),
			text_area :$("#text").val(),
			datefrom:$("input[name=datefrom]").val(),
			dateto:$("input[name=dateto]").val(),
			duration_field:$("input[name=duration_field]").val(),
			csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
			
			
		},
		dataType:'json',
		success: function(response){
			console.log(response)
			
		},
		error : function(){
			  
		},
	});
});


$("#date_ofbirth").datetimepicker({ 
        format: "Y-m-d", 
        timepicker:false,
});
$("#ProfilePage").validate({
	
	rules:{
		
		JobPostion:{required:true},
		dateofbirth:{required:true},
		file:{required:true},
			
	},
	 messages:{
		 JobPostion:"this field is required",
         dateofbirth:"this field is required",
         file:"Image is required",
	},
	submitHandler: function() {
       	var formData = new FormData();
	formData.append('JobPostion',$("input[name=JobPostion]").val());
	formData.append('file',$("input[name=file]")[0].files[0]);
	formData.append('dateofbirth',$("input[name=dateofbirth]").val());
	
	if($("input[name=user_name]").val()!=undefined){
	formData.append('user_name',$("input[name=user_name]").val());
	}

	formData.append('csrfmiddlewaretoken',$("input[name=csrfmiddlewaretoken]").val());
	$.ajax({
		method:"POST",
		url:$("form[name=ProfilePageView]").attr('action'),
		data: formData,
		processData:false,
		contentType:false,
		
		success: function(){
			
		},
		error : function(){
			  
		},
	});
      }
	
});

$("#SaveProfile").click(function(){
	$("#ProfilePage").submit();

});

});