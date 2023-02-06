//Record video screen
boolean recordingOn = false;
int startTime = 0;
int captureTime = 5000;
float b = 0;
float barWidth = 0;
int countdownTime = 3000;
int videoCounter = 0;

void sceneEight(PGraphics scene){  
  scene.beginDraw();

  if (client2.newFrame()) {
    canvasSyphoner = client2.getGraphics(canvasSyphoner);
    image(canvasSyphoner, 0, 0, 640, 508);
  }

  videoLayer.beginDraw();
    videoLayer.image(canvasSyphoner, 0, 0, 640, 508); 
    //Cover rest of screen outside of video - openCV does not like background function
    videoLayer.fill(0);
    //videoLayer.rect(0,508,w,h-508);
    
    for(int i = 0; i < selectedToggles.size(); i++){
      videoLayer.fill(30);
      videoLayer.rect(w/2-100, 450+(30*i), 200,30);
      videoLayer.fill(255);
      videoLayer.text(selectedToggles.get(i), w/2-80, 470+(30*i));
    }
    
  videoLayer.endDraw();
  
  if(recordingOn){
    veCanvas.beginDraw();
    veCanvas.image(videoLayer, 0,0);
    veCanvas.endDraw();     
    
    if ((millis() > startTime)&&(millis() < startTime+countdownTime)){
      //b7.setVisible(false);
      videoCounter = floor((millis() - startTime)/1000);
      renderCounter(progressBarCanvas, videoCounter);      
    } else {
      renderProgressBar(progressBarCanvas);
      ve.saveFrame();   
    }

    scene.image(videoLayer,0,0);
    scene.image(progressBarCanvas,0,0);
    
    if (millis() > startTime+captureTime+countdownTime){
      endRecording();
      restartProgressBar(progressBarCanvas);
    } 
  } else {
    scene.image(videoLayer,0,0);
  }
  scene.endDraw();
}


void renderProgressBar(PGraphics barCanvas){
  barCanvas.beginDraw();
  //Hide record button
  barCanvas.fill(0);
  barCanvas.rect(w/2-50,h-350, 100, 40);  
  barCanvas.fill(255,255,255);
  barCanvas.rect(0,h-170,w, 50);
  
  //progress
  float b = (millis() - startTime - countdownTime)/5;
  float barWidth = lerp(0,w,b/1000);
  barCanvas.fill(255,0,0);
  barCanvas.rect(0,h-170,barWidth,50);  
  barCanvas.endDraw();
}

void restartProgressBar(PGraphics barCanvas){
  barCanvas.beginDraw();
  barCanvas.fill(0,0,0);
  barCanvas.rect(0,h-170,width,50);  
  barCanvas.endDraw();
}

void endRecording(){
  recordingOn = false;
  ve.dispose();
  
  println("Video created. Loading video in...");
  //myClient.write("videoCaptured");
  client2.stop();
  println("Syphon Client 2 disconnected"); 
  
  userVideo = new Movie(this, "gallery/"+userID + ".mp4");
  userVideo.loop();
  
  println("Video ready.");
  b9a.setVisible(true);
  b9b.setVisible(true);
  currentScene = 9;
}
