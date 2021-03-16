function duration()
{ var fromdate= new date(document.getElementbyId("from").value);
 var todate= new date(document.getElementbyId("to").value);

var result=todate.getDate()- fromdate.getDate()/(1000*24*3600);

document.getElementbyId("duration")=result;
}
