"""
This type stub file was generated by pyright.
"""

"""
This module contains classes for performing a capture of the viewer.
"""

class CaptureViewer(object):
    """This class provides a way of capturing the contents of the viewer to disk."""

    def __init__(
        self,
        flipbook,
        frameRange,
        viewer,
        selectedViews,
        defaultWritePath,
        customWritePath,
        doFlipbook,
        doCleanup,
    ) -> None: ...
    def __call__(self):
        """Start the capture."""
        ...
