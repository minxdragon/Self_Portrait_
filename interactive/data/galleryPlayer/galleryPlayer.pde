import processing.video.*; 
ArrayList<File> allFiles;

//int[] randomNumSelector = {0,1,2};
boolean testMode = true;
String pathTest = "/Users/melhuang/Documents/Clients/Science Gallery/Self Portrait/sp-interactive/interactive/data/gallery/";
String path = "/Users/sgm_tech/Documents/sp-interactive/interactive/data/gallery/";

ArrayList<Movie> playlist;
Movie movie;

void setup() {
  fullScreen();
  windowResize(608, 1080);
  surface.setLocation(100, 0);  
  background(0);  
  frameRate(30);
  getFolderContents();
  assignNewVideoFile(allFiles);
}

void movieEvent(Movie m) {
  m.read();
}

// Get folder list - Cue videos
void getFolderContents(){  
  println("All valid files listed below: ");
  
  if(testMode){
    allFiles = getValidFiles(pathTest);  
  } else {
    allFiles = getValidFiles(path);  
  }
  
  println(allFiles);
}

void assignNewVideoFile(ArrayList<File> l){
  //get new list of folders since last time
  getFolderContents();

  int playlistSize = l.size();
  int randomIndexNumber = floor(random(0,playlistSize));
  //int randomIndexNumber = 0;
  println("Number of valid files found: " + playlistSize);
  
  println(randomIndexNumber, l.get(randomIndexNumber).getAbsolutePath());
  movie = new Movie(this, l.get(randomIndexNumber).getAbsolutePath());
  movie.noLoop();
  movie.play();
}

void draw() {
  float md = movie.duration();
  float mt = movie.time();
  if (mt >= md-0.05) {
    movie.stop();
    fill(0);
    rect(0, 0, width, height);
    assignNewVideoFile(allFiles);
  } else {
    image(movie, 0, 0, width, height);
  }
}


// Listing files
ArrayList<File> getValidFiles(String path) {
  File folder = new File(path);
  File[] listOfFiles = folder.listFiles();
  
  ArrayList<File> listOfValidFiles = new ArrayList<>();
  
  for (int i = 0; i < listOfFiles.length; i++) {
    if(!(listOfFiles[i].getName()).equals(".DS_Store")){
      listOfValidFiles.add(listOfFiles[i]);
    }
  }
  return listOfValidFiles;
}
