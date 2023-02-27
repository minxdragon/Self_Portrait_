//Would you like to display?
boolean userSavedVideo = false;

void sceneNine(PGraphics scene){  
  if (userVideo.available()) {
    userVideo.read();
  }
  
  scene.beginDraw();
  scene.background(0);
  scene.textAlign(CENTER);
  scene.textSize(24);
  scene.image(userVideo, 0,0,w,h); 
  scene.fill(0);
  scene.rect(w/2-124-10-48,678,364,240);
  scene.textAlign(CENTER);
  scene.textSize(20);
  scene.textFont(mono);  
  scene.fill(255);
  scene.text("WOULD YOU LIKE TO ADD",w/2,728);
  scene.text("YOUR VIDEO PORTRAIT",w/2,728+22);
  scene.text("THE GALLERY?",w/2,728+44);
  scene.endDraw();
  
  //5 minute timeout
  if (millis() > sceneTimer+timeoutMillis){
    timeout("9");
  }
}

void defineGUINine(){
  b9a = new GButton(this, w/2-124-10, 810, 124, 60);
  b9a.setText("YES");
  b9a.setIcon("data/icons/emoji-yes.png", 1);
  b9a.addEventHandler(this, "sceneNineAButton");
  b9a.setIconPos(GAlign.WEST);
  b9a.setTextAlign(GAlign.LEFT, GAlign.MIDDLE);   
  b9a.setVisible(false);
  
  b9b = new GButton(this, w/2+10, 810, 124, 60);
  b9b.setText("NO");
  b9b.addEventHandler(this, "sceneNineBButton");
  b9b.setIcon("data/icons/emoji-no.png", 1);
  b9b.setIconPos(GAlign.WEST);
  b9b.setTextAlign(GAlign.LEFT, GAlign.MIDDLE);   
  b9b.setVisible(false);
}

public void sceneNineAButton(GButton source, GEvent event) {
  println("a button event from sceneNineAButton: "+event);
  userSavedVideo = true;
  //Move file
  File getFile = dataFile(dataPath("galleryPlayer/"+ userID + ".mp4"));
  if(getFile.isFile()){
    getFile.renameTo(new File(dataPath("gallery/"+ userID + ".mp4")));
    println("File moved.");
  }
  
  userVideo.stop();
  b9a.setVisible(false);
  b9b.setVisible(false);
  b10.setVisible(true);
  sceneTimer = millis();
  currentScene = 10;
  exitButton.setVisible(false);
}

public void sceneNineBButton(GButton source, GEvent event) {
  println("a button event from sceneNineBButton: "+event);
  userSavedVideo = false;
  //Delete movie
  File getFile = dataFile(dataPath("galleryPlayer/"+ userID + ".mp4"));
  if(getFile.isFile()){
    getFile.delete();
    println("File deleted.");
  }
  
  userVideo.stop();
  b9a.setVisible(false);
  b9b.setVisible(false);
  b10.setVisible(true);
  sceneTimer = millis();
  currentScene = 10;
  exitButton.setVisible(false);
}
