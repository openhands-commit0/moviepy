resize_possible = True
resizer = None

try:
    import cv2
    import numpy as np
    def cv2_resize(pic, newsize):
        return cv2.resize(pic, tuple(map(int, newsize[::-1])))
    resizer = cv2_resize
    resizer.origin = 'cv2'
except ImportError:
    try:
        from PIL import Image
        import numpy as np
        def pil_resize(pic, newsize):
            newsize = tuple(map(int, newsize[::-1]))
            img = Image.fromarray(pic)
            img = img.resize(newsize, Image.BILINEAR)
            return np.array(img)
        resizer = pil_resize
        resizer.origin = 'PIL'
    except ImportError:
        try:
            from scipy.misc import imresize
            resizer = lambda pic, newsize: imresize(pic, map(int, newsize[::-1]))
            resizer.origin = 'Scipy'
        except ImportError:
            resize_possible = False
from moviepy.decorators import apply_to_mask

def resize(clip, newsize=None, height=None, width=None, apply_to_mask=True):
    """ 
    Returns a video clip that is a resized version of the clip.
    
    Parameters
    ------------
    
    newsize:
      Can be either 
        - ``(width,height)`` in pixels or a float representing
        - A scaling factor, like 0.5
        - A function of time returning one of these.
            
    width:
      width of the new clip in pixel. The height is then computed so
      that the width/height ratio is conserved. 
            
    height:
      height of the new clip in pixel. The width is then computed so
      that the width/height ratio is conserved.
    
    Examples
    ----------
             
    >>> myClip.resize( (460,720) ) # New resolution: (460,720)
    >>> myClip.resize(0.6) # width and heigth multiplied by 0.6
    >>> myClip.resize(width=800) # height computed automatically.
    >>> myClip.resize(lambda t : 1+0.02*t) # slow swelling of the clip
    
    """
    if not resize_possible:
        raise ImportError("No module can be found for video resizing. Install either OpenCV or Pillow.")

    if newsize is not None:
        if hasattr(newsize, '__call__'):
            def get_newsize(t):
                ns = newsize(t)
                if isinstance(ns, (int, float)):
                    return [ns * clip.size[0], ns * clip.size[1]]
                else:
                    return ns
            
            newsize_aux = get_newsize
        else:
            if isinstance(newsize, (int, float)):
                newsize = [newsize * clip.size[0], newsize * clip.size[1]]
            
            newsize_aux = lambda t: newsize

    elif height is not None:
        if hasattr(height, '__call__'):
            newsize_aux = lambda t: [height(t) * clip.w / clip.h, height(t)]
        else:
            newsize_aux = lambda t: [height * clip.w / clip.h, height]

    elif width is not None:
        if hasattr(width, '__call__'):
            newsize_aux = lambda t: [width(t), width(t) * clip.h / clip.w]
        else:
            newsize_aux = lambda t: [width, width * clip.h / clip.w]

    else:
        raise ValueError('No new size provided! Use newsize, height, or width.')

    def transform(get_frame, t):
        img = get_frame(t)
        return resizer(img, newsize_aux(t))

    newclip = clip.transform(transform, keep_duration=True)

    if apply_to_mask and clip.mask is not None:
        newclip.mask = resize(clip.mask, newsize, height, width, apply_to_mask=False)

    return newclip
if not resize_possible:
    doc = resize.__doc__
    resize.__doc__ = doc