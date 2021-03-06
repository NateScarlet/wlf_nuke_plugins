"""
This type stub file was generated by pyright.
"""

class CameraFilmBackPresets:
    """A simple container object for holding the label and film back data of a camera."""

    def __init__(self) -> None:
        """Initialise by adding all of our presets."""
        ...
    def addPreset(self, label, filmBackDict):
        """Parse a dict for the camera aperture size and add to the list."""
        ...

_gFilmBackPresets = CameraFilmBackPresets()

def getLabels():
    """Returns the list of preset labels for display in the knob."""
    ...

def getFilmBackSize(index):
    """Returns the film back size for the given index."""
    ...

def addPreset(label, haperture, vaperture):
    """Adds a preset to the global list of presets."""
    ...
