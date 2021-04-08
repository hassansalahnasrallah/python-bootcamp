	<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.js"></script>
	function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Description:</td>'+
            '<td>'+d.description+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extension number:</td>'+
            '<td>'+d.date_from+'</td>'+
        '</tr>'+
        
    '</table>';
}
 

	$(function(){
		
		var vacay_table = $('#vacation_table').DataTable({
			responsive : true,
			//"searching":false,
			

			ajax: {
				url: '{% url "vacation_grid" %}',
				type: 'POST',
				data: function(d){
					d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val(),
					d.user_id = "{{request.user.id}}" //$("input[name=user_id]").val()
					//{{django_topic_id}} w bruh 3al context
					
				}
			},

			lengthMenu: [1, 5, 10, 25, 50 ],
			
			pageLength: 10,
			
			processing: true,
			serverSide: true,
			
			columns: [
				{
	                "className":      'details-control',
	                "orderable":      false,
	                "data":           null,
	                "defaultContent": ''
	            },
				
				{'data': 'description', 'name': 'description', 'sortable':true},
				{'data': 'date_from', 'name': 'date_from', 'sortable':true},
				{'data': 'date_to', 'name': 'date_to', 'sortable':true},
				{'data': 'duration', 'name': 'duration', 'sortable':true},
				{'data': 'status', 'name': 'status'},
				{'data': 'action'}
			
				],
			
				"order": [[1, 'asc']],
			columnDefs: [
				{
					targets: -1, //or 3
					title: 'Actions',
					render: function(data, type, full, meta){
						var edit_url = "{% url 'vacation_form' %}?id=" + full.id;
						return " <button class='btn btn-dark btn-sm btn-edit' type='button' ><i class='fa fa-pencil-square-o' aria-hidden='true'></i></button> <button class='btn btn-dark btn-sm btn-update' type='button' data-id="+full.id+"><i class='fa fa-refresh' aria-hidden='true'></i></button> <button class='btn btn-dark btn-sm btn-delete' type='button' data-id="+full.id+"><i class='fa fa-trash' aria-hidden='true'></i></button>"
					}
					
				}
			],
			
			createdRow: function(row, data, dataIndex){
				console.log(data)
				if(data['status'] == "Active"){
					$(row).css({'background-color': "white"})
				}else{
					$(row).css({'background-color': "#ff5656"})
				}
			}
		});
		
		$("#vacation_table tfoot th[data-searchable=true]").each(function(){
			var title = $(this).text();
			$(this).html('<input type="text" placeholder="Search '+title+'"/>');
		});
		
		vacay_table.columns().every(function(){
			var column = this;
			$('input',this.footer()).on('change',function(){
				if(column.search()!== this.value){
					column.search(this.value).draw();
				}
			})
		});
		
		//$("#vacation_table tbody").on('click', '.btn-edit', function(){
			
		//});
		
		$("#vacation_table tbody").on('click', '.btn-update', function(){
			//show dialog
			console.log(2)
			$("#vacation_status_modal").show();
			$("input[name=vacation_id]").val($(this).attr('data-id'));
		});
		
		$("#hide_modal").click(function(){
				
				$("#vacation_status_modal").hide();
		});
		
		$("#save_status").click(function(){
			$.ajax({
				type:"POST",
				url: "{% url 'update_status' %}",
				data:{
					vacation_id: $("input[name=vacation_id]").val(),
					csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
				},
				dataType: 'json',//json bcz data is dictionary
				success: function(response){
					console.log(response)
					
					if(response.status == 'OK'){
						toastr.success('Vacation status updated');
						vacay_table.ajax.reload(); //to auto update table on success
						$("#vacation_status_modal").hide();
					}else{
						if(response.message == "VACATION_NOT_FOUND"){
							toastr.error('Vacation not found')										
						}
					}	
			    }, 
			    error: function(){
			    	toastr.error('An Error Has Occured')
				}
			});
		});
		
		
		$("#vacation_table tbody").on('click', '.btn-delete', function(){
			
			$("#delete_vacation_modal").show();
			$("input[name=vacation_id]").val($(this).attr('data-id'));
		});
		
		 $("#close_modal").click(function(){
			
			$("#delete_vacation_modal").hide();
		 });
		 
		 $("#delete_vacation").click(function(){
				$.ajax({
					type:"POST",
					url: "{% url 'delete_vacation' %}",
					data:{
						vacation_id: $("input[name=vacation_id]").val(),
						csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
					},
					dataType: 'json',//json bcz data is dictionary
					success: function(response){
						console.log(response)
						
						if(response.status == 'OK'){
							toastr.success('Vacation deleted successfuly');
							vacay_table.ajax.reload(); //to auto update table on success
							$("#vacation_status_modal").hide();
						}else{
							if(response.message == "VACATION_NOT_FOUND"){
								toastr.error('Vacation not found')											
							}
						}	
				    }, 
				    error: function(){
				    	toastr.error('An Error Has Occured')
					}
				});
			});
		
	});

	
	
	$('#vacation_table tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
 
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
    });
		