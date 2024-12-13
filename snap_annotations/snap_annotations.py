
from biigle import Api

# Biigle email and token

email = 'ENTER EMAIL HERE'
token = 'ENTER TOKEN HERE'
video_id = 123456789
video_frame_rate = 123456789 # TODO: implement get_video_fps(video_id) to automatically get the framerate



def update_annotation_frames(annotation_id, new_frames, points):
    payload = {
        'points': points,
        'frames': new_frames,
    }
    res = api.put('video-annotations/{}'.format(annotation_id), json=payload)
    if res.status_code != 200:
        print("Unable to snap annotation time for annotation {}".format(annotation_id))

def snap_timeframe(timestamp:float, fps:float):
    '''
    note: biigle_frame is the timestamp in seconds (not a frame)
    '''
    frame = timestamp*fps
    snapped_timestamp = int(frame)/fps
    return snapped_timestamp

def get_video_fps(video_id:int) -> float:
    '''
    TODO:
    prefetch video until moov atom is complete and return framerate
    '''
    raise NotImplementedError



api = Api( email=email, token=token)
res = api.get('videos/{}/annotations'.format(video_id))
if res.status_code != 200:
    print("Unable to get annotations for video{}".format(video_id))
    exit()

for annotation in res.json():
    frames = annotation.get('frames', None)
    points = annotation.get('points', None)
    annotation_id = annotation.get('id', None)
    print(annotation)
    if frames and points and annotation_id:
        new_frames = []
        for frame in frames:
            new_frame = snap_timeframe(frame, video_frame_rate)
            print(f"will update ts={frame} to ts={new_frame}") 
            new_frames.append(new_frame)
        update_annotation_frames(annotation_id, new_frames, points)