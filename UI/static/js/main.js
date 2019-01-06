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

function deleter(){

	if(confirm("Are you sure you want to delete this meetup?")){

		if(confirm("Are you really sure you want to delete this meetup?")){
			let box = document.querySelector('.buttonz-alert').parentNode.closest('.box');
			box.remove();
			setTimeout(()=>{ alert("Meet up deleted successfully!"); }, 100);
		}else{
			return false;
		}
 	
 	}else{
 		return false;
 	}
	
	
}