//Connecting hold screen

void sceneSeven(PGraphics scene){  
  if ((millis() > delayTimer)&&(millis() < delayTimer+delaySyphonConnect)){
    scene.beginDraw();
    scene.background(0,0,0);  
    scene.textAlign(CENTER);
    scene.textSize(20);
    scene.textFont(mono);
    scene.text("GET READY TO RECORD", w/2, h/2-20);
    scene.text("YOUR 5 SECOND PORTRAIT", w/2, h/2);
    scene.text("...", w/2, h/2+20);
    scene.endDraw();
    
    if (millis() > sceneTimer+timeoutMillis){
      timeout("7");
    }
  } else {
    syphonServerReady();
    println("Delay timer complete. Connected.");
  }
}
