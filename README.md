Processing install:
- Processing 4.0
- Processing libraries(install via Processing): ControlP5, OpenCV, Syphon
- Processing library -> Video Export(new Kotlin version - manual install: https://github.com/hamoid/video_export_processing/tree/kotlinGradle) - this library requires ffmpeg
- ffmpeg https://ffmpeg.org/download.html
- Syphoner

Environment setup:
- Homebrew macosx
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
For some reason it corrupted and I had to do this:
rm -fr $(brew --repo homebrew/core)
brew tap homebrew/core
- Install Python
brew install python
- Install imgbbpy
pip3 install imgbbpy --user