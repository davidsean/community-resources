
from biigle import Api

# Biigle email and token
email = 'ENTER EMAIL HERE'
token = 'ENTER TOKEN HERE'
video_id = 123456789


def update_annotation_frames(annotation_id, new_frames, points):
    payload = {
        'points': points,
        'frames': new_frames,
    }
    res = api.put('video-annotations/{}'.format(annotation_id), json=payload)
    if res.status_code != 200:
        print("Unable to snap annotation time for annotation {}".format(annotation_id))


api = Api( email=email, token=token)
res = api.get('videos/{}/annotations'.format(video_id))
if res.status_code != 200:
    print("Unable to get annotations for video{}".format(video_id))
    exit()

for annotation in res.json():
    frames = annotation.get('frames', None)
    points = annotation.get('points', None)
    annotation_id = annotation.get('id', None)
    if frames and points and annotation_id:
        new_frames = []
        for frame in frames:
            new_frames.append(int(frame))
        update_annotation_frames(annotation_id, new_frames, points)