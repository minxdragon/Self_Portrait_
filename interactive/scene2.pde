//Analysing hold screen

void sceneTwo(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.textAlign(CENTER);
  scene.textSize(20);
  scene.textFont(mono);
  scene.text("JUST A MOMENT", w/2, h/2-20);
  scene.text("ANALYSING YOUR FACE", w/2, h/2);
  scene.text("...", w/2, h/2+20);
  scene.endDraw();

  if (millis() > sceneTimer+timeoutMillis){
    timeout("2");
  }
}

void defineGUITwo(){
}
