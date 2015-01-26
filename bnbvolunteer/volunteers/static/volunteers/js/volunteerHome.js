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
        console.log(invalid_boolean);
        var invalid_boolean = {{invalid_boolean}};
        if (invalid_boolean){
        document.getElementById('invalid').style.display = 'none';
}
window.onload = doImmediately;


    $(document).ready(function() {  
        var invalid_boolean = "{{invalid_boolean}}";
        if (invalid_boolean === "False"){
        $("#invalid").hide();
    } 


});

  $(function() {
    $( "#datepicker" ).datepicker();
  });
