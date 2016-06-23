var manifestUri = '//storage.googleapis.com/shaka-demo-assets/angel-one/dash.mpd';

function initApp() {
  // Install built-in polyfills to patch browser incompatibilities.
  shaka.polyfill.installAll();

  // Check to see if the browser supports the basic APIs Shaka needs.
  if (shaka.Player.isBrowserSupported()) {
    // Everything looks good!
    initPlayer();
  } else {
    // This browser does not have the minimum set of APIs we need.
    console.error('Browser not supported!');
  }
}

function initPlayer() {
  // Create a Player instance.
  var video = document.getElementById('video');
  if(Hls.isSupported()) {
    var hls = new Hls();
    manifestUri = video.getAttribute("source");
    hls.loadSource(manifestUri);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED,function() {
      video.play();
    });
  }
  //var player = new shaka.Player(video);

  //player.configure({'streaming':
    //{'rebufferingGoal': 5, 'bufferingGoal': 10}});

  // Attach player to the window to make it easy to access in the JS console.
  //window.player = player;

  // Listen for error events.
  //player.addEventListener('error', onErrorEvent);
  //manifestUri = video.getAttribute("source");

  // Try to load a manifest.
  // This is an asynchronous process.
  //player.load(manifestUri).then(function() {
    // This runs if the asynchronous load is successful.
    //console.log('The video has now been loaded!');
  //}).catch(onError);  // onError is executed if the asynchronous load fails.
}

function onErrorEvent(event) {
  // Extract the shaka.util.Error object from the event.
  onError(event.detail);
}

function onError(error) {
  // Log the error.
  console.error('Error code', error.code, 'object', error);
}

//document.addEventListener('DOMContentLoaded', initApp);
