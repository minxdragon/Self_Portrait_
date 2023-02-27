//Generating hold screen

void sceneFive(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.textAlign(CENTER);
  scene.textSize(20);
  scene.textFont(mono);
  scene.text("GENERATING A PORTRAIT", w/2, h/2-20);
  scene.text("TO MATCH YOUR KEYWORDS", w/2, h/2);
  scene.text("...", w/2, h/2+20);
  scene.endDraw();
  
  if (millis() > sceneTimer+timeoutMillis){
    timeout("5");
  }
}

void defineGUIFive(){
}
