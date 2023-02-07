//Would you like to display?
boolean userSavedVideo = false;

void sceneNine(PGraphics scene){  
  scene.beginDraw();
  scene.textAlign(CENTER);
  scene.textSize(24);
  if (userVideo.available()) {
    userVideo.read();
  }
  scene.image(userVideo, 0,0,w,h); 
  
  scene.text("Would you like to display this on the gallery wall?",w/2-200,height/2+100,400,800);
  scene.endDraw();
}

void defineGUINine(){
  b9a = new GButton(this, w/2-120,h-300, 100, 40);
  b9a.setText("Yes");
  b9a.addEventHandler(this, "sceneNineAButton");
  b9a.setVisible(false);
  
  b9b = new GButton(this, w/2+10,h-300, 100, 40);
  b9b.setText("No thanks");
  b9b.addEventHandler(this, "sceneNineBButton");
  b9b.setVisible(false);
}

public void sceneNineAButton(GButton source, GEvent event) {
  println("a button event from sceneNineAButton: "+event);
  userSavedVideo = true;
  b9a.setVisible(false);
  b9b.setVisible(false);
  b10.setVisible(true);
  
  currentScene = 10;
  createNewVideoExport();
}

public void sceneNineBButton(GButton source, GEvent event) {
  println("a button event from sceneNineBButton: "+event);
  userSavedVideo = false;
  //Delete movie
  File getFile = dataFile(dataPath("gallery/"+ userID + ".mp4"));
  if(getFile.isFile()){
    getFile.delete();
    println("File deleted.");
  }
  
  b9a.setVisible(false);
  b9b.setVisible(false);
  b10.setVisible(true);
  
  currentScene = 10;
  createNewVideoExport();
}
