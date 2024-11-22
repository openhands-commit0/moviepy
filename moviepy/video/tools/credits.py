"""
This module contains different functions to make end and opening
credits, even though it is difficult to fill everyone needs in this
matter.
"""
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.resize import resize
from moviepy.video.VideoClip import ImageClip, TextClip

def credits1(creditfile, width, stretch=30, color='white', stroke_color='black', stroke_width=2, font='Impact-Normal', fontsize=60, gap=0):
    """

    Parameters
    -----------
    
    creditfile
      A text file whose content must be as follows: ::
        
        # This is a comment
        # The next line says : leave 4 blank lines
        .blank 4
        
        ..Executive Story Editor
        MARCEL DURAND
        
        ..Associate Producers
        MARTIN MARCEL
        DIDIER MARTIN
        
        ..Music Supervisor
        JEAN DIDIER
    
    width
      Total width of the credits text in pixels
      
    gap
      Horizontal gap in pixels between the jobs and the names
    
    color
      Color of the text. See ``TextClip.list('color')``
      for a list of acceptable names.

    font
      Name of the font to use. See ``TextClip.list('font')`` for
      the list of fonts you can use on your computer.

    fontsize
      Size of font to use

    stroke_color
      Color of the stroke (=contour line) of the text. If ``None``,
      there will be no stroke.

    stroke_width
      Width of the stroke, in pixels. Can be a float, like 1.5.
    
        
    Returns
    ---------
    
    image
      An ImageClip instance that looks like this and can be scrolled
      to make some credits:

          Executive Story Editor    MARCEL DURAND
             Associate Producers    MARTIN MARCEL
                                    DIDIER MARTIN
                Music Supervisor    JEAN DIDIER
              
    """
    # Parse the credit file
    with open(creditfile) as f:
        lines = f.readlines()

    # Initialize variables
    texts = []
    current_job = None
    current_names = []
    total_height = 0
    max_job_width = 0
    max_name_width = 0

    # Process each line
    for line in lines:
        line = line.strip()
        
        # Skip comments
        if line.startswith('#'):
            continue
            
        # Handle blank lines
        if line.startswith('.blank'):
            try:
                n_blanks = int(line.split()[1])
                total_height += n_blanks * fontsize
            except:
                total_height += fontsize
            continue
            
        # Handle job titles
        if line.startswith('..'):
            # Save previous job if exists
            if current_job is not None:
                job_clip = TextClip(current_job, font=font, fontsize=fontsize, color=color,
                                  stroke_color=stroke_color, stroke_width=stroke_width)
                max_job_width = max(max_job_width, job_clip.w)
                
                for name in current_names:
                    name_clip = TextClip(name, font=font, fontsize=fontsize, color=color,
                                       stroke_color=stroke_color, stroke_width=stroke_width)
                    max_name_width = max(max_name_width, name_clip.w)
                    texts.append((current_job, name))
                    total_height += fontsize
                
            current_job = line[2:]
            current_names = []
            continue
            
        # Handle names
        if current_job is not None and line:
            current_names.append(line)
            
    # Add last job if exists
    if current_job is not None:
        job_clip = TextClip(current_job, font=font, fontsize=fontsize, color=color,
                           stroke_color=stroke_color, stroke_width=stroke_width)
        max_job_width = max(max_job_width, job_clip.w)
        
        for name in current_names:
            name_clip = TextClip(name, font=font, fontsize=fontsize, color=color,
                               stroke_color=stroke_color, stroke_width=stroke_width)
            max_name_width = max(max_name_width, name_clip.w)
            texts.append((current_job, name))
            total_height += fontsize
            
    # Create clips for each text pair
    clips = []
    y = 0
    
    for job, name in texts:
        # Create job clip
        job_clip = TextClip(job, font=font, fontsize=fontsize, color=color,
                           stroke_color=stroke_color, stroke_width=stroke_width)
        job_clip = job_clip.set_position(('right', y))
        
        # Create name clip
        name_clip = TextClip(name, font=font, fontsize=fontsize, color=color,
                            stroke_color=stroke_color, stroke_width=stroke_width)
        name_clip = name_clip.set_position((job_clip.w + gap, y))
        
        clips.extend([job_clip, name_clip])
        y += fontsize
        
    # Create final composite
    final_clip = CompositeVideoClip(clips, size=(width, total_height))
    return final_clip