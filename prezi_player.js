var player = new PreziPlayer('player-api-intro', { //id of div to embed into
	preziId: 'qxbj8zhqkxry', //id of prezi, visible in the url when you load the prezi on Prezi.com
	width: 620,
	height: 444
});



//make the prezi jump, when you click on a link
document.getElementById("link6").onclick = function(e){
	e.preventDefault();
	player.flyToStep(6);
};

//or in the other direction, highlight the link if prezi jumps to that step
player.on(PreziPlayer.EVENT_CURRENT_STEP, function(e) {
	oldLink.removeClass('active');
  	var stepIdx = e.value;
	$('select your link based on stepIdx').addClass('active');
});
