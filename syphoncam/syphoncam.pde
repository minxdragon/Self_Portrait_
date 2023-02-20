import codeanticode.syphon.*;

PGraphics canvas;
SyphonServer server;

import processing.video.*;
Capture cam;

void setup() { 
  size(640, 480, P3D);
  canvas = createGraphics(640, 480, P3D);
  
  // Create syphon server to send frames out.
  server = new SyphonServer(this, "Processing Syphon");
  
  cam = new Capture(this, "pipeline:autovideosrc");
  cam.start();
}

void draw() {
  if (cam.available() == true) {
    cam.read();
  }

  canvas.beginDraw();
  canvas.pushMatrix();
  canvas.translate(width,0);
  canvas.scale(-1,1);  
  canvas.image(cam, 0, 0,640,480);
  canvas.popMatrix();
  canvas.endDraw();

  image(canvas, 0, 0);
  
  server.sendImage(canvas);
}
