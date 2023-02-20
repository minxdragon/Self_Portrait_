//Start screen
boolean togState1 = false;
boolean togState2 = false;


void sceneZero(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);
  for (Portrait p : portraits){
    p.move();
    p.resetCycle();
    p.display(scene);
  }
  scene.endDraw();
}

void defineGUIZero(){
  b0 = new GButton(this, w/2-125, h/2, 250, 60);
  b0.setText("TOUCH TO BEGIN");
  b0.addEventHandler(this, "sceneZeroButton");
  b0.setIcon("data/icons/emoji-wave.png", 1);
  b0.setIconPos(GAlign.WEST);
  b0.setTextAlign(GAlign.LEFT, GAlign.MIDDLE);
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
  
  client1 = new SyphonClient(this, "syphoncam");
  
  b1.setVisible(true);
  currentScene = 1;
}

class Portrait {
  PVector location;
  PVector velocity;
  PImage imageFile;
  float initialLocationX;
  
  Portrait(int index){
     initialLocationX = (index%5)*265;
     location = new PVector(initialLocationX, ceil(index/5)*265);
     velocity = new PVector(random(1,3),0);
     imageFile = loadImage("portraits/mask-" + index +".png");
  }
  
  void move(){
    location.x = location.x - velocity.x;
  }
  
  void resetCycle(){
    if (location.x < -265){
      location.x = width+530;
      velocity.x = random(1,3);
    }
  }
  
  void display(PGraphics s){
    s.image(imageFile, location.x,location.y);
  }
}
