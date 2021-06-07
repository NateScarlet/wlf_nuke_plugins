"""
This type stub file was generated by pyright.
"""

class pyAppHelper(object):
    """Helper class to run python commands in a separate thread."""

    def __init__(self, start=...) -> None:
        """constructor"""
        ...
    def run(self, call, args=..., kwargs=...):
        """Runs the specified call in a separate thread."""
        ...
    def initiate(self):
        """Start the thread associated with this object"""
        ...
    def terminate(self):
        """Terminated the thread associated with this object"""
        ...
