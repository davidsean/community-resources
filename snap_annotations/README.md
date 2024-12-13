# Snap Annotations

Adjusts the temporal coordinate on annotations to snap to closest exact video timestamp. Actually just takes the integer part of the frame.


## Usage

Make a token, get the video_id and run the script!

WARNING: This may modify all annotations of the video!
Make a volume backup first.

Open the script and adjust `email`,  `token` and `video_id` accordingly.

```bash
python snap_annotations.py 
```
