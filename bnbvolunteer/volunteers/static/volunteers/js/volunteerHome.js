var counter = 1;
var limit = 15;
function addInput(divName){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Entry " + (counter + 1) + " <input type='text' class='codeEntry' name='myInputs'>";
          document.getElementById(divName).appendChild(newdiv);
          counter++;

          //THIS LISTENER BELOW NEEDS TO BE IN THIS JAVASCRIPT TWICE, 
          // below for the first code entry and here for after 
          // each additional entry field is added to the page 
          $( ".codeEntry" ).keydown(function(e){
            var key = e.keyCode;
            if ((key >= 96 && key <= 105) || (key >= 48 && key <= 57) || (key >= 65 && key <= 90)) { //keyCode checks which character the user is entering
              // Do nothing (for some reason, doing ![the statement in the 'if' statement] wasn't working...)
            }else{
              e.preventDefault(); //prevents anything other than a number or letter to be entered
            }
          });
     }
}
function doImmediately() {
        
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

  $(function() {
    $( "#datepicker" ).datepicker();

    //THIS LISTENER BELOW NEEDS TO BE IN THIS JAVASCRIPT TWICE, 
    // here for the first code entry and above for after 
    // each additional entry field is added to the page 
    $( ".codeEntry" ).keydown(function(e){
      var key = e.keyCode;
      if (key == 8 || key == 9 || key == 13 || (key >= 96 && key <= 105) || (key >= 48 && key <= 57) || (key >= 65 && key <= 90)) { //keyCode checks which character the user is entering
        // Do nothing (for some reason, doing ![the statement in the 'if' statement] wasn't working...)
      }else{
        e.preventDefault(); //prevents anything other than a number or letter to be entered
      }
    });

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
