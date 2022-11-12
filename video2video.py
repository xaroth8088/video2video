import argparse
import io
import requests
import base64
import imageio.v3 as iio

parser = argparse.ArgumentParser(description='Proof-of-concept using img2img to make the analog video2video')
parser.add_argument('path', type=str,
                    help='the path to the video file')
parser.add_argument('prompt', type=str,
                    help='the prompt to use')
parser.add_argument('--outfile', default='out.mp4', type=str,
                    help='filename for the generated file')
parser.add_argument('--preview', action="store_true",
                    help='generate a short preview video, instead of the full-length video')
parser.add_argument('--sampler', type=str, default='Euler',
                    help='which sampler to use (default: Euler')
parser.add_argument('--denoising_strength', type=float, default=0.75,
                    help='how severely to rewrite the image (0: return the same image, 1: return a wholly new image) (default: 0.75)')

args = parser.parse_args()

# Things to convert to args later
seed = 1234
steps = 50
cfg_scale = 7.0
width = 512
height = 512
restore_faces = False
tiling = False
negative_prompt = None

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
            'steps': steps,
            'cfg_scale': cfg_scale,
            'width': width,
            'height': height,
            'restore_faces': restore_faces,
            'tiling': tiling,
            'negative_prompt': negative_prompt
        })
        image_str = response.json()["images"][0]
        image = iio.imread(io.BytesIO(base64.b64decode(image_str)))

        # Add returned image to video stream
        out_file.write_frame(image)
