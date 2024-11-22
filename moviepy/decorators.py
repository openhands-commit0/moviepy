"""
all decorators used in moviepy go there
"""
import decorator
from moviepy.tools import cvsecs

@decorator.decorator
def outplace(f, clip, *a, **k):
    """ Applies f(clip.copy(), *a, **k) and returns clip.copy()"""
    newclip = clip.copy()
    f(newclip, *a, **k)
    return newclip

@decorator.decorator
def convert_masks_to_RGB(f, clip, *a, **k):
    """ If the clip is a mask, convert it to RGB before running the function """
    if clip.ismask:
        clip = clip.rgb_mode()
    return f(clip, *a, **k)

@decorator.decorator
def apply_to_mask(f, clip, *a, **k):
    """ This decorator will apply the same function f to the mask of
        the clip created with f """
    newclip = f(clip, *a, **k)
    if getattr(clip, 'mask', None) is not None:
        newclip.mask = f(clip.mask, *a, **k)
    return newclip

@decorator.decorator
def apply_to_audio(f, clip, *a, **k):
    """ This decorator will apply the function f to the audio of
        the clip created with f """
    newclip = f(clip, *a, **k)
    if getattr(clip, 'audio', None) is not None:
        newclip.audio = f(clip.audio, *a, **k)
    return newclip

@decorator.decorator
def requires_duration(f, clip, *a, **k):
    """ Raise an error if the clip has no duration."""
    if clip.duration is None:
        raise ValueError("Attribute 'duration' not set")
    else:
        return f(clip, *a, **k)

@decorator.decorator
def audio_video_fx(f, clip, *a, **k):
    """ Use an audio function on a video/audio clip
    
    This decorator tells that the function f (audioclip -> audioclip)
    can be also used on a video clip, at which case it returns a
    videoclip with unmodified video and modified audio.
    """
    if hasattr(clip, 'audio'):
        newclip = clip.copy()
        if clip.audio is not None:
            newclip.audio = f(clip.audio, *a, **k)
        return newclip
    else:
        return f(clip, *a, **k)

def preprocess_args(fun, varnames):
    """ Applies fun to variables in varnames before launching the function """
    def wrapper(f, *a, **kw):
        if hasattr(f, '__code__'):
            names = f.__code__.co_varnames
        else:
            names = getattr(f, 'func', f).__code__.co_varnames
        
        new_a = [fun(arg) if (name in varnames) and (arg is not None)
                else arg
                for (arg, name) in zip(a, names)]
        new_kw = {k: fun(v) if k in varnames else v
                 for (k, v) in kw.items()}
        return f(*new_a, **new_kw)
    return decorator.decorator(wrapper)

def convert_to_seconds(varnames):
    """Converts the specified variables to seconds"""
    return preprocess_args(cvsecs, varnames)

@decorator.decorator
def add_mask_if_none(f, clip, *a, **k):
    """ Add a mask to the clip if there is none. """
    if clip.mask is None:
        clip = clip.add_mask()
    return f(clip, *a, **k)

@decorator.decorator
def use_clip_fps_by_default(f, clip, *a, **k):
    """ Will use clip.fps if no fps=... is provided in **k """
    if 'fps' not in k and hasattr(clip, 'fps') and clip.fps is not None:
        k['fps'] = clip.fps
    return f(clip, *a, **k)