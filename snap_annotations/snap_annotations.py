
from biigle import Api
import cv2

# Biigle email and token
email = 'ENTER EMAIL HERE'
token = 'ENTER TOKEN HERE'
video_id = 123456789
video_frame_rate = 123456789 # TODO: implement get_video_fps(video_id) to automatically get the framerate

# experimental, try this if you do not that the framerate
# video_frame_rate = get_video_fps(video_id)


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


def get_partial_video(video_id:int, start:int, end:int, fname) -> bool:
    print(f"start: {start} \t end:{end}")

    headers = {"Range": f"bytes={start}-{end}"}
    res = api.get('videos/{}/file'.format(video_id), headers=headers)
    if res.status_code != 206:
        print('could not get partial video')
        exit()
    # write partial video before opening it as a file.
    # TODO: try to see how to open a buffered bytesIO Object
    with open(fname, 'ab') as fp:
        fp.write(res.content)
    cap = cv2.VideoCapture(fname)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps

def get_video_fps(video_id:int) -> float:
    '''
    TODO:
    prefetch video until moov atom is complete and return framerate
    '''
    # get filename because we will write the file
    # TODO: try to see how to open a buffered bytesIO Object
    res = api.get('videos/{}'.format(video_id))
    fname = res.json().get('filename', None)
    if fname is None:
        print('Cannot get video filename')
        exit()

    chunk_size = 1024
    for chunk_num in range(32):
        start = chunk_num*chunk_size
        end = (chunk_num+1)*chunk_size-1
        fps = get_partial_video(video_id, start, end, fname)
        if fps != 0.0:
            break
    return fps






api = Api( email=email, token=token)
res = api.get('videos/{}/annotations'.format(video_id))
if res.status_code != 200:
    print("Unable to get annotations for video{}".format(video_id))
    exit()

for annotation in res.json():
    frames = annotation.get('frames', None)
    points = annotation.get('points', None)
    annotation_id = annotation.get('id', None)
    print("Found annotation: {annotation}")
    if frames and points and annotation_id:
        new_frames = []
        for frame in frames:
            new_frame = snap_timeframe(frame, video_frame_rate)
            print(f"will update ts={frame} to ts={new_frame}") 
            new_frames.append(new_frame)
        update_annotation_frames(annotation_id, new_frames, points)