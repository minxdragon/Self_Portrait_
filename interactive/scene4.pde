//Select keywords
String[] allKeywords = {"creative", "visionary", "calm", "tortured", "weird", "provocative", "passionate", "analytical", "level-headed", "angry",
                        "adventurous", "bizarre", "risk-taker", "assertive", "zealous", "musical", "vacant", "enchanting", "lonely", "expressive",
                        "dilligent", "energetic", "contemplative", "serene", "chaotic", "calculating", "elegant", "reserved", "happy", "independant",
                        "brooding", "sensual", "surreal", "mad"};

LinkedHashMap<String,Boolean> allKeywordsHashMap = new LinkedHashMap<String,Boolean>();
ArrayList<GButton> wordToggles = new ArrayList<GButton>();
StringList selectedToggles;

void sceneFourSetup(){  
  for(int i = 0; i < allKeywords.length; i++){  
    allKeywordsHashMap.put(allKeywords[i],false);
  }
}

void sceneFour(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);
  scene.endDraw();
}

void defineGUIFour(){
  int increment = 0;

  for(int i = 0; i < allKeywords.length-1; i+=3){   
    //wordToggles.add(sceneGUI.addToggle(allKeywords[i]).setPosition(50, 50+(30*increment)+30).setSize(200,10).setValue(false).setColorBackground(color(255, 255, 255)));
    //wordToggles.add(sceneGUI.addToggle(allKeywords[i+1]).setPosition(260, 50+(30*increment)+30).setSize(200,10).setValue(false).setColorBackground(color(255, 255, 255)));
    wordToggles.add(new GButton(this, 60, 50+(30*increment), 150, 50, allKeywords[i]));
    wordToggles.add(new GButton(this, 230, 50+(30*increment), 150, 50, allKeywords[i+1]));
    wordToggles.add(new GButton(this, 400, 50+(30*increment), 150, 50, allKeywords[i+2]));
    wordToggles.get(i).setVisible(false);
    wordToggles.get(i).addEventHandler(this,"wordToggleEvent");
    
    wordToggles.get(i+1).setVisible(false);
    wordToggles.get(i+1).addEventHandler(this, "wordToggleEvent");

    wordToggles.get(i+2).setVisible(false);
    wordToggles.get(i+2).addEventHandler(this, "wordToggleEvent");    
    
    increment+=2;
  }
  
  //for(int i = 0; i < allKeywords.length-1; i+=2){    
  //  scenes[4].fill(30);    
  //  //wordToggle[i] = sceneGUI.addToggle("toggle-" + allKeywords[i]).setPosition(50, 50+(30*increment+10)).setSize(200,30).setValue(false);
  //  //sceneGUI.addToggle("toggle-" + allKeywords[i+1]).setPosition(260, 50+(30*increment+10)).setSize(200,30).setValue(false);
    
  //  //scenes[4].fill(255);    
  //  //scenes[4].text(allKeywords[i], 70, 70+(30*increment+2));
  //  //scenes[4].text(allKeywords[i+1], 280, 70+(30*increment+2));
    
  //  increment++;
  //}  
  
  //b4a = sceneGUI.addButton("sceneFourAButton")
  //             .setLabel("Generate")
  //             .setPosition(width/2-50,height-100)
  //             .setSize(100,40)
  //             .setColorLabel(color(0, 0, 0))
  //             .setColorBackground(color(255, 255, 255));
  
  //b4b = sceneGUI.addButton("sceneFourBButton")
  //             .setLabel("Clear all")
  //             .setPosition(width/2-50,height-200)
  //             .setSize(100,40)
  //             .setColorLabel(color(0, 0, 0))
  //             .setColorBackground(color(255, 255, 255));
               
  //b4a.hide();
  //b4b.hide();
  
  
  b4a = new GButton(this, width/2-50,height-200, 120, 50);
  b4a.setText("Generate");
  b4a.addEventHandler(this, "sceneFourAButton");
  b4a.setVisible(false);
  
  b4b = new GButton(this, width/2-50,height-270, 120, 50);
  b4b.setText("Clear all");
  b4b.addEventHandler(this, "sceneFourBButton");
  b4b.setVisible(false);
}

public void sceneFourAButton(GButton source, GEvent event) {
  println("a button event from sceneFourAButton: "+event);
  selectedToggles = new StringList();
  
  for(int i = 0; i < allKeywords.length; i++){  
    boolean toggleValue = allKeywordsHashMap.get(allKeywords[i]);
    if (toggleValue){
      selectedToggles.append(allKeywords[i]);
    }
  }  
  
  String[] toggledKeywords = selectedToggles.array();
  String userSelectedKeywords = join(toggledKeywords, "&"); 
  
  String clientMessageString = "userSelected," + userSelectedKeywords;
  
  myClient.write(clientMessageString);
  println("Message sent to server: " + clientMessageString);
  
  for(int i = 0; i < wordToggles.size(); i++){  
    wordToggles.get(i).setVisible(false);
  }
  
  //b4a.hide();
  //b4b.hide();
  b4a.setVisible(false);
  b4b.setVisible(false);
  currentScene = 5;
}

public void sceneFourBButton(GButton source, GEvent event) {
  for(int i = 0; i < wordToggles.size(); i++){  
    allKeywordsHashMap.put(allKeywords[i],false);
    wordToggles.get(i).setLocalColorScheme(6);
  }
}


public void wordToggleEvent(GButton source, GEvent event) {
  println("a button event from wordToggleEvent: " + event);  
  if ((event == GEvent.CLICKED) && (source.getLocalColorScheme() == 6)){
    source.setLocalColorScheme(1);
    println(event, source.getText());
    allKeywordsHashMap.put(source.getText(),true);
    println(allKeywordsHashMap);
  } else if ((event == GEvent.CLICKED) && (source.getLocalColorScheme() == 1)){
    source.setLocalColorScheme(6);
    println(event, source.getText());
    allKeywordsHashMap.put(source.getText(),false);
    println(allKeywordsHashMap);
  }
}
