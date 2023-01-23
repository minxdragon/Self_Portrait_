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
    scene.image(canvasWebcam, 0, 0, 640, 508);
  }   
  
  //if (client.newFrame()) {
  //  sCanvas = client.getGraphics(sCanvas);
    
  //  //photobooth image 1232 x 688px
  //  scene.image(sCanvas, 0, 0, 640, 508);    
  //  //userImage = createGraphics(608, 1080);
  //  //userPhoto = createImage(608, 1080,RGB);
  //}  
  ////println(scene.width, scene.height);
  userPhoto = scene.get(0,0,640, 508);  
  
  scene.fill(0);
  scene.rect(0, 508,w,h-508);
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
  //b1 = sceneGUI.addButton("sceneOneButton")
  //             .setLabel("Take Photo")
  //             .setPosition(width/2-50,height-200)
  //             .setSize(100,40)
  //             .setColorLabel(color(0, 0, 0))
  //             .setColorBackground(color(255, 255, 255));
  //b1.hide();
  b1 = new GButton(this, w/2-50,h/2-20, 100, 40);
  b1.setText("Take Photo");
  b1.addEventHandler(this, "sceneOneButton");
  b1.setVisible(false);
}


void renderCounter(PGraphics currentScene, int counter){  
  currentScene.beginDraw();
  currentScene.fill(0);
  currentScene.ellipse(w/2-50,h-150,30,30);
  currentScene.fill(255);
  currentScene.text("3", w/2-55,h-160,30,30);

  currentScene.fill(0);
  currentScene.ellipse(w/2,h-150,30,30);
  currentScene.fill(255);
  currentScene.text("2", w/2-5,h-160,30,30);
  
  currentScene.fill(0);
  currentScene.ellipse(w/2+50,h-150,30,30);
  currentScene.fill(255);
  currentScene.text("1", w/2+45,h-160,30,30);

  switch(counter){
    case 0:
      currentScene.fill(255);
      currentScene.ellipse(w/2-50,h-150,30,30);
      currentScene.fill(0);
      currentScene.text("3", w/2-55,h-160,30,30);
      break;
    case 1:
      currentScene.fill(255);
      currentScene.ellipse(w/2,h-150,30,30);
      currentScene.fill(0);
      currentScene.text("2", w/2-5,h-160,30,30); 
      break;
    case 2:
      currentScene.fill(255);
      currentScene.ellipse(w/2+50,h-150,30,30);
      currentScene.fill(0);
      currentScene.text("1", w/2+45,h-160,30,30);
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
    PImage faceCrop = get(faces[0].x-40, faces[0].y-40, faces[0].width+80, faces[0].height+80);
    PGraphics faceImageCanvas = createGraphics(400,400);  
    
    faceImageCanvas.beginDraw();
    faceImageCanvas.image(faceCrop,0,0,400,400);
    faceImageCanvas.save("data/face.jpg");
    println("Face crop successful.");
    faceImageCanvas.endDraw(); 
    userImage.endDraw(); 
  } else {
    //PGraphics faceImageCanvas = createGraphics(400,400);  

    //faceImageCanvas.beginDraw();
    //faceImageCanvas.image(faceDefault,0,0,400,400);
    //faceImageCanvas.save("data/face.jpg");
    //println("Face default successful.");
    //faceImageCanvas.endDraw();     
  }  
}
