//Results screen
PImage maskImageB;

int delaySyphonConnect = 3000;
int delayTimer;
ArrayList<Keyword> keywords = new ArrayList<Keyword>();

void sceneSix(PGraphics scene){  
  maskImageB = loadImage("data/dream.jpg");
  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.image(maskImageB,w/2-219, 136,438,438);
  scene.textAlign(CENTER);
  scene.textSize(20);
  scene.textFont(mono);
  scene.text("YOUR GENERATED PORTRAIT",w/2,620);
  scene.text("OF A PERSON WHO IS:",w/2,620+24);
    
  for(int i = 0; i < selectedToggles.size(); i++){
    String keyword = selectedToggles.get(i);
    scene.text(keyword.toUpperCase(), w/2, 668+(24*i));
  }
  
  scene.endDraw();
  
  if (millis() > sceneTimer+timeoutMillis){
    timeout("6");
  }
}

void defineGUISix(){
  b6 = new GButton(this, width/2-210, h-90, 420, 60);
  b6.setText("RECORD YOUR 5 SECOND PORTRAIT");
  b6.addEventHandler(this, "sceneSixButton");
  b6.setIcon("data/icons/emoji-video.png", 1);
  b6.setIconPos(GAlign.WEST);
  b6.setTextAlign(GAlign.LEFT, GAlign.MIDDLE);    
  b6.setVisible(false);
}

//send server message that video is ready
void syphonServerReady(){
  client2 = new SyphonClient(this, syphonClient2Name);
  println("Syphon Client 2 connected to: " + client2.getServerName());
  
  for (int i = 0; i < selectedToggles.size(); i++){
    String keyword = selectedToggles.get(i);
    keywords.add(new Keyword(keyword, i));
  }
  
  exitButton.setVisible(false);
  currentScene = 8;
  
  recordingOn = true;
  ve.setMovieFileName("data/galleryPlayer/"+ userID + ".mp4");
  ve.startMovie();
  println("Starting to record...");
  startTime = millis();
}

public void sceneSixButton(GButton source, GEvent event) {
  println("a button event from sceneSixButton: " + event);  
  
  myClient.write("connectSyphonServer");    
  //timer 3 seconds
  delayTimer = millis();
  createNewVideoExport();
  b6.setVisible(false);
  startTime = millis();
  currentScene = 7;
}
