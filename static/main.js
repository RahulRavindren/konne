function convertFloat32ToInt16(buffer) {
  l = buffer.length;
  buf = new Int16Array(l);
  while (l--) {
    buf[l] = Math.min(1, buffer[l])*0x7FFF;
  }
  return buf.buffer;
}
function askAudioInput(){
	console.log('init audio');
	navigator.getUserMedia  = navigator.getUserMedia ||
                          navigator.webkitGetUserMedia ||
                          navigator.mozGetUserMedia ||
                          navigator.msGetUserMedia;
    var errorCallback = function(e) {
   	 console.log('rejected!', e);
  	};
  	navigator.getUserMedia({audio:true, video:false},function(stream){
  		console.log('start receiving stream');
  		alert('Recording audio');
  		audio_context = new AudioContext;
		var audioInput = audio_context.createMediaStreamSource(stream);
		var bufferSize = 4096;

		var recording = true;

		sampleRate = audio_context.sampleRate;
		
		var recorder = audio_context.createScriptProcessor(bufferSize, 1, 1);
   		recorder.onaudioprocess = function(e){
   			if(recording){
   				//stream audio 
	   			var socket_connect = io.connect('http://' + document.domain + ':' + location.port + "/streamaudio");
	   			socket_connect.on('connect', function(){
	   				console.log('connecting ....');
	   				var left = e.inputBuffer.getChannelData(0);
	   				socket_connect.emit('listenaudio', left);
	   			});
		   		var media_stop_elem = document.getElementById('media-stop');
		   		media_stop_elem.onclick = function(){
		   			console.log('going for disconnection....');
	   				var socket = io.connect('http://' + document.domain + ':' + location.port + "/disconnectstream");
	   				recording = false;
		   			socket.emit('disconnect');
		   			audioInput.disconnect(recorder);
		   			recorder.disconnect(audio_context.destination);
		   			//closing all socket connections
		   			socket.close();
		   			socket_connect.close();



		   		};
		   		media_stop_elem.classList.remove('hide');
   			}

   		};
   		 audioInput.connect(recorder);
   		recorder.connect(audio_context.destination);



  	},errorCallback);
}
window.onload = function(){

}