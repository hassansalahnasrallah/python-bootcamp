$().ready(function(){
	$("#vacation.html").validate({
		rules: {
			desc: "required",
		},
		
		messages: {
			desc: "please fill this input",
		
		},
	
	})
});