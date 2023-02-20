// Face photo screen
Rectangle[] faces;
int countdownStartTime = 0;
int countdownDurationTime = 3;
boolean countdownOn = false;
int countdownCurrentTime = 0;

void sceneOne(PGraphics scene){  
  scene.beginDraw(); 
  if (client1.newFrame()) {
    canvasWebcam = client1.getGraphics(canvasWebcam);
    scene.image(canvasWebcam, -400, 0, 1372, 1030);
  }   
  userPhoto = scene.get(0,0,width, height);  
  
  //scene.fill(0);
  //scene.rect(0, 580,w,h-580);
  if (countdownOn){
    //3,2,1
    countdownCurrentTime = floor((millis() - countdownStartTime)/1000);
    renderCounter(scene, countdownCurrentTime);
  }
  scene.endDraw();

  if (countdownCurrentTime > countdownDurationTime){
    countdownOn = false;
    takeUserPhoto();
    currentScene = 2;
  }
}

void defineGUIOne(){
  b1 = new GButton(this, w/2-100, h/2, 200, 60);
  b1.setText("TAKE PHOTO");
  b1.addEventHandler(this, "sceneOneButton");
  b1.setIcon("data/icons/emoji-cam.png", 1);
  b1.setIconPos(GAlign.WEST);
  b1.setTextAlign(GAlign.LEFT, GAlign.MIDDLE);
  b1.setVisible(false);
}


void renderCounter(PGraphics currentScene, int counter){  
  currentScene.beginDraw();
  currentScene.textAlign(CENTER);
  currentScene.textSize(20);
  currentScene.textFont(mono);
  currentScene.ellipseMode(CENTER);
  currentScene.noStroke();
  
  currentScene.fill(255);
  currentScene.text("LOOK UP AT CAM", w/2, 50);
  currentScene.image(pointEmoji, w/2-130, 16, 48, 48);
  currentScene.image(pointEmoji, w/2+82, 16, 48, 48);
  
  currentScene.fill(0);
  currentScene.ellipse(w/2-62-10,101,62,62);
  currentScene.fill(255);
  currentScene.text("3", w/2-62-10-31,101-14,62,62);

  currentScene.fill(0);
  currentScene.ellipse(w/2,101,62,62);
  currentScene.fill(255);
  currentScene.text("2", w/2-31,101-14,62,62);
  
  currentScene.fill(0);
  currentScene.ellipse(w/2+62+10,101,62,62);
  currentScene.fill(255);
  currentScene.text("1", w/2+62+10-31,101-14,62,62);

  switch(counter){
    case 0:
      currentScene.fill(255);
      currentScene.ellipse(w/2-62-10,101,62,62);
      currentScene.fill(0);
      currentScene.text("3", w/2-62-10-31,101-14,62,62);
      break;
    case 1:
      currentScene.fill(255);
      currentScene.ellipse(w/2,101,62,62);
      currentScene.fill(0);
      currentScene.text("2", w/2-31,101-14,62,62);
      break;
    case 2:
      currentScene.fill(255);
      currentScene.ellipse(w/2+62+10,101,62,62);
      currentScene.fill(0);
      currentScene.text("1", w/2+62+10-31,101-14,62,62);
      break;
  } 
  
  currentScene.endDraw();
}

public void sceneOneButton(GButton source, GEvent event) {
  println("a button event from sceneOneButton: "+ event);
  b1.setVisible(false);
  countdownStartTime = millis();
  countdownOn = true; 
}

void takeUserPhoto(){
  userImage.beginDraw();
  userImage.image(userPhoto,0,0);
  userImage.save("data/user.jpg");
  println("Webcam image saved.");
  userImage.endDraw();
  
  processImage();
  myClient.write("faceCaptured");
  client1.stop();
}

void processImage(){
  opencv = new OpenCV(this, "user.jpg");
  opencv.loadCascade(OpenCV.CASCADE_FRONTALFACE);    
  faces = opencv.detect();
  println("Faces found: " + faces.length);
  
  if (faces.length >= 1){    
    userImage.beginDraw();
    userImage.loadPixels();
    userImage.image(opencv.getInput(),0,0);
    userImage.endDraw(); 
    
    PImage faceCrop = get(faces[0].x-40, faces[0].y-40, faces[0].width+80, faces[0].height+80);
    PGraphics faceImageCanvas = createGraphics(400,400);  
    faceImageCanvas.beginDraw();
    faceImageCanvas.image(faceCrop,0,0,400,400);
    faceImageCanvas.save("data/face.jpg");
    println("Face crop successful.");
    faceImageCanvas.endDraw(); 
  } else {
    PGraphics defaultImageCanvas = createGraphics(400,400);
    defaultImageCanvas.beginDraw();
    defaultImageCanvas.image(faceDefault,0,0,400,400);
    defaultImageCanvas.save("data/face.jpg");
    println("Face not found. Saved default.");
    defaultImageCanvas.endDraw(); 
  }  
}
