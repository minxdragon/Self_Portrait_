import replicate
import webbrowser
import argparse
import cv2
import numpy as np
from urllib.request import urlopen, Request

parser = argparse.ArgumentParser(description='StableDiffusion')
parser.add_argument('--prompt', type=str, required=True, help='Prompt for generation')
args = parser.parse_args()
init = 'https://res.cloudinary.com/dj1ptpbol/image/upload/v1667791534/opencv0_o7mtqy.jpg' #Init image URL currently fixed, will make dynamic later
promptString = "a full head and shoulders portrait of a person"
negative = "profile, NSFW, abstract, cropped, animal, cartoon, landscape, food, text, logo"

print (args.prompt)

# def stable_diffusion(prompt, init_image, src_img, prompt_strength, negative_prompt):
#     prompt = promptString
#     model = replicate.models.get("stability-ai/stable-diffusion")
#     version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")
#     #version.predict(prompt="a 19th century portrait of a wombat gentleman")
#     init_image = init
#     prompt_strength = 0.3
#     negative_prompt = 'profile, NSFW, abstract, cropped'
#     output_url = version.predict(prompt=(promptString), init_image=init)[0]
#     print(output_url)
#     # download the image, convert it to a NumPy array, and then read
#     # it into OpenCV format
#     request_site = Request(output_url, headers={"User-Agent": "Mozilla/5.0"})
#     req = urlopen(request_site)
#     arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#     img = cv2.imdecode(arr, -1) # 'Load it as it is'
#     img = np.array(img)
#     dream = cv2.imwrite('interactive/data/dream.jpg', img)

#     return dream

# stable_diffusion(prompt = promptString, init_image=init, src_img='interactive/data/dream.jpg', prompt_strength=0.3, negative_prompt=negative)

model = replicate.models.get("stability-ai/stable-diffusion")
version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")
# https://replicate.com/stability-ai/stable-diffusion/versions/27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478#input
inputs = {
    # Input prompt
    'prompt': promptString,

    # The prompt NOT to guide the image generation. Ignored when not using
    # guidance
    'negative_prompt': negative
    }
output = version.predict(**inputs)
print(output)

# output_url = model.predict(prompt=(args.prompt))[0]
# print(output_url)
# webbrowser.open(output)