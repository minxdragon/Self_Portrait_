//Would you like to display?
boolean userSavedVideo = false;

void sceneEight(PGraphics scene){  
  scene.beginDraw();
  scene.textAlign(CENTER);
  scene.textSize(24);
  if (userVideo.available()) {
    userVideo.read();
  }
  scene.image(userVideo, 0,0,width,height); 
  
  scene.text("Would you like to display this on the gallery wall?",width/2-200,height/2+300,400,800);
  scene.endDraw();
}

void defineGUIEight(){
  //b8a = sceneGUI.addButton("sceneEightAButton")
  //              .setLabel("Yes")
  //              .setPosition(width/2-120,height-100)
  //              .setSize(100,40)
  //              .setColorLabel(color(0, 0, 0))
  //              .setColorBackground(color(255, 255, 255));
                
  //b8b = sceneGUI.addButton("sceneEightBButton")
  //              .setLabel("No thanks")
  //              .setPosition(width/2+10,height-100)
  //              .setSize(100,40)
  //              .setColorLabel(color(0, 0, 0))
  //              .setColorBackground(color(255, 255, 255));
  //b8a.hide();
  //b8b.hide();
  
  b8a = new GButton(this, width/2-120,height-100, 100, 40);
  b8a.setText("Yes");
  b8a.addEventHandler(this, "sceneEightAButton");
  b8a.setVisible(false);
  
  b8b = new GButton(this, width/2+10,height-100, 100, 40);
  b8b.setText("No thanks");
  b8b.addEventHandler(this, "sceneEightBButton");
  b8b.setVisible(false);
}

public void sceneEightAButton(GButton source, GEvent event) {
  println("a button event from sceneEightAButton: "+event);
  userSavedVideo = true;
  //b8a.hide();
  //b8b.hide();
  b8a.setVisible(false);
  b8b.setVisible(false);
  //b9.show();
  b9.setVisible(true);
  
  currentScene = 9;
}

public void sceneEightBButton(GButton source, GEvent event) {
  println("a button event from sceneEightBButton: "+event);
  userSavedVideo = false;
  //Delete movie
  File getFile = dataFile(dataPath("gallery/"+ userID + ".mp4"));
  if(getFile.isFile()){
    getFile.delete();
    println("File deleted.");
  }
  
  //b8a.hide();
  //b8b.hide();
  b8a.setVisible(false);
  b8b.setVisible(false);
  //b9.show();
  b9.setVisible(true);
  
  currentScene = 9;
}
