"""
This type stub file was generated by pyright.
"""

onUserCreates = {  }
def addOnUserCreate(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute when user creates a node"""
  ...

def removeOnUserCreate(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def onUserCreate():
  ...

onCreates = {  }
def addOnCreate(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute when a node is created or undeleted"""
  ...

def removeOnCreate(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def onCreate():
  ...

onScriptLoads = {  }
def addOnScriptLoad(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute when a script is loaded"""
  ...

def removeOnScriptLoad(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def onScriptLoad():
  ...

onScriptSaves = {  }
def addOnScriptSave(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute before a script is saved"""
  ...

def removeOnScriptSave(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def onScriptSave():
  ...

onScriptCloses = {  }
def addOnScriptClose(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute before a script is closed"""
  ...

def removeOnScriptClose(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def onScriptClose():
  ...

onDestroys = {  }
def addOnDestroy(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute when a node is destroyed"""
  ...

def removeOnDestroy(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def onDestroy():
  ...

knobChangeds = {  }
def addKnobChanged(call, args=..., kwargs=..., nodeClass=..., node=...):
  """Add code to execute when the user changes a knob
  The knob is availble in nuke.thisKnob() and the node in nuke.thisNode().
  This is also called with dummy knobs when the control panel is opened
  or when the inputs to the node changes. The purpose is to update other
  knobs in the control panel. Use addUpdateUI() for changes that
  should happen even when the panel is closed."""
  ...

def removeKnobChanged(call, args=..., kwargs=..., nodeClass=..., node=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def knobChanged():
  ...

updateUIs = {  }
def addUpdateUI(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute on every node when things change. This is done
  during idle, you cannot rely on it being done before it starts updating
  the viewer"""
  ...

def removeUpdateUI(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def updateUI():
  ...

autolabels = {  }
def addAutolabel(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute on every node to produce the text to draw on it
  in the DAG. Any value other than None is converted to a string and used
  as the text. None indicates that previously-added functions should
  be tried"""
  ...

def removeAutolabel(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def autolabel():
  ...

beforeRenders = {  }
def addBeforeRender(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute before starting any renders"""
  ...

def removeBeforeRender(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def beforeRender():
  ...

beforeFrameRenders = {  }
def addBeforeFrameRender(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute before each frame of a render"""
  ...

def removeBeforeFrameRender(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def beforeFrameRender():
  ...

afterFrameRenders = {  }
def addAfterFrameRender(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute after each frame of a render"""
  ...

def removeAfterFrameRender(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def afterFrameRender():
  ...

afterRenders = {  }
def addAfterRender(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute after any renders"""
  ...

def removeAfterRender(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def afterRender():
  ...

renderProgresses = {  }
def addRenderProgress(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute when the progress bar updates during any renders"""
  ...

def removeRenderProgress(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def renderProgress():
  ...

_beforeRecordings = {  }
def addBeforeRecording(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute before viewer recording"""
  ...

def removeBeforeRecording(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def beforeRecording():
  ...

_afterRecordings = {  }
def addAfterRecording(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute after viewer recording"""
  ...

def removeAfterRecording(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def afterRecording():
  ...

_beforeReplays = {  }
def addBeforeReplay(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute before viewer replay"""
  ...

def removeBeforeReplay(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def beforeReplay():
  ...

_afterReplays = {  }
def addAfterReplay(call, args=..., kwargs=..., nodeClass=...):
  """Add code to execute after viewer replay"""
  ...

def removeAfterReplay(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def afterReplay():
  ...

beforeBackgroundRenders = []
def addBeforeBackgroundRender(call, args=..., kwargs=...):
  """Add code to execute before starting any background renders.
  The call must be in the form of:
  def foo(context):
    pass

  The context object that will be passed in is a dictionary containing the following elements:
  id => The identifier for the task that's about to begin

  Please be aware that the current Nuke context will not make sense in the callback (e.g. nuke.thisNode will return a random node).
  """
  ...

def removeBeforeBackgroundRender(call, args=..., kwargs=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def beforeBackgroundRender(context):
  ...

afterBackgroundFrameRenders = []
def addAfterBackgroundFrameRender(call, args=..., kwargs=...):
  """Add code to execute after each frame of a background render.
  The call must be in the form of:
  def foo(context):
    pass

  The context object that will be passed in is a dictionary containing the following elements:
  id => The identifier for the task that's making progress
  frame => the current frame number being rendered
  numFrames => the total number of frames that is being rendered
  frameProgress => the number of frames rendered so far.

  Please be aware that the current Nuke context will not make sense in the callback (e.g. nuke.thisNode will return a random node).
  """
  ...

def removeAfterBackgroundFrameRender(call, args=..., kwargs=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def afterBackgroundFrameRender(context):
  ...

afterBackgroundRenders = []
def addAfterBackgroundRender(call, args=..., kwargs=...):
  """Add code to execute after any background renders.
  The call must be in the form of:
  def foo(context):
    pass

  The context object that will be passed in is a dictionary containing the following elements:
  id => The identifier for the task that's ended

  Please be aware that the current Nuke context will not make sense in the callback (e.g. nuke.thisNode will return a random node).
  """
  ...

def removeAfterBackgroundRender(call, args=..., kwargs=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def afterBackgroundRender(context):
  ...

filenameFilters = {  }
def addFilenameFilter(call, args=..., kwargs=..., nodeClass=...):
  """Add a function to modify filenames before Nuke passes them to
  the operating system. The first argument to the function is the
  filename, and it should return the new filename. None is the same as
  returning the string unchanged. All added functions are called
  in backwards order."""
  ...

def removeFilenameFilter(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback with the same arguments."""
  ...

def filenameFilter(filename):
  ...

validateFilenames = {  }
def addValidateFilename(call, args=..., kwargs=..., nodeClass=...):
  """Add a function to validate a filename in Write nodes. The first argument
  is the filename and it should return a Boolean as to whether the filename is valid
  or not. If a callback is provided, it will control whether the Render button of Write nodes
  and the Execute button of WriteGeo nodes is enabled or not."""
  ...

def removeFilenameValidate(call, args=..., kwargs=..., nodeClass=...):
  """Remove a previously-added callback."""
  ...

def validateFilename(filename):
  ...

autoSaveFilters = {  }
def addAutoSaveFilter(filter):
  """addAutoSaveFilter(filter) -> None

  Add a function to modify the autosave filename before Nuke saves the current script on an autosave timeout.

  Look at rollingAutoSave.py in the nukescripts directory for an example of using the auto save filters.

  @param filter: A filter function.  The first argument to the filter is the current autosave filename.
  The filter should return the filename to save the autosave to."""
  ...

def removeAutoSaveFilter(filter):
  """Remove a previously-added callback with the same arguments."""
  ...

def autoSaveFilter(filename):
  """Internal function.  Use addAutoSaveFilter to add a callback"""
  ...

autoSaveRestoreFilters = {  }
def addAutoSaveRestoreFilter(filter):
  """addAutoSaveRestoreFilter(filter) -> None

  Add a function to modify the autosave restore file before Nuke attempts to restores the autosave file.

  Look at rollingAutoSave.py in the nukescripts directory for an example of using the auto save filters.

  @param filter: A filter function.  The first argument to the filter is the current autosave filename.
  This function should return the filename to load autosave from or it should return None if the autosave file should be ignored."""
  ...

def removeAutoSaveRestoreFilter(filter):
  """Remove a previously-added callback with the same arguments."""
  ...

def autoSaveRestoreFilter(filename):
  """Internal function.  Use addAutoSaveRestoreFilter to add a callback"""
  ...

autoSaveDeleteFilters = {  }
def addAutoSaveDeleteFilter(filter):
  """addAutoSaveDeleteFilter(filter) -> None

  Add a function to modify the autosave filename before Nuke attempts delete the autosave file.

  Look at rollingAutoSave.py in the nukescripts directory for an example of using the auto save filters.

  @param filter: A filter function.  The first argument to the filter is the current autosave filename.
  This function should return the filename to delete or return None if no file should be deleted."""
  ...

def removeAutoSaveDeleteFilter(filter):
  """Remove a previously-added callback with the same arguments."""
  ...

def autoSaveDeleteFilter(filename):
  """Internal function.  Use addAutoSaveDeleteFilter to add a callback"""
  ...
