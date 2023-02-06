//Thank you screen

void sceneTen(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.textAlign(CENTER);  
  scene.textSize(40);
  if (userSavedVideo){
    scene.text("Your video has been added to the gallery. Go around to see it in the gallery in x minutes.",width/2-200,height/2-100,400,800);
  } else {
    scene.text("Your video has been deleted.",w/2-200,h/2-100,400,800);
  }

  scene.endDraw();
}

void defineGUITen(){
  b10 = new GButton(this, w/2-40,h-300, 100, 40);
  b10.setText("End");
  b10.addEventHandler(this, "sceneTenButton");
  b10.setVisible(false);
}

public void sceneTenButton(GButton source, GEvent event) {
  println("a button event from sceneTenButton: "+ event);
  b10.setVisible(false);
  b0.setVisible(true);
  currentScene = 0;
}
