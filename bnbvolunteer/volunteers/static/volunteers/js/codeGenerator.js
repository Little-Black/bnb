// Returns a random integer between min (included) and max (included)
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

var alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];

//Returns a string of a random capitalized letter of the alphabet 
function getRandomLetter(){
	var letterInt = getRandomInt(0,25);
	return alphabet[letterInt];
}

//Generates an 8-digit-long random code that alternates between capital letters and numbers 1-9
function generateCode(){
	var code = "";
	for (var i=0; i<8; i++){
		if (i%2 == 0){
			var letter = getRandomLetter();
			code = code + letter;
		}else{
			var integer = getRandomInt(1, 9);
			code = code + integer;
		}
	}

	return code;
}

// console.log("Random code:"+generateCode());
$(".generate-code-btn").click(function(){
	var code = generateCode();
	console.log("Random code:"+code);
	$(".codeAppear").html(code);
});