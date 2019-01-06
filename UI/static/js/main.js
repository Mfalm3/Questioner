let button = document.getElementById('new-meetup');
let myModal = document.getElementById('modalCreate');
let close = document.getElementsByClassName('close')[0];

button.onclick = function() {
	myModal.style.display = "block";
}

close.onclick = function() {
	myModal.style.display = "none";
}

window.onclick = function(e) {
	if(e.target == myModal){
		return false;
	}
}
