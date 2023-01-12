//Analysis complete screen - Image and Keywords
PImage maskImageA;
String[] returnedKeywords;

void sceneThree(PGraphics scene){  
  maskImageA = loadImage("data/dream.jpg");
  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.image(maskImageA,width/2-150, 100,300,300);

  for(int i = 0; i < returnedKeywords.length; i++){
    scene.fill(30);
    scene.rect(width/2-100, 450+(30*i), 200,30);
    scene.fill(255);
    scene.text(returnedKeywords[i], width/2-80, 470+(30*i));
  }

  scene.endDraw();
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
  //b3 = sceneGUI.addButton("sceneThreeButton")
  //             .setLabel("Next")
  //             .setPosition(width/2-50,height-200)
  //             .setSize(100,40)
  //             .setColorLabel(color(0, 0, 0))
  //             .setColorBackground(color(255, 255, 255));
  //b3.hide();
  
  b3 = new GButton(this, width/2-50,height-200, 100, 40);
  b3.setText("Next");
  b3.addEventHandler(this, "sceneThreeButton");
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
      wordToggles.get(i).setLocalColorScheme(1);
    } else {
      wordToggles.get(i).setLocalColorScheme(6);
    }
  }

  currentScene = 4;
}
