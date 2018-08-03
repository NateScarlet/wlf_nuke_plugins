# -*- coding=UTF-8 -*-
"""Patch nukescript precomp functions.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import nuke
import nukescripts  # pylint: disable=import-error

from wlf.codectools import get_unicode as u
from wlf.path import PurePath

UNPATCH_FUNC_STACK = []


def patch_precomp_dialog():
    """Enhance precomp creation.  """

    orig = nukescripts.PrecompOptionsDialog.__init__

    def _func(self):

        orig(self)

        self.precompName = nuke.String_Knob(
            'precomp_name'.encode('utf-8'),
            '预合成名称'.encode('utf-8'),
            'precomp1'.encode('utf-8'))
        self.addKnob(self.precompName)

        self.scriptPath.setLabel('脚本路径'.encode('utf-8'))
        self.renderPath.setLabel('渲染路径'.encode('utf-8'))
        self.channels.setLabel('输出通道'.encode('utf-8'))
        self.origNodes.setLabel('原节点'.encode('utf-8'))

        _knob_changed(self, self.precompName)
        nuke.addKnobChanged(lambda self: _knob_changed(self, nuke.thisKnob()),
                            args=self,
                            nodeClass='PanelNode',
                            node=self._PythonPanel__node)  # pylint: disable=protected-access

    def _knob_changed(self, knob):
        if knob is not self.precompName:
            return

        rootpath = PurePath(u(nuke.value('root.name')))
        name = u(knob.value()) or 'precomp1'
        self.scriptPath.setValue(
            (
                rootpath.parent /
                ''.join([rootpath.stem]
                        + ['.{}'.format(name)]
                        + rootpath.suffixes)
            ).as_posix().encode('utf-8'))
        self.renderPath.setValue(
            'precomp/{0}/{0}.%04d.exr'.format(
                ''.join([rootpath.stem]
                        + ['.{}'.format(name)]
                        + [i for i in rootpath.suffixes if i != '.nk'])
            ).encode('utf-8'))

    nukescripts.PrecompOptionsDialog.__init__ = _func
    UNPATCH_FUNC_STACK.append(lambda: setattr(
        nukescripts.PrecompOptionsDialog, '__init__', orig))


def enable():
    """Enable patch. """
    patch_precomp_dialog()


def disable():
    """Disable patch. """

    while True:
        try:
            UNPATCH_FUNC_STACK.pop()()
        except IndexError:
            return
