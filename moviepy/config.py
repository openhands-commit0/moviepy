import os
import subprocess as sp
from .compat import DEVNULL
from .config_defaults import FFMPEG_BINARY, IMAGEMAGICK_BINARY

def try_cmd(cmd):
    """Try to execute a command and return (success, stderr output)."""
    try:
        process = sp.Popen(cmd, stdout=DEVNULL, stderr=sp.PIPE)
        _, error = process.communicate()
        success = process.returncode == 0
        return success, error
    except Exception as e:
        return False, str(e)
if os.name == 'nt':
    try:
        import winreg as wr
    except ImportError:
        import _winreg as wr
if FFMPEG_BINARY == 'ffmpeg-imageio':
    from imageio.plugins.ffmpeg import get_exe
    FFMPEG_BINARY = get_exe()
elif FFMPEG_BINARY == 'auto-detect':
    if try_cmd(['ffmpeg'])[0]:
        FFMPEG_BINARY = 'ffmpeg'
    elif try_cmd(['ffmpeg.exe'])[0]:
        FFMPEG_BINARY = 'ffmpeg.exe'
    else:
        FFMPEG_BINARY = 'unset'
else:
    success, err = try_cmd([FFMPEG_BINARY])
    if not success:
        raise IOError(str(err) + ' - The path specified for the ffmpeg binary might be wrong')
if IMAGEMAGICK_BINARY == 'auto-detect':
    if os.name == 'nt':
        try:
            key = wr.OpenKey(wr.HKEY_LOCAL_MACHINE, 'SOFTWARE\\ImageMagick\\Current')
            IMAGEMAGICK_BINARY = wr.QueryValueEx(key, 'BinPath')[0] + '\\convert.exe'
            key.Close()
        except:
            IMAGEMAGICK_BINARY = 'unset'
    elif try_cmd(['convert'])[0]:
        IMAGEMAGICK_BINARY = 'convert'
    else:
        IMAGEMAGICK_BINARY = 'unset'
else:
    if not os.path.exists(IMAGEMAGICK_BINARY):
        raise IOError('ImageMagick binary cannot be found at {}'.format(IMAGEMAGICK_BINARY))
    if not os.path.isfile(IMAGEMAGICK_BINARY):
        raise IOError('ImageMagick binary found at {} is not a file'.format(IMAGEMAGICK_BINARY))
    success, err = try_cmd([IMAGEMAGICK_BINARY])
    if not success:
        raise IOError('%s - The path specified for the ImageMagick binary might be wrong: %s' % (err, IMAGEMAGICK_BINARY))

def get_setting(varname):
    """ Returns the value of a configuration variable. """
    if varname == "FFMPEG_BINARY":
        return FFMPEG_BINARY
    elif varname == "IMAGEMAGICK_BINARY":
        return IMAGEMAGICK_BINARY
    else:
        raise ValueError(f"Unknown setting {varname}")

def change_settings(new_settings=None, filename=None):
    """ Changes the value of configuration variables."""
    global FFMPEG_BINARY, IMAGEMAGICK_BINARY
    
    if new_settings is None:
        new_settings = {}
    
    if filename is not None:
        # Load settings from file
        with open(filename) as f:
            exec(f.read(), globals())
    
    # Update with new settings
    if "FFMPEG_BINARY" in new_settings:
        FFMPEG_BINARY = new_settings["FFMPEG_BINARY"]
    if "IMAGEMAGICK_BINARY" in new_settings:
        IMAGEMAGICK_BINARY = new_settings["IMAGEMAGICK_BINARY"]
if __name__ == '__main__':
    if try_cmd([FFMPEG_BINARY])[0]:
        print('MoviePy : ffmpeg successfully found.')
    else:
        print("MoviePy : can't find or access ffmpeg.")
    if try_cmd([IMAGEMAGICK_BINARY])[0]:
        print('MoviePy : ImageMagick successfully found.')
    else:
        print("MoviePy : can't find or access ImageMagick.")