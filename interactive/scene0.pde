//Start screen
boolean togState1 = false;
boolean togState2 = false;

void sceneZero(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);
  scene.endDraw();
}

void defineGUIZero(){
  //.setImages(loadImage("Arrow-Left.png"), loadImage("Arrow-Right.png"), loadImage("Refresh.png"))
  //b0 = sceneGUI
  //     .addButton("sceneZeroButton")
  //     .setLabel("Start")
  //     .setPosition(width/2-50,height/2-20)
  //     .setSize(100,40)
  //     .setColorLabel(color(0, 0, 0))
  //     .setColorBackground(color(255, 255, 255))
  //     ;
  
  b0 = new GButton(this, width/2-50,height/2-20, 100, 40);
  b0.setText("Start");
  b0.addEventHandler(this, "sceneZeroButton");
  b0.setVisible(true);
}

public void sceneZeroButton(GButton source, GEvent event) {
  println("a button event from sceneZeroButton: "+event);
  userID = month()+"-"+day()+"-"+hour()+"-"+minute()+"-"+second();

  countdownStartTime = 0;
  countdownCurrentTime = 0;
    
  b0.setVisible(false);  
  myClient.write("cameraNoMask");

  for(int i = 0; i < wordToggles.size(); i++){  
    allKeywordsHashMap.put(allKeywords[i], false);
  }
  
  returnedKeywords = new String[0];
  
  b1.setVisible(true);
  currentScene = 1;
}
