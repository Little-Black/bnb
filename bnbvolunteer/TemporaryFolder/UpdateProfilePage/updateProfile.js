var changingPassword = false;
$(".change-password-btn").click(function(){
	if (!changingPassword){
		changingPassword = true;
		$(".changing-password-fields").css("display", "block");
	}else{
		changingPassword = false;
		$(".changing-password-fields").css("display", "none");
	}
});