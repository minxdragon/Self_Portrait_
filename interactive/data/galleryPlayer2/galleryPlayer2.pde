import processing.video.*; 
import java.io.*;
import java.util.*;

boolean testMode = false;
String pathHome = "/Users/melhuang/Documents/Clients/Science Gallery/Self Portrait/sp-interactive/interactive/data/gallery/";
String pathSGM = "/Users/sgm_tech/Documents/Self_Portrait_-base/interactive/data/gallery/";
String path = "";

Movie movie;
int finalWindowWidth = 1280;
int finalWindowHeight = 720;
int counter = 0;
int newPlaylistCountdown = 0;

int playlistSize = 10;
File[] playlistFiles = new File[playlistSize];
Movie[] playlist = new Movie[playlistSize];
int currentNumberofFiles = 0;

// fullscreen 0 and 3 on Gallery Computer
void setup() {
  fullScreen(3);
  windowResize(finalWindowWidth,finalWindowHeight);
  //surface.setLocation(100, 0);  
  background(0);  
  frameRate(30);
  
  if(testMode){
    path = pathHome;
  } else {
    path = pathSGM;
  }

  getFolderContents();
  currentNumberofFiles = checkForNewFiles();
  assignNewVideoFile();
}

void movieEvent(Movie m) {
  m.read();
}

void assignNewVideoFile(){
  int randomIndexNumber = floor(random(0,playlistSize));  
  println("Playing: ", randomIndexNumber, playlistFiles[randomIndexNumber].getAbsolutePath());
  
  movie = playlist[randomIndexNumber];
  movie.noLoop();
  movie.play();
  
  counter++;
  newPlaylistCountdown++;
  println(counter);
}

void draw() {
  float md = movie.duration();
  float mt = movie.time();
  if (mt >= md-0.05) {
    movie.stop();
    assignNewVideoFile();
  } else {
    pushMatrix();
    scale(1);
    translate(finalWindowWidth/2,finalWindowHeight/2);
    rotate(radians(-90));
    image(movie, -finalWindowHeight/2, -finalWindowWidth/2, finalWindowHeight, finalWindowWidth);
    popMatrix();
  }
  
  if(newPlaylistCountdown > 200){
    print(currentNumberofFiles, checkForNewFiles());
    
    if (checkForNewFiles() > currentNumberofFiles){
      getFolderContents();
      println("New list");
    } else {
      println("No new videos");
    }
    
    newPlaylistCountdown = 0;
  }
}

void getFolderContents(){    
  getSomeValidFiles();  
  createNewPlaylist();
}

// Listing files
void getSomeValidFiles() {
  File folder = new File(path);
  FileFilter filter = new FileFilter(){
    public boolean accept(File f){
      return f.getName().endsWith(".mp4");
    }
  };
  File[] listOfFiles = folder.listFiles(filter);
  Arrays.sort(listOfFiles, Comparator.comparingLong(File::lastModified));
  
  for (int i = 0; i < playlistSize; i++) {
    playlistFiles[i] = listOfFiles[listOfFiles.length-1-i];
  }
}

int checkForNewFiles(){
  println(path);
  File folder = new File(path);
  FileFilter filter = new FileFilter(){
    public boolean accept(File f){
      return f.getName().endsWith(".mp4");
    }
  };
  return folder.listFiles(filter).length;
}

void createNewPlaylist(){
  for (int i = 0; i < playlistSize; i++) {
    playlist[i] = new Movie(this, playlistFiles[i].getAbsolutePath());
  }
}
