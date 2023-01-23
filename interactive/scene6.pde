//Results screen
PImage maskImageB;

void sceneSix(PGraphics scene){  
  maskImageB = loadImage("data/dream.jpg");
  
  scene.beginDraw();
  scene.background(0,0,0);  
  scene.image(maskImageB,w/2-150, 100,300,300);

  for(int i = 0; i < selectedToggles.size(); i++){
    scene.fill(30);
    scene.rect(w/2-100, 450+(30*i), 200,30);
    scene.fill(255);
    scene.text(selectedToggles.get(i), w/2-80, 470+(30*i));
  }

  scene.endDraw();
}


void defineGUISix(){
  //b6 = sceneGUI.addButton("sceneSixButton")
  //             .setLabel("Next")
  //             .setPosition(width/2-50,height-200)
  //             .setSize(100,40)
  //             .setColorLabel(color(0, 0, 0))
  //             .setColorBackground(color(255, 255, 255));
  //b6.hide();
  
  b6 = new GButton(this, w/2-50,h-400, 100, 40);
  b6.setText("Next");
  b6.addEventHandler(this, "sceneSixButton");
  b6.setVisible(false);
}

public void sceneSixButton(GButton source, GEvent event) {
  println("a button event from sceneSixButton: " + event);
  //b6.hide(); 
  b6.setVisible(false);
  //b7.show();
  b7.setVisible(true);
  currentScene = 7;
}
