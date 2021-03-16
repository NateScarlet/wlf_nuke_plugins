# -*- coding=UTF-8 -*-
"""Match drop frame from a node.  """

import typing

import nuke


def get_timewarp_data(n: nuke.Node, start: int, end: int, tolerance: float = ...) -> typing.List[int]:
    ...


def create_timewarp(data: typing.List[int], start: int) -> nuke.Node:
    ...


def show_dialog() -> typing.Optional[nuke.Node]:
    ...