# video2video

Leveraging stable diffusion's img2img capability, apply a prompt to a whole video

# Usage

First, get [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) up and running.

Next, start it with the `--api` flag.

Finally, run the script with whatever input and options you like:

```
usage: video2video.py [-h] [--outfile OUTFILE] [--preview] [--sampler SAMPLER] [--denoising_strength DENOISING_STRENGTH] path prompt

Proof-of-concept using img2img to make the analog video2video

positional arguments:
  path                  the path to the video file
  prompt                the prompt to use

options:
  -h, --help            show this help message and exit
  --outfile OUTFILE     filename for the generated file
  --preview             generate a short preview video, instead of the full-length video
  --sampler SAMPLER     which sampler to use (default: Euler
  --denoising_strength DENOISING_STRENGTH
                        how severely to rewrite the image (0: return the same image, 1: return a wholly new image) (default: 0.75)

```
