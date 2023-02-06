//Results screen
PImage maskImageB;

int delaySyphonConnect = 3000;
int delayTimer;

void sceneSix(PGraphics scene){  
  maskImageB = loadImage("data/dream.jpg");
  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.image(maskImageB,w/2-150, 100,300,300);

  for(int i = 0; i < selectedToggles.size(); i++){
    scene.fill(30);
    scene.rect(w/2-100, 450+(30*i), 200,30);
    scene.fill(255);
    scene.text(selectedToggles.get(i), w/2-80, 470+(30*i));
  }

  scene.endDraw();
}

void defineGUISix(){
  b6 = new GButton(this, w/2-50,h-400, 100, 40);
  b6.setText("Record video");
  b6.addEventHandler(this, "sceneSixButton");
  b6.setVisible(false);
}

//send server message that video is ready
void syphonServerReady(){
  client2 = new SyphonClient(this, syphonClient2Name);
  println("Syphon Client 2 connected to: " + client2.getServerName());
  currentScene = 8;

  recordingOn = true;
  ve.setMovieFileName("data/gallery/"+ userID + ".mp4");
  ve.startMovie();
  println("Starting to record...");
  startTime = millis();
}

public void sceneSixButton(GButton source, GEvent event) {
  println("a button event from sceneSixButton: " + event);  
  
  myClient.write("connectSyphonServer");    
  //timer 3 seconds
  delayTimer = millis();
  b6.setVisible(false);
  currentScene = 7;
}
