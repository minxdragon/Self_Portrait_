//Analysis complete screen - Image and Keywords
PImage maskImageA;
String[] returnedKeywords;

void sceneThree(PGraphics scene){  
  maskImageA = loadImage("data/dream.jpg");
  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.image(maskImageA,w/2-219, 136,438,438);
  scene.fill(255);
  scene.textAlign(CENTER);
  scene.textSize(20);
  scene.textFont(mono);
  scene.text("YOU HAVE BEEN CATEGORISED AS:",w/2,620);
    
  for(int i = 0; i < returnedKeywords.length; i++){
    String keyword = returnedKeywords[i];
    scene.text(keyword.toUpperCase(), w/2, 644+(24*i));
  }

  scene.endDraw();
  
  if (millis() > sceneTimer+timeoutMillis){
    timeout("3");
  }
}

void updateKeywordToggles(String[] computerSelected){
  for(int i = 0; i < allKeywordsHashMap.size(); i++){
    allKeywordsHashMap.put(allKeywords[i], false);
  }
  
  //update allKeywordsHashMap with computer selected toggles
  for(int i = 0; i < computerSelected.length; i++){
    allKeywordsHashMap.put(computerSelected[i], true);
  } 
}


void defineGUIThree(){
  b3 = new GButton(this, w/2-160, h-90, 320, 60);
  b3.setText("CHOOSE YOUR KEYWORDS");
  b3.addEventHandler(this, "sceneThreeButton");
  b3.setIcon("data/icons/emoji-edit.png", 1);
  b3.setIconPos(GAlign.WEST);
  b3.setTextAlign(GAlign.LEFT, GAlign.MIDDLE);  
  b3.setVisible(false);
}

public void sceneThreeButton(GButton source, GEvent event) {
  println("a button event from sceneThreeButton: "+event);
  updateKeywordToggles(returnedKeywords);
  b3.setVisible(false);
  
  b4a.setVisible(true);
  b4b.setVisible(true);
  
  for(int i = 0; i < wordToggles.size(); i++){  
    wordToggles.get(i).setVisible(true);
    //set the ones that are "true" to the green colour scheme otherwise purple
    if(allKeywordsHashMap.get(allKeywords[i]) == true){
      wordToggles.get(i).setLocalColorScheme(6);
    } else {
      wordToggles.get(i).setLocalColorScheme(1);
    }
  }
  sceneTimer = millis();
  currentScene = 4;
}
