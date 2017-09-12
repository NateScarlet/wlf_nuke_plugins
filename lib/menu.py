# -*- coding: UTF-8 -*-
"""Nuke menu file."""
import sys

import _ui
import callback
import pref
from wlf import cgtwq

try:
    __import__('validation')
except ImportError:
    import os
    __import__('nuke').message('Plugin\n {} crushed.'.format(
        os.path.normpath(os.path.join(__file__, '../../'))))
    sys.exit(1)

print(u'添加菜单')
_ui.add_menu()
print(u'添加面板')
_ui.add_panel()
print(u'增强节点标签')
_ui.add_autolabel()
print(u'添加首选项')
pref.add_preferences()
print(u'设置knob默认值')
pref.set_knob_default()
callback.menu()

if cgtwq.MODULE_ENABLE:
    print(u'更新CGTeamWork状态')
    cgtwq.CGTeamWork.update_status()
