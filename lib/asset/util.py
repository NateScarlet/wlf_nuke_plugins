# -*- coding=UTF-8 -*-
"""Asset utility.  """

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import cache, localization, notify


def setup():
    localization.setup()
    notify.setup()
    cache.setup()
