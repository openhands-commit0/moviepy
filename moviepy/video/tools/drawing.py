"""
This module deals with making images (np arrays). It provides drawing
methods that are difficult to do with the existing Python libraries.
"""
import numpy as np

def blit(im1, im2, pos=None, mask=None, ismask=False):
    """ Blit an image over another.
    
    Blits ``im1`` on ``im2`` as position ``pos=(x,y)``, using the
    ``mask`` if provided. If ``im1`` and ``im2`` are mask pictures
    (2D float arrays) then ``ismask`` must be ``True``.
    """
    pass

def color_gradient(size, p1, p2=None, vector=None, r=None, col1=0, col2=1.0, shape='linear', offset=0):
    """Draw a linear, bilinear, or radial gradient.
    
    The result is a picture of size ``size``, whose color varies
    gradually from color `col1` in position ``p1`` to color ``col2``
    in position ``p2``.
    
    If it is a RGB picture the result must be transformed into
    a 'uint8' array to be displayed normally:
     
     
    Parameters
    ------------      
    
    size
        Size (width, height) in pixels of the final picture/array.
    
    p1, p2
        Coordinates (x,y) in pixels of the limit point for ``col1``
        and ``col2``. The color 'before' ``p1`` is ``col1`` and it
        gradually changes in the direction of ``p2`` until it is ``col2``
        when it reaches ``p2``.
    
    vector
        A vector [x,y] in pixels that can be provided instead of ``p2``.
        ``p2`` is then defined as (p1 + vector).
    
    col1, col2
        Either floats between 0 and 1 (for gradients used in masks)
        or [R,G,B] arrays (for colored gradients).
                         
    shape
        'linear', 'bilinear', or 'circular'.
        In a linear gradient the color varies in one direction,
        from point ``p1`` to point ``p2``.
        In a bilinear gradient it also varies symetrically form ``p1``
        in the other direction.
        In a circular gradient it goes from ``col1`` to ``col2`` in all
        directions.
    
    offset
        Real number between 0 and 1 indicating the fraction of the vector
        at which the gradient actually starts. For instance if ``offset``
        is 0.9 in a gradient going from p1 to p2, then the gradient will
        only occur near p2 (before that everything is of color ``col1``)
        If the offset is 0.9 in a radial gradient, the gradient will
        occur in the region located between 90% and 100% of the radius,
        this creates a blurry disc of radius d(p1,p2).  
    
    Returns
    --------
    
    image
        An Numpy array of dimensions (W,H,ncolors) of type float
        representing the image of the gradient.
        
    
    Examples
    ---------
    
    >>> grad = color_gradient(blabla).astype('uint8')
    
    """
    pass

def color_split(size, x=None, y=None, p1=None, p2=None, vector=None, col1=0, col2=1.0, grad_width=0):
    """Make an image splitted in 2 colored regions.
    
    Returns an array of size ``size`` divided in two regions called 1 and
    2 in wht follows, and which will have colors col& and col2
    respectively.
    
    Parameters
    -----------
    
    x: (int)
        If provided, the image is splitted horizontally in x, the left
        region being region 1.
            
    y: (int)
        If provided, the image is splitted vertically in y, the top region
        being region 1.
    
    p1,p2:
        Positions (x1,y1),(x2,y2) in pixels, where the numbers can be
        floats. Region 1 is defined as the whole region on the left when
        going from ``p1`` to ``p2``.
    
    p1, vector:
        ``p1`` is (x1,y1) and vector (v1,v2), where the numbers can be
        floats. Region 1 is then the region on the left when starting
        in position ``p1`` and going in the direction given by ``vector``.
         
    gradient_width
        If not zero, the split is not sharp, but gradual over a region of
        width ``gradient_width`` (in pixels). This is preferable in many
        situations (for instance for antialiasing). 
     
    
    Examples
    ---------
    
    >>> size = [200,200]
    >>> # an image with all pixels with x<50 =0, the others =1
    >>> color_split(size, x=50, col1=0, col2=1)
    >>> # an image with all pixels with y<50 red, the others green
    >>> color_split(size, x=50, col1=[255,0,0], col2=[0,255,0])
    >>> # An image splitted along an arbitrary line (see below) 
    >>> color_split(size, p1=[20,50], p2=[25,70] col1=0, col2=1)
            
    """
    pass

def circle(screensize, center, radius, col1=1.0, col2=0, blur=1):
    """ Draw an image with a circle.
    
    Draws a circle of color ``col1``, on a background of color ``col2``,
    on a screen of size ``screensize`` at the position ``center=(x,y)``,
    with a radius ``radius`` but slightly blurred on the border by ``blur``
    pixels
    """
    pass