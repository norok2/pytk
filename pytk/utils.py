import os
import warnings

from pytk import tk
from pytk import msg, dbg


# ======================================================================
def has_decorator(
        text,
        pre_decor='"',
        post_decor='"'):
    """
    Determine if a string is delimited by some characters (decorators).

    Args:
        text (str): The text input string.
        pre_decor (str): initial string decorator.
        post_decor (str): final string decorator.

    Returns:
        has_decorator (bool): True if text is delimited by the specified chars.

    Examples:
        >>> has_decorator('"test"')
        True
        >>> has_decorator('"test')
        False
        >>> has_decorator('<test>', '<', '>')
        True
    """
    return text.startswith(pre_decor) and text.endswith(post_decor)


# ======================================================================
def strip_decorator(
        text,
        pre_decor='"',
        post_decor='"'):
    """
    Strip initial and final character sequences (decorators) from a string.

    Args:
        text (str): The text input string.
        pre_decor (str): initial string decorator.
        post_decor (str): final string decorator.

    Returns:
        text (str): the text without the specified decorators.

    Examples:
        >>> strip_decorator('"test"')
        'test'
        >>> strip_decorator('"test')
        'test'
        >>> strip_decorator('<test>', '<', '>')
        'test'
    """
    begin = len(pre_decor) if text.startswith(pre_decor) else None
    end = -len(post_decor) if text.endswith(post_decor) else None
    return text[begin:end]


# ======================================================================
def auto_convert(
        text,
        pre_decor=None,
        post_decor=None):
    """
    Convert value to numeric if possible, or strip delimiters from string.

    Args:
        text (str|int|float|complex): The text input string.
        pre_decor (str): initial string decorator.
        post_decor (str): final string decorator.

    Returns:
        val (int|float|complex): The numeric value of the string.

    Examples:
        >>> auto_convert('<100>', '<', '>')
        100
        >>> auto_convert('<100.0>', '<', '>')
        100.0
        >>> auto_convert('100.0+50j')
        (100+50j)
        >>> auto_convert('1e3')
        1000.0
        >>> auto_convert(1000)
        1000
        >>> auto_convert(1000.0)
        1000.0
    """
    if isinstance(text, str):
        if pre_decor and post_decor and \
                has_decorator(text, pre_decor, post_decor):
            text = strip_decorator(text, pre_decor, post_decor)
        try:
            val = int(text)
        except (TypeError, ValueError):
            try:
                val = float(text)
            except (TypeError, ValueError):
                try:
                    val = complex(text)
                except (TypeError, ValueError):
                    val = text
    else:
        val = text
    return val


# ======================================================================
def get_curr_screen_geometry():
    """
    Workaround to get the size of the current screen in a multi-screen setup.

    Returns:
        geometry (str): The standard Tk geometry string.
            [width]x[height]+[left]+[top]
    """
    temp = tk.Tk()
    temp.update()
    temp.attributes('-fullscreen', True)
    temp.state('iconic')
    geometry = temp.winfo_geometry()
    temp.destroy()
    return geometry


# ======================================================================
def set_icon(
        root,
        basename,
        dirpath=os.path.abspath(os.path.dirname(__file__))):
    basepath = os.path.join(dirpath, basename) if dirpath else basename

    # first try modern file formats
    for file_ext in ['png', 'gif']:
        if not basepath.endswith('.' + file_ext):
            filepath = basepath + '.' + file_ext
        else:
            filepath = basepath
        try:
            icon = tk.PhotoImage(file=filepath)
            root.tk.call('wm', 'iconphoto', root._w, icon)
        except tk.TclError:
            warnings.warn('E: Could not use icon `{}`'.format(filepath))
        else:
            return

    # fall back to ico/xbm format
    tk_sys = root.tk.call('tk', 'windowingsystem')
    if tk_sys.startswith('win'):
        filepath = basepath + '.ico'
    else:  # if tk_sys == 'x11':
        filepath = '@' + basepath + '.xbm'
    try:
        root.iconbitmap(filepath)
    except tk.TclError:
        warnings.warn('E: Could not use icon `{}`.'.format(filepath))
    else:
        return


# ======================================================================
def center(target, parent=None):
    target.update_idletasks()
    if parent is None:
        parent_geom = Geometry(get_curr_screen_geometry())
    else:
        parent.update_idletasks()
        parent_geom = Geometry(parent.winfo_geometry())
    target_geom = Geometry(target.winfo_geometry()).set_to_center(parent_geom)
    target.geometry(target_geom.as_str())


# ======================================================================
class Geometry():
    def __init__(self, geometry_text=None):
        """
        Generate a geometry object from the standard Tk geometry string.

        Args:
            geometry_text (str): The standard Tk geometry string.
                [width]x[height]+[left]+[top]

        Returns:
            None.
        """
        try:
            tokens1 = geometry_text.split('+')
            tokens2 = tokens1[0].split('x')
            self.width = int(tokens2[0])
            self.height = int(tokens2[1])
            self.left = int(tokens1[1])
            self.top = int(tokens1[2])
        except:
            self.width, self.height, self.left, self.top = 0, 0, 0, 0

    def __repr__(self):
        return self.as_str()

    def as_dict(self):
        return {
            'w': self.width,
            'h': self.height,
            'l': self.left,
            't': self.top}

    def as_tuple(self):
        return self.width, self.height, self.left, self.top

    def as_str(self):
        return '{w:d}x{h:d}+{l:d}+{t:d}'.format(**self.as_dict())

    def set_to_center(self, parent):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = parent.width // 2 - self.width // 2 + parent.left
        self.top = parent.height // 2 - self.height // 2 + parent.top
        return self

    def set_to_origin(self):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = 0
        self.top = 0
        return self

    def set_to_top_left(self, parent):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = parent.left
        self.top = parent.top
        return self

    def set_to_top(self, parent):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = parent.width // 2 - self.width // 2 + parent.left
        self.top = parent.top
        return self

    def set_to_top_right(self, parent):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = parent.width - self.width + parent.left
        self.top = parent.top
        return self

    def set_to_right(self, parent):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = parent.width - self.width + parent.left
        self.top = parent.height // 2 - self.height // 2 + parent.top
        return self

    def set_to_bottom_right(self, parent):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = parent.width - self.width + parent.left
        self.top = parent.height - self.height + parent.top
        return self

    def set_to_bottom(self, parent):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = parent.width // 2 - self.width // 2 + parent.left
        self.top = parent.height - self.height + parent.top
        return self

    def set_to_bottom_left(self, parent):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = parent.left
        self.top = parent.height - self.height + parent.top
        return self

    def set_to_left(self, parent):
        """
        Update the geometry to be centered with respect to a container.

        Args:
            parent (Geometry): The geometry of the container.

        Returns:
            geometry (Geometry): The updated geometry.
        """
        self.left = parent.left
        self.top = parent.height // 2 - self.height // 2 + parent.top
        return self
