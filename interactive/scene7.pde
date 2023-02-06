//Connecting hold screen

void sceneSeven(PGraphics scene){  
  if ((millis() > delayTimer)&&(millis() < delayTimer+delaySyphonConnect)){
    scene.beginDraw();
    scene.background(0,0,0);  
    scene.textAlign(CENTER);
    scene.textSize(40);
    scene.text("Connecting...", w/2, h/2);
    scene.endDraw();
  } else {
    syphonServerReady();
    println("Delay timer complete. Connected.");
  }
}
