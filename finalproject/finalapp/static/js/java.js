
$(document).ready(function(){
  $("#event").click(function(){
	
	var datefrom=new date($("#datefrom").text().split(" ")[0])
	var dateto=new date($("#dateto").text().split(" ")[0])
  var Difference_In_Time = dateto.getTime() - datefrom.getTime();
  var Difference_In_Days = Difference_In_Time / (1000 * 3600 * 24); 
alert("Total number of days between dates  <br>"
               + datefrom + "<br> and <br>" 
               + dateto + " is: <br> " 
               + Difference_In_Days); 

  });

});