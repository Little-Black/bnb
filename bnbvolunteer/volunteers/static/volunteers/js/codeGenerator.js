$(document).ready(function(){
    $('#date1').datepicker({format: "yyyy-mm-dd"});
    $('#date2').datepicker({format: "yyyy-mm-dd"});
});

var counter = 1;
var limit = 15;
function addInput(divName){
    if (counter == limit)  {
        alert("You have reached the limit of adding " + counter + " kinds of vouchers");
    }
    else {
        var newdiv = document.createElement('div');
        counter++;
        // '<p class="counter'+counter+'">'+counter+'</p>'+
	    newdiv.innerHTML = '<p class="voucher-points">Voucher Points:</p><input type="text" name="myInputs'+counter+'">'+
	    '<p class="how-many">How many?:</p><input type="text" name="myInputs'+counter+'">'
        document.getElementById(divName).appendChild(newdiv);   
    }
}