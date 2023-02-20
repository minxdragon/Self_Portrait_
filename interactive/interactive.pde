import processing.video.*;
import java.awt.Rectangle;
import java.util.LinkedHashMap;
import java.io.File;

//import controlP5.*;
import g4p_controls.*;
import gab.opencv.*;
import processing.net.*; 
import codeanticode.syphon.*;
import videoExport.*;

PGraphics canvasWebcam;
PGraphics canvasSyphoner;
SyphonClient client1;
SyphonClient client2;

Boolean testMode = true;

String syphonClient2Name = "";
String syphonClientHome = "Syphoner";
String syphonClientSGM = "python";

Client myClient;

String inString;
String inString2;

PGraphics[] scenes = new PGraphics[11];
GToggleGroup sceneGUI;
GButton b0,b1,b2,b3,b4a,b4b,b5,b6,b7,b8,b9a,b9b,b10;
GButton tog1;
GButton tog2;

PGraphics userImage;
PImage userPhoto;
OpenCV opencv;

String responseKeywordsString = "";
int currentScene = 0;

VideoExport ve;
PGraphics veCanvas;
String userID;
Movie userVideo;

PGraphics videoLayer;
PGraphics progressBarCanvas;
PImage faceDefault;

int w = 630;
int h = 1030;
PFont mono;
int sceneTimer = 0;
PImage pointEmoji;
ArrayList<Portrait> portraits = new ArrayList<Portrait>();

void setup(){
  size(630, 1030,P3D);
  //Libraries seem to go bonkers with fullscreen mode and windowResize
  //fullScreen(P3D);
  //windowResize(608, 1080);
  //delay(20);
  surface.setLocation(800, 0);  
  
  if (testMode){
    syphonClient2Name = syphonClientHome;
  } else {
    syphonClient2Name = syphonClientSGM;
  } 
  
  createCanvases();
  frameRate(30);
  
  mono = createFont("fonts/JetBrainsMono-Regular.ttf", 20);
  textFont(mono);
  //client = new SyphonClient(this);
  canvasWebcam = createGraphics(width, height);  
  client1 = new SyphonClient(this, "syphoncam");
  
  canvasSyphoner = createGraphics(640, 480); 
  client2 = new SyphonClient(this, syphonClient2Name);
  
  myClient = new Client(this, "127.0.0.1", 5008); 
  
  G4P.setDisplayFont("JetBrains Mono", G4P.PLAIN, 20); // New for G4P V4.3
  sceneGUI = new GToggleGroup();
  defineGUI();
  
  sceneFourSetup();
  
  userImage = createGraphics(w, h);
  userPhoto = createImage(w, h,RGB);
  faceDefault = loadImage("default.jpeg");
  
  veCanvas = createGraphics(w, h,P3D);
  createNewVideoExport();
  
  videoLayer = createGraphics(w, h,P3D);
  progressBarCanvas = createGraphics(w, h,P3D);
  
  background(0,0,0);
  
  pointEmoji = loadImage("icons/emoji-point.png");

  for (int i = 0; i < 20; i++){
    portraits.add(new Portrait(i));
  }
}

void draw(){
  listenServerClient();
  renderScene(currentScene);
  image(scenes[currentScene], 0, 0); 
}

void listenServerClient(){  
  if (myClient.available() > 0) {    
    inString = myClient.readString(); 
    println(inString);
    
    String[] responseList = split(inString, ',');
    switch(responseList[0]) {
      case "analysisComplete": 
        currentScene = 3;
        responseKeywordsString = responseList[1];
        //responseKeywordsString musical&level-headed&visionary&risk-taker&creative
        returnedKeywords = split(responseKeywordsString, '&');
        b3.setVisible(true);
        break;
      case "cameraMaskReady": 
        currentScene = 6;
        b6.setVisible(true);
        break;
      default:             
        println(responseList[0] + " is not a recognised response");
        break;
    }
  }
}

void renderScene(int currentSceneNumber){
  switch(currentSceneNumber) {
    case 0: 
      sceneZero(scenes[0]);
      break;
    case 1: 
      sceneOne(scenes[1]);
      break;
    case 2: 
      sceneTwo(scenes[2]);
      break;
    case 3: 
      sceneThree(scenes[3]);
      break;
    case 4: 
      sceneFour(scenes[4]);
      break;
    case 5: 
      sceneFive(scenes[5]);
      break;
    case 6: 
      sceneSix(scenes[6]);
      break;
    case 7: 
      sceneSeven(scenes[7]);
      break;
    case 8: 
      sceneEight(scenes[8]);
      break;
    case 9: 
      sceneNine(scenes[9]);
      break;
    case 10: 
      sceneTen(scenes[10]);
      break;
    }
}

void createCanvases(){
  for(int i = 0; i < 11; i++){
    scenes[i] = createGraphics(w, h, P3D);
  }
}

void defineGUI(){
  defineGUIZero(); 
  defineGUIOne();
  defineGUITwo();
  defineGUIThree();
  defineGUIFour();
  defineGUIFive();
  defineGUISix();
  //defineGUISeven();
  //defineGUIEight();
  defineGUINine();
  defineGUITen();
}

void createNewVideoExport(){
  ve = new VideoExport(this);
  ve.setGraphics(veCanvas);  
}

void screenTimeOut(){
  
}
