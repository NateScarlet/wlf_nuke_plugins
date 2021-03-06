"""
This type stub file was generated by pyright.
"""

def cache_clear(args=...):
    """
    Clears the buffer memory cache by calling nuke.memory("free")
    If args are supplied they are passed to nuke.memory as well
    eg. nuke.memory( "free", args )
    """
    ...

def cache_report(args=...):
    """
    Gets info on memory by calling nuke.memory("info")
    If args are supplied they are passed to nuke.memory as well
    eg. nuke.memory( "info", args )
    """
    ...

def clearAllCaches():
    """
    Clears all caches. The disk cache, viewer playback cache and memory buffers.
    """
    ...
