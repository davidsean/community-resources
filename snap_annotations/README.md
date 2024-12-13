# Snap Annotations

Adjusts the temporal coordinate on annotations to snap to closest "exact" timestamp of a video frame.


## Usage
Make a token, get the video_id and run the script!

For the moment, you need to specify the video framerate.

WARNING: This may modify all annotations of the video!
Make a volume backup first.

Open the script and adjust `email`,  `token` and `video_id` accordingly.

```bash
python snap_annotations.py 
```
