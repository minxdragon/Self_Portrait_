//Thank you screen

void sceneNine(PGraphics scene){  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.textAlign(CENTER);  
  scene.textSize(40);
  if (userSavedVideo){
    scene.text("Your video has been added to the gallery. Go around to see it in the gallery in x minutes.",width/2-200,height/2-200,400,800);
  } else {
    scene.text("Your video has been deleted.",width/2-200,height/2-200,400,800);
  }

  scene.endDraw();
}

void defineGUINine(){
  //b9 = sceneGUI.addButton("sceneNineButton")
  //             .setLabel("End")
  //             .setPosition(width/2-40,height-100)
  //             .setSize(100,40)
  //             .setColorLabel(color(0, 0, 0))
  //             .setColorBackground(color(255, 255, 255));
  //b9.hide();
  
  b9 = new GButton(this, width/2-40,height-100, 100, 40);
  b9.setText("End");
  b9.addEventHandler(this, "sceneNineButton");
  b9.setVisible(false);
}

public void sceneNineButton(GButton source, GEvent event) {
  println("a button event from sceneNineButton: "+ event);
  //b9.hide();
  b9.setVisible(false);
  //b0.show();
  b0.setVisible(true);
  currentScene = 0;
}
