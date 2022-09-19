import replicate
import webbrowser
import argparse

parser = argparse.ArgumentParser(description='StableDiffusion')
parser.add_argument('--prompt', type=str, required=True, help='Prompt for generation')
args = parser.parse_args()

print (args.prompt)

model = replicate.models.get("stability-ai/stable-diffusion")

output_url = model.predict(prompt=(args.prompt))[0]
print(output_url)
webbrowser.open(output_url)