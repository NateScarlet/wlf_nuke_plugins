"""
This type stub file was generated by pyright.
"""

def create_curve(): ...
def create_read(defaulttype=...):
    """Create a Read node for a file selected from the file browser.
    If a node is currently selected in the nodegraph and it has a 'file'
    (or failing that a 'proxy') knob, the value (if any) will be used as the default
    path for the file browser."""
    ...

def isGeoFilename(filename): ...
def isAbcFilename(filename): ...
def isDeepFilename(filename): ...
def isAudioFilename(filename): ...
def create_viewsplitjoin(): ...
