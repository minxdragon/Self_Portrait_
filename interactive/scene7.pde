//Record video screen
boolean recordingOn = false;
int startTime = 0;
int captureTime = 5000;
float b = 0;
float barWidth = 0;
int countdownTime = 3000;
int videoCounter = 0;

//TO DO: Black frame at start, look at adding a delay.

void sceneSeven(PGraphics scene){  
  scene.beginDraw();
  
  //if (client2.newFrame()) {
  //  sCanvas = client2.getGraphics(sCanvas);    
  //}

  if (client2.newFrame()) {
    canvasSyphoner = client2.getGraphics(canvasSyphoner);
    image(canvasSyphoner, 0, 0, 640, 508);
  }

  videoLayer.beginDraw();
  //int w = 608;int h = 1080;

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
      b7.setVisible(false);
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
  //barCanvas.fill(255,0,0);
  //barCanvas.rect(w/2, h-300,200,20);
  //barCanvas.fill(255);
  //barCanvas.text("Recording...", w/2, h-300);
  
  barCanvas.fill(255,255,255);
  barCanvas.rect(0,h-170,w, 50);
  
  //progress
  float b = (millis() - startTime - countdownTime)/5;
  float barWidth = lerp(0,w,b/1000);
  //println(b);
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

void defineGUISeven(){
  //b7 = sceneGUI.addButton("sceneSevenButton")
  //             .setLabel("Record clip")
  //             .setPosition(width/2-50,height-100)
  //             .setSize(100,40)
  //             .setColorLabel(color(0, 0, 0))
  //             .setColorBackground(color(255, 255, 255));
  //b7.hide();
  
  b7 = new GButton(this, w/2-50,h-350, 100, 40);
  b7.setText("Record clip");
  b7.addEventHandler(this, "sceneSevenButton");
  b7.setVisible(false);
}

public void sceneSevenButton(GButton source, GEvent event) {
  println("a button event from sceneSevenButton: "+event);
  
  recordingOn = true;
  ve.setMovieFileName("data/gallery/"+ userID + ".mp4");
  ve.startMovie();
  println("Starting to record...");
  startTime = millis();

  b7.setVisible(false);
}

void endRecording(){
  recordingOn = false;
  ve.dispose();
  
  println("Video created. Loading video in...");
  myClient.write("videoCaptured");
  userVideo = new Movie(this, "gallery/"+userID + ".mp4");
  userVideo.loop();
  
  println("Video ready.");
  //b8a.show();
  //b8b.show();
  b8a.setVisible(true);
  b8b.setVisible(true);
  currentScene = 8;
}
