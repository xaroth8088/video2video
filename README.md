# video2video

Leveraging stable diffusion's img2img capability, apply a prompt to a whole video

# Usage

First, get [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) up and running.

Next, start it with the `--api` flag.

Finally, run the script with whatever input and options you like:

```
usage: video2video.py [-h] [--negative_prompt NEGATIVE_PROMPT] [--outfile OUTFILE] [--preview] [--sampler SAMPLER] [--denoising_strength DENOISING_STRENGTH] [--seed SEED] [--steps STEPS] [--cfg_scale CFG_SCALE] [--width WIDTH]
                      [--height HEIGHT] [--restore_faces] [--tiling]
                      path prompt

Proof-of-concept using img2img to make the analog video2video

positional arguments:
  path                  the path to the video file
  prompt                the prompt to use

options:
  -h, --help            show this help message and exit
  --negative_prompt NEGATIVE_PROMPT
                        words to de-emphasize when generating frames
  --outfile OUTFILE     filename for the generated file
  --preview             generate a short preview video, instead of the full-length video
  --sampler SAMPLER     which sampler to use (default: Euler)
  --denoising_strength DENOISING_STRENGTH
                        how severely to rewrite the video frame (0: return the same frame, 1: return a wholly new frame) (default: 0.75)
  --seed SEED           the random seed to use for generation (defaults to randomly selected)
  --steps STEPS         the number of iterations used in video frame generation (default: 50)
  --cfg_scale CFG_SCALE
                        how much freedom the video frame generation has to deviate from the prompt (default: 7.0; higher numbers = more deviation
  --width WIDTH         output width for the generated video (default: 512)
  --height HEIGHT       output height for the generated video (default: 512)
  --restore_faces       run face restoration on the generated video frames
  --tiling              generate video frames which will (independently) tile seamlessly
```
