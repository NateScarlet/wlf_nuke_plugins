"""
This type stub file was generated by pyright.
"""

import nuke

profileCategories = { "ProfileStore": nuke.PROFILE_STORE,"ProfileValidate": nuke.PROFILE_VALIDATE,"ProfileRequest": nuke.PROFILE_REQUEST,"ProfileEngine": nuke.PROFILE_ENGINE }
class NukeProfiler:
  def __init__(self) -> None:
    ...
  
  def setPathToFile(self, filename):
    ...
  
  def indentString(self):
    ...
  
  def OpenTag(self, tagName, optionsDict=..., closeTag=...):
    ...
  
  def CloseTag(self, tagName):
    ...
  
  def WriteDictInner(self, dictToWrite):
    ...
  
  def NodeProfile(self, nukeNode, maxEngineVal):
    ...
  
  def initProfileDesc(self):
    ...
  
  def writeXMLInfo(self):
    ...
  
  def resetTimersAndStartProfile(self):
    ...
  
  def writeProfileDesc(self):
    ...
  
  def addFrameProfileAndResetTimers(self):
    ...
  
  def endProfile(self):
    ...
  

