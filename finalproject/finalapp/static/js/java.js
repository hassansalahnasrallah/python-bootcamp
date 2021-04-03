
$(document).ready(function(){
  $("#event").on("click", function(){
	
	var datefrom=new Date($("#datefrom").val())
	var dateto=new Date($("#dateto").val())
  var Difference_In_Time = dateto.getTime() - datefrom.getTime();
  var Difference_In_Days = Difference_In_Time / (1000 * 3600 * 24); 

$("#duration").val(Difference_In_Days);
$("#save_vacation").attr("disabled", false);

  });
$("#datefrom").datetimepicker({ 
        format: "Y-m-d", 
          timepicker:false,
        onSelectDate: function(){
            startdate = new Date($("#datefrom").val());
            var data =$('#datefrom').val();
            var arr = data.split('-');
            DateFirst = new Date(arr[0],arr[1],arr[2])
     formattedDate =  startdate.getFullYear()+ "-" +(startdate.getMonth() + 1 ) + "-" + (startdate.getDate());
       console.log(DateFirst);
       console.log(formattedDate);
        }
      
         
    });

$("#dateto").datetimepicker({ 
        format: "Y-m-d", 
          timepicker:false,
        onSelectDate: function(){
            enddate = new Date($("#dateto").val());
           var data =$('#dateto').val();
            var arr = data.split('-');
            DateSecond = new Date(arr[0],arr[1],arr[2])
        formattedDate2= enddate.getFullYear()+ "-" +( enddate.getMonth() + 1 ) + "-" + (enddate.getDate());
           console.log(DateSecond);
           console.log(formattedDate2);
        }
      
         
    });

$("#save_vacation").click(function(){
	console.log($("form[name=VacationForm]").attr('action'))
	
   $.ajax({
			type:"POST",
			url: $("form[name=VacationForm]").attr('action'),
			data:{
				id: $("input[name=hidden]").val(),
				description: $("input[name=dsp]").val(),
				datefrom: $("input[name=datef]").val(),
				dateto: $("input[name=datet]").val(),
				duration: $("input[name=dura]").val(),
				csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
			},
			dataType:'json',
			success:function(){
				
				
			},
			error:function(){
				
				
			},
			
			
		})
		
    
    
  });

});

