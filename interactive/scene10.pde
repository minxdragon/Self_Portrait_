//Thank you screen

void sceneTen(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.textAlign(CENTER);
  scene.textSize(20);
  scene.textFont(mono); 
  if (userSavedVideo){
    scene.text("YOUR VIDEO HAS BEEN ADDED",w/2,h/2-24);
    scene.text("TO THE GALLERY WALL",w/2,h/2);
    scene.text("THANK YOU",w/2,h/2+48);
  } else {
    scene.text("YOUR VIDEO HAS BEEN DELETED",w/2,h/2-24);
    scene.text("THANK YOU",w/2,h/2+24);
  }

  scene.endDraw();

  //5 minute timeout
  if (millis() > sceneTimer+timeoutMillis){
    timeout("10");
  }
}

void defineGUITen(){
  b10 = new GButton(this, w/2-62, 810, 124, 60);
  b10.setText("END");
  b10.addEventHandler(this, "sceneTenButton");
  b10.setVisible(false);
}

public void sceneTenButton(GButton source, GEvent event) {
  println("a button event from sceneTenButton: "+ event);
  b10.setVisible(false);
  b0.setVisible(true);
  currentScene = 0;
}
