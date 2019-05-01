function on(id) {
  document.getElementById("full-overlay").style.display = "block";
  document.getElementById(id).style.display = "flex";

}

function off() {
  document.getElementById("full-overlay").style.display = "none";
  $('audio').each(function(){
  		this.pause(); // Stop playing
  			this.currentTime = 0; // Reset time
  		}); 
  $('div[id^="div-"]').hide();
}
