$(document).ready(function(){
var startdate,enddate;
var formattedDate,formattedDate2;
var DateFirst;
var DateSecond;
 $("#SpecialButton2").html(">");
 $("#SpecialButton1").html("<");
 var save=4;
 var i=1;

$("button").click(function(){
	var image_src = document.querySelector("#Images");
    console.log(image_src.getAttribute('src'))
	 var image=["/static/IMAGE/PhotographyImage1.png","/static/IMAGE/photographyimage3.png", "/static/IMAGE/travel5.jpg", "/static/IMAGE/travel8.jpg"];
          var valButton = this.id;
            
            if(valButton=="SpecialButton2"){
               if(i < 4 )
               {
                
         image_src.setAttribute('src',image[i]);
      
                 save=i;
                   i=i+1;
                 
                  
                }else{
                    i=0;
          image_src.setAttribute('src',image[0]);
       
         
                     save=i;
                    i=i+1;
                  
                    
                }
               }
            else if(valButton=="SpecialButton1"){
               
               
                if(save>0)
                    {
                      save=save-1; 
             image_src.setAttribute('src',image[save]);   
                    i=save+1;
                        
              }else{
                    save=3;
               image_src.setAttribute('src',image[save]);
                  i=save+1;
                   
                }
               
	}
	
})
$("#date_from").datetimepicker({ 
        format: "Y-m-d", 
          timepicker:false,
        onSelectDate: function(){
            startdate = new Date($("#date_from").val());
            var data =$('#date_from').val();
            var arr = data.split('-');
            DateFirst = new Date(arr[0],arr[1],arr[2])
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
      DateSecond= new Date(arr1[0],arr1[1],arr1[2])
      
	var timediff =  DateSecond.getTime() - DateFirst.getTime();
	console.log(timediff);
	var days = timediff/(1000*3600*24);
	console.log(days);
	$("#durationField").val(parseInt(days));
	
	})
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
		success: function(){
			
		},
		error : function(){
			  
		},
	});
});

});