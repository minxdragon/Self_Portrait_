import schedule
import time
import datetime
import replicate
import requests
import cv2
import numpy as np
from urllib.request import Request, urlopen

print("Starting script...")

def job():
    print("I'm running on", datetime.datetime.now())
    promptString = "an adorable painting of a cat"
    model = replicate.models.get("jagilley/controlnet-pose")
    version = model.versions.get("0304f7f774ba7341ef754231f794b1ba3d129e3c46af3022241325ae0c50fb99")
    # https://replicate.com/jagilley/controlnet-hed/versions/cde353130c86f37d0af4060cd757ab3009cac68eb58df216768f907f0d0a0653#input
    inputs = {
        # Input image
        'image': open("face.jpg", "rb"),

        # Prompt for the model
        'prompt': promptString,

        # Number of samples (higher values may OOM)
        'num_samples': "1",

        # Image resolution to be generated
        'image_resolution': "512",

        # Steps
        'ddim_steps': 20,

        # Guidance Scale
        # Range: 0.1 to 30
        'scale': 9,

        # Seed
        # 'seed': ...,
        
        # Canny line detection low threshold
        # Range: 1 to 255
        'low_threshold': 100,

        # Canny line detection high threshold
        # Range: 1 to 255
        'high_threshold': 200,

        # eta (DDIM)
        'eta': 0,

        # Added Prompt
        'a_prompt': "painting, best quality, extremely detailed",

        # Negative Prompt
        'n_prompt': "photograph, photographic, naked, nude, longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality",

        # Resolution for detection)
        # Range: 128 to 1024
        'detect_resolution': 512,
    }

    # https://replicate.com/jagilley/controlnet-hed/versions/cde353130c86f37d0af4060cd757ab3009cac68eb58df216768f907f0d0a0653#output-schema
    output = version.predict(**inputs)
    print(output)
    second_url = output[1] # select the second URL from the output list
    request_site = Request(second_url, headers={"User-Agent": "Mozilla/5.0"})
    req = urlopen(request_site)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    img = np.array(img)
    dream = cv2.imwrite('interactive/data/dream.jpg', img)

    return dream

while True:
    print("starting loop")
    now = datetime.datetime.now().time()
    if now >= datetime.time(23, 0) and now <= datetime.time(7, 0):
        job()
    print("sleeping")
    time.sleep(3600) # Sleep for 1 hour