import codeanticode.syphon.*;

PGraphics canvas;
SyphonServer server;

import processing.video.*;
Capture cam;

void setup() { 
  size(640, 508, P3D);
  canvas = createGraphics(640, 508, P3D);
  
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
  canvas.image(cam, 0, 0,640, 508);
  canvas.endDraw();
  
  image(canvas, 0, 0);
  server.sendImage(canvas);
}
