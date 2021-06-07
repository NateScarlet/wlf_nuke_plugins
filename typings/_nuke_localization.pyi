# -*- coding=UTF-8 -*-
# This typing file was generated by typing_from_help.py
"""
_nuke_localization - Internal module for Nuke's localization functionality.
"""

import six
import typing

def alwaysUseSourceFiles() -> bool:
    """
    Check if Nuke is currently set to read source files instead of localized copies
    @return: True if source files are always read
    """
    ...

def clearUnusedFiles() -> None:
    """
    Clears unused files in the localisation folder
    """
    ...

def forceUpdateAll() -> None:
    """
    Update all localized files currently in use in Nuke
    """
    ...

def forceUpdateSelectedNodes() -> None:
    """
    Update all localized files used by nodes that are currently selected
    """
    ...

def isLocalizationPaused() -> bool:
    """
    @return: whether localization was paused
    """
    ...

def pauseLocalization() -> None:
    """
    Pause the localization background thread if it was running
    """
    ...

def resumeLocalization() -> None:
    """
    Resume the localization background thread if it was paused
    """
    ...

def setAlwaysUseSourceFiles(v: bool) -> None:
    """
    Set whether Nuke should always read source files instead of localized copies
    """
    ...

__all__: ...
"""
['__doc__', '__name__', '__package__', 'alwaysUseSourceFiles...
"""
