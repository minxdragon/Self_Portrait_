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
    image(canvasSyphoner, -400, 0, 1372, 1030);
  }

  videoLayer.beginDraw();
    videoLayer.image(canvasSyphoner, -400, 0, 1372, 1030); 
    videoLayer.rectMode(CENTER);
    videoLayer.textAlign(CENTER);
    videoLayer.textSize(16);
    videoLayer.textFont(mono);
    videoLayer.fill(255);
    for (Keyword words : keywords){
      words.move();
      words.bounce();
      words.display(videoLayer);
    } 
  videoLayer.endDraw();
  
  if(recordingOn){
    veCanvas.beginDraw();
    veCanvas.image(videoLayer, 0,0);
    veCanvas.endDraw();     
    
    if ((millis() > startTime)&&(millis() < startTime+countdownTime)){
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
  barCanvas.clear();
  barCanvas.noStroke();
    
  //progress
  float b = (millis() - startTime - countdownTime)/5;
  float barWidth = lerp(0,w,b/1000);
  barCanvas.fill(0);
  barCanvas.rect(0,0,width,40);  
  
  barCanvas.fill(255,0,0);
  barCanvas.rect(0,0,barWidth,40);  

  barCanvas.textAlign(CENTER);
  barCanvas.textSize(16);
  barCanvas.textFont(mono);
  barCanvas.fill(255);
  barCanvas.text("NOW RECORDING", w/2, 24);
  
  barCanvas.endDraw();
}

void restartProgressBar(PGraphics barCanvas){
  barCanvas.beginDraw();
  barCanvas.clear();
  barCanvas.endDraw();
}

void endRecording(){
  recordingOn = false;
  ve.dispose();
  
  println("Video created. Loading video in...");
  client2.stop();
  println("Syphon Client 2 disconnected"); 
  
  userVideo = new Movie(this, "galleryPlayer/"+userID + ".mp4");
  userVideo.loop();
  keywords.clear();
  println("Video ready.");
  b9a.setVisible(true);
  b9b.setVisible(true);
  sceneTimer = millis();
  currentScene = 9;
}

class Keyword {
  PVector size; 
  PVector location;
  PVector velocity;
  String wordLabel;
  
  Keyword(String label, int index){
     size = new PVector(170,50);
     if (index < 4){
       location = new PVector(random(size.x, width-size.x), height-150-(70*index));
     } else {
       location = new PVector(random(size.x, width-size.x), 50+(70*(index-3)));
     }
     velocity = new PVector(random(2),0);
     wordLabel = label;
  }
   
  void move(){
    location.x = location.x + velocity.x;
     //location = location.add(velocity);
  }

  void bounce(){
    if ((location.x > width-(size.x/2)) || (location.x < (size.x/2))){
      velocity.x = velocity.x * -1;
    }
    //if ((location.y > height-(size.y/2)) || (location.y < (size.y/2))){
    //  velocity.y = velocity.y * -1;
    //}
  }   
   
  void display(PGraphics scene){
     scene.rectMode(CENTER);
     scene.textAlign(CENTER);
     scene.textSize(16);
     scene.textFont(mono);
     scene.noFill();
     scene.stroke(255);
     scene.rect(location.x, location.y, size.x, size.y, 10);
     scene.text(wordLabel.toUpperCase(), location.x, location.y+4);
  }
}
