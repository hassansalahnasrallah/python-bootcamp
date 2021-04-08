$(document).ready(function(){
var startdate,enddate;
var formattedDate,formattedDate2;
var DateFirst;
var DateSecond;

 function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Description:</td>'+
            '<td>'+d.description+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Date_From:</td>'+
            '<td>'+d. datetimefrom+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Date_to:</td>'+
            '<td>'+d.datetimeto+'</td>'+
        '</tr>'+
        '<tr>'+
        '<td>Duration:</td>'+
        '<td>'+d.Duration+'</td>'+
    '</tr>'+
    '</table>';
}  

/*
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
      
         
    }).on('changeDate', function (ev) {
  var date_from1 = $("#date_from").data("datetimepicker").getDate();
   var date_to2 = $("#date_to").data("datetimepicker").getDate();
if (date_to2 < date_from1){
	console.log($('#date_to').data("DateTimePicker").options());
	$("#date_to").datetimepicker('option', 'minDate', $("#date_from").val());
}
$("#date_to").datetimepicker('startDate',$("#date_from").val());

});
*/
/*$("#ButtonCal").click(function(){
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
*/
function calculationDuration(){
		var date_from = $("#date_from").data('datepicker').viewDate;
		var date_to = $("#date_to").data('datepicker').viewDate;
		
		if(date_from && date_to){
			var duration = moment(date_to).diff(moment(date_from), 'days');
			
			$("input[name=duration_field]").val(duration);
		}
		
	}
	$("#date_from").datepicker({
			'format': "yyyy-mm-dd",
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
			'format': "yyyy-mm-dd",
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

$("#SignUpForm").validate({
	rules:{
		email:{required:true,
		      email:true},
	},
	 messages:{
		email:"Please enter a valid email",
	},
	
});

var vacation_table = $("#vacation_grid").DataTable({
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
	
    responsive: true,    

	processing:true,
	serverSide:true,
	
	columns:[
	/*	{
               "className":      'details-control',
               "orderable":      false,
               "data":           null,
               "defaultContent": ''
           },*/
	
	{'data':'description','name':'description'},
	{'data':'datetimefrom','name':'datetimefrom'},
	{'data':'datetimeto','name':'datetimeto'},
	{'data':'Duration','name':'Duration'},
	{'data':'status','name':'status'},
	{'data':'action'}],
	/* "order": [[1, 'asc']],*/
	columnDefs:[
		{
		targets: -1,
		title:"Actions",
		render: function(data , type, row, meta){
			console.log(row);
			console.log(type);
		var edit_id = "/url/HomePage/?id=" + row.id;
	     

	 return "<a href='"+edit_id+"'>Edit</a> <button type='button' class='btn btn-success btn-sm btn-update' data-id='"+row.id+"'><i class='fa fa-check-circle' style='font-size:10px;'></i></button> <button type='button' class='btn btn-success btn-sm btn-delete' data-id='"+row.id+"'><i class='fa fa-trash' style='font-size:10px;'></i></button>" ;
     // return "<a href='#'>Edit</a>";
		}
		
	}],
	createdRow: function(row, data, dataIndex){
		console.log(data)
		if(data['status'] == "Active"){
			$(row).css({'background-color': "#85BB65"})
		}else{
			$(row).css({'background-color': "red"})
		}
	},

	
	
});
/*$('#vacation_grid tbody').on('click', 'td.details-control', function () {
                var tr = $(this).closest('tr');
                var row = vacation_table.row( tr );
         
                if ( row.child.isShown() ) {
                    // This row is already open - close it
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {
                    // Open this row
                    row.child( format(row.data()) ).show();
                    tr.addClass('shown');
                }
            } );*/
 $('#vacation_grid tbody').on('click', '.btn-update', function (){
 
   // $("#modal_update").show();
$("#modal_update").modal('show');
    $("input[name=vacation_Id]").val($(this).attr('data-id'));

});
$("#btnclose,#close_status").click(function(){
    //$("#modal_update").hide();
$("#modal_update").modal('hide');
        });
$("#btn_close_delete,#NDelete_status").click(function(){
    //$("#modal_update").hide();
$("#modal_delete").modal('hide');
        });

$("#update_status").click(function(){
    $.ajax({
				type:"POST",
				url: "/update_status/",
				data:{
					vacation_Id: $("input[name=vacation_Id]").val(),
					csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
				},
				dataType: 'json',
				success: function(response){
					
					if(response.status == 'OK'){
						toastr.success('Vacation status updated');
						vacation_table.ajax.reload(); 
						$("#modal_update").modal('hide');
					}else {
						if(response.message == "VACATION_NOT_FOUND"){
							toastr.error('Vacation not found')											
						}else if(response.message == "MISSING_REQUIRED_PARAMETERS"){
							toastr.success("You have missing parameters");
						}
					}	
			    }, 
			    error: function(){
			    	alert("Error in save")
				}
			});
        });
$('#vacation_grid tbody').on('click', '.btn-delete', function (){
 
   // $("#modal_update").show();
$("#modal_delete").modal('show');
    $("input[name=vacation_id]").val($(this).attr('data-id'));

});
$("#Delete_status").click(function(){
				$.ajax({
					type:"POST",
					url: "/delete_vacation/",
					data:{
						vacation_id: $("input[name=vacation_id]").val(),
						csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
					},
					dataType: 'json',
					success: function(response){
						console.log(response)
						
						if(response.status == 'OK'){
							toastr.success('Vacation deleted Successfully');
							vacation_table.ajax.reload(); 
							$("#modal_delete").modal('hide');
						}else{
							if(response.message == "VACATION_NOT_FOUND"){
								toastr.error('Vacation not found')											
							}else if(response.message == "MISSING_REQUIRED_PARAMETERS"){
								toastr.success("You have missing parameters");
							}
						}	
				    }, 
				    error: function(){
				    	toastr.success("Error in delete");
					}
				});
			});
			
			

$("#vacation_grid tfoot th[data-searchable='true']").each(function(){
	
	var title = $(this).text();
	$(this).html('<input type="text" placeholder="Search '+ title +'">');
	
	
	
});

//input le ma7tot bel footer bel on change  
vacation_table.columns().every( function () {
	var column=this;
	// input le mawjoud bl footer 3al on change lal text bel search
	 $( 'input', this.footer() ).on( 'change keyup', function () {
                    if ( column.search() !== this.value ) {
	// bas 8ayer lvalue ya3mly executipon w y7otoly search  la haydy lvalue
                       column.search( this.value ).draw();
                    }
                   })
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