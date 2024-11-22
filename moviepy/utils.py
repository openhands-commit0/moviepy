from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip

CLIP_TYPES = {'audio': AudioFileClip, 'video': VideoFileClip, 'image': ImageClip}

def close_all_clips(objects=None):
    """Closes all the clips that are passed as arguments or that exist in the global scope.
    
    This is useful to make sure that all files are closed when leaving a session.
    """
    if objects is None:
        objects = list(globals().values())
    
    if not isinstance(objects, (list, tuple)):
        objects = [objects]
    
    for obj in objects:
        if hasattr(obj, 'close'):
            obj.close()