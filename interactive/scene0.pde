//Start screen
boolean togState1 = false;
boolean togState2 = false;

void sceneZero(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);
  scene.endDraw();
}

void defineGUIZero(){
  b0 = new GButton(this, w/2-50, h/2-20, 100, 40);
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
  allKeywordsHashMap = new LinkedHashMap<String,Boolean>();
  
  for(int i = 0; i < wordToggles.size(); i++){  
    allKeywordsHashMap.put(allKeywords[i], false);
  }
  
  returnedKeywords = new String[0];
  
  b1.setVisible(true);
  currentScene = 1;
}
