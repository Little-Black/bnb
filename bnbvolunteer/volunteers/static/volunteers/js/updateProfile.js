var changingPassword = false;
var startRepeat = false;
$(".change-password-btn").click(function(){
	if (!changingPassword){
		changingPassword = true;
		$(".changing-password-fields").css("display", "block");

		$(".new-password-input2").keyup(function(){
			console.log("keyup working");
			var newPass2 = $(".new-password-input2").val();
			// console.log("keyup working");
			if (!startRepeat){ 
				startRepeat = true;
			}else if (newPass2 == ""){
				//make sure note goes away, since the user is starting over.
				$(".password-note").text("");
				console.log("CLEAR");
			}else{
				var otherPassword = $(".new-password-input").val();

				if ( $(".new-password-input2").val() == $(".new-password-input").val() ){

				}
			}
		});
	}else{
		changingPassword = false;
		$(".changing-password-fields").css("display", "none");
	}
});

// var startRepeat = false;
$(".zip-input").keyup(function(){
	console.log("keyup working");
	// var newPass2 = $(".new-password-input2").val();
	// console.log("keyup working");
	// if (!startRepeat){ 
	// 	startRepeat = true;
	// }else if (newPass2 == ""){
	// 	//make sure note goes away, since the user is starting over.
	// 	$(".password-note").text("");
	// 	console.log("CLEAR");
	// }else{
	// 	var otherPassword = $(".new-password-input").val();

	// 	if ( $(".new-password-input2").val() == $(".new-password-input").val() ){

	// 	}
	// }
});

// //Checks if the user is ready to sign up. If so, we enable the sign up button. If not, we disable it.
// function checkIfUserIsReadyToSignUp(){
// 	var password1 = $('.passwordField-signup').val();
// 	var password2 = $('.passwordconfirmField-signup').val();

// 	var samePassword = comparePasswords();

// 	var username = $('.usernameField-signup').val();

// 	//If the user has entered a username and the passwords are the same.
// 	if (trimSpaces(username) !== '' && samePassword){
// 		$('.signup-btn').prop("disabled",false);
// 	}
// 	else{
// 		$('.signup-btn').prop("disabled",true);
// 	}
// }

//Trims the spaces at the beginning and end of a given string
function  trimSpaces(string){
	return string.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
}

//Checks the password fields and returns true if they are the same. Returns false otherwise.
//Exception: Also returns true if both password fields are emtpy.
function  comparePasswords(){
	var password1 = $('.new-password-input').val();
	var password2 = $('.new-password-input2').val();

	if (trimSpaces(password1) === '' && trimSpaces(password2) === ''){
		$('.password-note').removeClass('confirmed');
		$('.password-note').removeClass('notconfirmed');
		$('.password-note').html('');
		$('.submit-btn').prop("disabled",false);

		return false;
	}
	else if (trimSpaces(password1) === trimSpaces(password2)){
		$('.password-note').removeClass('notconfirmed');
		$('.password-note').addClass('confirmed');
		$('.password-note').html("Passwords match");
		$('.submit-btn').prop("disabled",false);

		return true;
	}
	else{
		$('.password-note').removeClass('confirmed');
		$('.password-note').addClass('notconfirmed');
		$('.password-note').html("Passwords don't match");
		$('.submit-btn').prop("disabled",true);

		return false;
	}
}