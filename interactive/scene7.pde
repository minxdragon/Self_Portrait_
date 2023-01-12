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
  
  if (client.newFrame()) {
    sCanvas = client.getGraphics(sCanvas);    
  }
  
  videoLayer.beginDraw();
    videoLayer.image(sCanvas, 0, 0, 640, 508); 
    //Cover rest of screen outside of video - openCV does not like background function
    videoLayer.fill(0);
    videoLayer.rect(0,508,width,height-508);
  
    for(int i = 0; i < selectedToggles.size(); i++){
      videoLayer.fill(30);
      videoLayer.rect(width/2-100, 450+(30*i), 200,30);
      videoLayer.fill(255);
      videoLayer.text(selectedToggles.get(i), width/2-80, 470+(30*i));
    }
  videoLayer.endDraw();
  
  if(recordingOn){
    veCanvas.beginDraw();
    veCanvas.image(videoLayer, 0,0);
    veCanvas.endDraw();     
    
    if ((millis() > startTime)&&(millis() < startTime+countdownTime)){
      videoCounter = floor((millis() - startTime)/1000);
      println(videoCounter);
      renderCounter(progressBarCanvas, videoCounter);      
    } else {
      renderProgressBar(progressBarCanvas);
      ve.saveFrame();
    }

    scene.image(videoLayer,0,0);
    scene.image(progressBarCanvas,0,0);
    
    if (millis() > startTime+captureTime+countdownTime){
      endRecording();
    } 
  } else {
    scene.image(videoLayer,0,0);
  }
  scene.endDraw();
}


void renderProgressBar(PGraphics barCanvas){
  barCanvas.beginDraw();
  barCanvas.fill(255,0,0);
  barCanvas.rect(width/2, height-150,200,20);
  barCanvas.fill(255);
  barCanvas.text("Recording...", width/2, height-150);
  
  barCanvas.fill(255,255,255);
  barCanvas.rect(0,height-20,width, 20);
  
  //progress
  float b = (millis() - startTime - countdownTime)/5;
  float barWidth = lerp(0,width,b/1000);
  //println(b);
  barCanvas.fill(255,0,0);
  barCanvas.rect(0,height-20,barWidth,20);   
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
  
  b7 = new GButton(this, width/2-50,height-100, 100, 40);
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
  
  //b7.hide();
  b7.setVisible(false);
}

void endRecording(){
  recordingOn = false;
  ve.dispose();
  
  println("Video created. Loading video in...");
  userVideo = new Movie(this, "gallery/"+userID + ".mp4");
  userVideo.loop();
  
  println("Video ready.");
  //b8a.show();
  //b8b.show();
  b8a.setVisible(true);
  b8b.setVisible(true);
  currentScene = 8;
}
