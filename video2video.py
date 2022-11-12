import argparse
import base64
import io
import random

import imageio.v3 as iio
import requests

parser = argparse.ArgumentParser(description='Proof-of-concept using img2img to make the analog video2video')
parser.add_argument('path', type=str,
                    help='the path to the video file')
parser.add_argument('prompt', type=str,
                    help='the prompt to use')
parser.add_argument('--negative_prompt', type=str,
                    help='words to de-emphasize when generating frames')
parser.add_argument('--outfile', default='out.mp4', type=str,
                    help='filename for the generated file')
parser.add_argument('--preview', action="store_true",
                    help='generate a short preview video, instead of the full-length video')
parser.add_argument('--sampler', type=str, default='Euler',
                    help='which sampler to use (default: Euler')
parser.add_argument('--denoising_strength', type=float, default=0.75,
                    help='how severely to rewrite the video frame (0: return the same frame, 1: return a wholly new '
                         'frame) (default: 0.75)')
parser.add_argument('--seed', type=int,
                    help='the random seed to use for generation (defaults to randomly selected)')
parser.add_argument('--steps', type=int, default=50,
                    help='the number of iterations used in video frame generation (default: 50)')
parser.add_argument('--cfg_scale', type=float, default=7.0,
                    help='how much freedom the video frame generation has to deviate from the prompt (default: 7.0; '
                         'higher numbers = more deviation')
parser.add_argument('--width', type=int, default=512,
                    help='output width for the generated video (default: 512)')
parser.add_argument('--height', type=int, default=512,
                    help='output height for the generated video (default: 512)')
parser.add_argument('--restore_faces', action="store_true",
                    help='run face restoration on the generated video frames')
parser.add_argument('--tiling', action="store_true",
                    help='generate video frames which will (independently) tile seamlessly')

args = parser.parse_args()

seed = random.randint(1, 2147483647)
if args.seed:
    seed = args.seed

# Gather some metadata, for giving progress, etc.
metadata = iio.immeta(args.path, plugin="pyav")
fps = metadata["fps"]
duration = metadata["duration"]

with iio.imopen(args.outfile, "w", plugin="pyav") as out_file:
    output_fps = fps
    if args.preview is True:
        output_fps = 1

    out_file.init_video_stream("h264", fps=output_fps)

    for idx, frame in enumerate(iio.imiter(args.path, plugin="pyav")):
        if args.preview is True and (idx % fps) != 0:
            continue

        # Print current status
        print(f"{idx}/{fps * duration}")

        # Send POST
        response = requests.post("http://127.0.0.1:7860/sdapi/v1/img2img", json={
            'init_images': [
                "data:image/png;base64," + base64.b64encode(iio.imwrite("<bytes>", frame, extension=".png")).decode()
            ],
            'prompt': args.prompt,
            'denoising_strength': args.denoising_strength,
            'sampler_index': args.sampler,
            'seed': seed,
            'steps': args.steps,
            'cfg_scale': args.cfg_scale,
            'width': args.width,
            'height': args.height,
            'restore_faces': args.restore_faces,
            'tiling': args.tiling,
            'negative_prompt': args.negative_prompt
        })

        # Parse the image out of the response
        image_str = response.json()["images"][0]
        image = iio.imread(io.BytesIO(base64.b64decode(image_str)))

        # Add returned image to video stream
        out_file.write_frame(image)
