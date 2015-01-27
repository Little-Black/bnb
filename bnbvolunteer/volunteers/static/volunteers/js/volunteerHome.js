var counter = 1;
var limit = 15;
function addInput(divName){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Entry " + (counter + 1) + " <input type='text' name='myInputs'>";
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}
function doImmediately() {
    $('#tohide').hide();
        
        // var invalid_boolean = {{invalid_boolean}};
        if (invalid_boolean){
          document.getElementById('invalid').style.display = 'none';
   }
     var invalid_boolean = "{{invalid_boolean}}";
     if (invalid_boolean === "False"){
        $("#invalid").hide();
   }
}
window.onload = doImmediately;


//     $(document).ready(function() {  

//     } 


// });

  $(function() {
    $( "#datepicker" ).datepicker();
  });

  function validateForm() {
     var y = document.forms["newLogForm"]["date"].value;
    if (y == null || y == "") {
        alert("Please enter a date.");
        return false;
    }
    var x = document.forms["newLogForm"]["activityType"].value;
    if (x == null || x == "") {
        alert("Please select an activity type.");
        return false;
    }

}





