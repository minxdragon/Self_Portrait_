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
int maximumToggles = 7;

void sceneFourSetup(){  
  for(int i = 0; i < allKeywords.length; i++){  
    allKeywordsHashMap.put(allKeywords[i],false);
  }
}

void sceneFour(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);
  scene.textAlign(CENTER);
  scene.textSize(20);
  scene.textFont(mono);
  scene.text("SELECT 1-7 KEYWORDS YOU IDENTIFY WITH", w/2, h-200);
  scene.endDraw();
}

void defineGUIFour(){
  int increment = 0;

  for(int i = 0; i < allKeywords.length-1; i+=3){   
    wordToggles.add(new GButton(this, 30+25, 50+(30*increment), 170, 50, allKeywords[i].toUpperCase())); 
    wordToggles.add(new GButton(this, 210+25, 50+(30*increment), 170, 50, allKeywords[i+1].toUpperCase()));
    wordToggles.add(new GButton(this, 390+25, 50+(30*increment), 170, 50, allKeywords[i+2].toUpperCase()));
    wordToggles.get(i).setVisible(false);
    wordToggles.get(i).addEventHandler(this,"wordToggleEvent");
    
    wordToggles.get(i+1).setVisible(false);
    wordToggles.get(i+1).addEventHandler(this, "wordToggleEvent");

    wordToggles.get(i+2).setVisible(false);
    wordToggles.get(i+2).addEventHandler(this, "wordToggleEvent");    
    
    increment+=2;
  }
  
  b4a = new GButton(this, width-290-30-25, h-90, 290, 60);
  b4a.setText("GENERATE PORTRAIT");
  b4a.addEventHandler(this, "sceneFourAButton");
  b4a.setIcon("data/icons/emoji-paint.png", 1);
  b4a.setIconPos(GAlign.WEST);
  b4a.setTextAlign(GAlign.LEFT, GAlign.MIDDLE);    
  b4a.setVisible(false);
 
  b4b = new GButton(this, 30+25, h-90, 220, 60);
  b4b.setText("CLEAR ALL");
  b4b.addEventHandler(this, "sceneFourBButton");
  b4b.setLocalColorScheme(1);
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
    wordToggles.get(i).setLocalColorScheme(1);
  }
  b4a.setEnabled(false);
  b4a.setLocalColorScheme(7);
}


public void wordToggleEvent(GButton source, GEvent event) {
  println("a button event from wordToggleEvent: " + event);  
  if ((event == GEvent.CLICKED) && (source.getLocalColorScheme() == 1)){
    source.setLocalColorScheme(6);
    println(event, source.getText());
    allKeywordsHashMap.put(capitaliseKeyword(source.getText()),true);
    println("ON: " + capitaliseKeyword(source.getText()));
  } else if ((event == GEvent.CLICKED) && (source.getLocalColorScheme() == 6)){
    source.setLocalColorScheme(1);
    println(event, source.getText());
    allKeywordsHashMap.put(capitaliseKeyword(source.getText()),false);
    println("OFF: " + capitaliseKeyword(source.getText()));
  }
  
  boolean buttonState = checkToggleCount();
  
  if (buttonState){
    b4a.setEnabled(false);
    b4a.setLocalColorScheme(7);
  } else {
    b4a.setEnabled(true);
    b4a.setLocalColorScheme(6);  
  }
}

boolean checkToggleCount(){
  int selectedToggleCount = 0;
  for(int i = 0; i < allKeywordsHashMap.size(); i++){  
    if (allKeywordsHashMap.get(allKeywords[i])){
      selectedToggleCount++;
    }
  }
    
  return ((selectedToggleCount > maximumToggles)||(selectedToggleCount < 1));
}

String capitaliseKeyword(String uppercaseString){  
  return str(uppercaseString.charAt(0)) + uppercaseString.substring(1, uppercaseString.length()).toLowerCase();
}
