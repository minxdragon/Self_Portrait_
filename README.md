# Modified code based on Faceswap and integrated Stable Diffusion.
The face swap code has stable diffusion worked into it, to allow generation of new faces on the fly. additionally a classifier has been added with personality traits to be classified and returned as a part of a process to generate the stablediffusion mask for the development of a new interactive artwork.

### Stable Diffusion using Replicate
### Face Swap using forked code below
### Multi Label Classifier

# Classify
take a shot from the camera and crop to your face and classify (using the dummy classifier)
```sh
python sixpredict.py
```

# FaceSwap
Swap face between two photos for Python 3 with OpenCV and dlib.

## Get Started
```sh
python main.py --src imgs/test6.jpg --dst dream.jpg --out test.jpg --correct_color --prompt 'image promt here'
```

## Install
### Requirements
* `pip install -r requirements.txt`
* '''conda create --name selfportrait --file requirements.txt'''

Note: See [requirements.txt](requirements.txt) for more details.

### Swap Your Face
```sh
python main.py ...
```
Note: Run **python main.py -h** for more details.


### Real-time camera
```sh
python main_video.py --src_img dream.jpg --show --correct_color --save_path {*.avi} --prompt 'image promt here'
```
### Video
```sh
python main_video.py --src_img dream.jpg --video_path {video_path} --show --correct_color --save_path {*.avi}
```
### To Do
- make the local file save readable as an init or upload the file save
- train a proper classifier!
