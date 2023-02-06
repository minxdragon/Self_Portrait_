//Select keywords
String[] allKeywords = {"Nurturing", "Creative", "Rational", "Sensitive", "Determined", 
                        "Introspective", "Caring", "Perceptive", "Intuitive", "Emotional",
                        "Moody", "Intelligent", "Passionate", "Playful", "Shy", "Imaginative", 
                        "Decisive", "Strong", "Practical", "Intimidating", "Condescending", 
                        "Provocative", "Impulsive", "Inventive", "Conceptual", "Persistent", 
                        "Protective", "Reserved", "Happy", "Independant", "Brooding", "Surreal", 
                        "Mad"};
                        
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
  
  b4a = new GButton(this, w/2-50,h-200, 120, 50);
  b4a.setText("Generate");
  b4a.addEventHandler(this, "sceneFourAButton");
  b4a.setVisible(false);
  
  b4b = new GButton(this, w/2-50,h-270, 120, 50);
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
  
  String[] toggledKeywords = selectedToggles.toArray(new String[0]);
  String userSelectedKeywords = join(toggledKeywords, "&"); 
  
  String clientMessageString = "userSelected," + userSelectedKeywords;

  //connectAllClients();
  myClient.write(clientMessageString);
  println("Message sent to server: " + clientMessageString);
  
  for(int i = 0; i < wordToggles.size(); i++){  
    wordToggles.get(i).setVisible(false);
  }
  
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
    //println(allKeywordsHashMap);
  } else if ((event == GEvent.CLICKED) && (source.getLocalColorScheme() == 1)){
    source.setLocalColorScheme(6);
    println(event, source.getText());
    allKeywordsHashMap.put(source.getText(),false);
    //println(allKeywordsHashMap);
  }
}
