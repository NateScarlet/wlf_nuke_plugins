# -*- coding=UTF-8 -*-
"""Test asset module.  """

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
from random import sample
from tempfile import mkdtemp
from unittest import TestCase, main, skip

import nuke

from wlf.path import Path


class FrameRangesTestCase(TestCase):
    def test_from_path(self):
        from asset import FrameRanges
        first = FrameRanges('test测试')
        self.assertEqual(str(first), '1-1')
        last = FrameRanges('test测试.%04d.exr')
        root = FrameRanges.from_root()
        self.assertEqual(str(last), str(root))
        last = FrameRanges(Path('test测试.%04d.exr'))
        self.assertEqual(str(last), str(root))

    def test_from_framerange(self):
        from asset import FrameRanges
        first = FrameRanges(nuke.FrameRange('1-80'))
        self.assertEqual(str(first), '1-80')

    def test_from_node(self):
        from asset import FrameRanges
        n = nuke.nodes.Read(file=b'test测试.###.png', first=5, last=80)
        first = FrameRanges(n)
        self.assertEqual(str(first), '5-80')
        n['first'].setValue(20)
        n['last'].setValue(60)
        self.assertEqual(str(first), '20-60')
        # Delete after evaluate.
        nuke.delete(n)
        self.assertEqual(str(first), '20-60')
        # Delete before evaluate.
        n = nuke.nodes.Read(file=b'test测试2.###.png', first=5, last=60)
        last = FrameRanges(n)
        nuke.delete(n)
        self.assertEqual(str(last), '1-100')  # Use root framerange.
        # Wrong frame ranges.
        n = nuke.nodes.Read(file=b'test测试2.###.png', first=60, last=7)
        last = FrameRanges(n)
        self.assertEqual(str(last), '7-60')  # Auto corrected framerange.
        nuke.delete(n)

    def test_dynamic_root(self):
        from asset import FrameRanges
        root = nuke.Root()
        root['first_frame'].setValue(1)
        root['last_frame'].setValue(100)
        from_root = FrameRanges.from_root()
        self.assertIsInstance(from_root._wrapped, nuke.Root)
        self.assertEqual(str(from_root), '1-100')
        # Change root frame range.
        root['first_frame'].setValue(8)
        root['last_frame'].setValue(80)
        self.assertEqual(str(from_root), '8-80')
        # Wrong frame range auto reverse.
        root['first_frame'].setValue(70)
        root['last_frame'].setValue(7)
        self.assertEqual(str(from_root), '7-70')
        # Clean up.
        root['first_frame'].setValue(1)
        root['last_frame'].setValue(100)
        self.assertEqual(str(from_root), '1-100')

    def test_node_file_changed(self):
        from asset import FrameRanges
        first_file = b'test测试.###.png'
        n = nuke.nodes.Read(file=first_file, first=5, last=80)
        first = FrameRanges(n)
        self.assertEqual(str(first), '5-80')
        n['file'].setValue(b'test测试2.%d.jpg')
        n['first'].setValue(22)
        # Use cached if filename changed.
        self.assertEqual(str(first), '5-80')
        # Use node if filename changed back.
        n['file'].setValue(first_file)
        n['first'].setValue(9)
        self.assertEqual(str(first), '9-80')
        nuke.delete(n)

    def test_reversed(self):
        from asset import FrameRanges
        first = FrameRanges('200-100')
        self.assertEqual(first.toFrameList(), range(200, 99, -1))
        n = nuke.nodes.Read(file=b'测试wfjm.###.exr', first=200, last=100)
        last = FrameRanges(n)
        self.assertEqual(last.toFrameList(), range(100, 201))
        nuke.delete(n)

    def test_to_frame_list(self):
        from asset import FrameRanges
        empty = nuke.FrameRanges([])
        self.assertIs(empty.toFrameList(), None)
        self.assertIsInstance(FrameRanges(empty).to_frame_list(), list)

    def test_bool(self):
        from asset import FrameRanges
        empty = nuke.FrameRanges([])
        self.assertFalse(FrameRanges(empty))
        self.assert_(FrameRanges())


class AssetTestCase(TestCase):
    def _pop(self):
        from asset import Asset
        return Asset('test测试')

    def test_nest(self):
        from asset import Asset
        first = self._pop()
        self.assertIs(first, Asset(first))

    def test_cache(self):
        first = self._pop()
        self.assertIs(first, self._pop())

    def test_auto_framerange(self):
        from asset import Asset
        first = Asset('test测试')
        self.assertEqual(str(first.frame_ranges), '1-1')
        last = Asset('test测试.%04d.exr')
        self.assertEqual(str(last.frame_ranges), '1-100')

    def test_expand_range(self):
        from asset import Asset

        first = Asset('test测试.%d.exr')
        self.assertEqual(str(first.frame_ranges), '1-100')
        last = Asset('test测试.%d.exr', '50-200')
        self.assertIs(last, first)
        self.assertEqual(str(first.frame_ranges), '1-200')
        last = Asset('test测试.%d.exr', '300-400')
        self.assertEqual(str(first.frame_ranges), '1-200 300-400')

    def test_single_frame(self):
        from asset import Asset

        first = Asset('test测试.exr')
        self.assertEqual(str(first.frame_ranges), '1-1')
        last = Asset('test测试.exr', '50-200')
        self.assertEqual(str(last.frame_ranges), '1-1')

    def test_from_node(self):
        from asset import Asset
        # Single frame.
        n = nuke.nodes.Read(file=b'test测试文件.exr', first=1, last=188)
        first = Asset(n)
        self.assert_(str(first.frame_ranges), '1-1')
        nuke.delete(n)
        # Multiple frame.
        n = nuke.nodes.Read(file=b'test测试文件.%d.exr', first=2, last=288)
        last = Asset(n)
        self.assert_(str(last.frame_ranges), '2-288')
        n['first'].setValue(3)
        self.assert_(str(last.frame_ranges), '3-288')
        nuke.delete(n)


class AssetsTestCase(TestCase):

    def setUp(self):
        self.nodes = [
            nuke.nodes.Read(file='test_file1.%04d.exr', first=1, last=100),
            nuke.nodes.Read(file='test_file2.%04d.exr', first=1, last=40),
            nuke.nodes.Read(file='test_file2.%04d.exr', first=50, last=100),
            nuke.nodes.Read(file='test_file3.%d.exr', first=50, last=100),
            nuke.nodes.Read(file='test_file4.###.exr', first=50, last=100),
            nuke.nodes.Read(file=b'test_file5中文.###.exr', first=50, last=100),
            nuke.nodes.Read(file='test_file6.###.exr', first=500, last=100)]
        self.expected_dict = {
            'test_file1.%04d.exr': '1-100',
            'test_file2.%04d.exr': '1-40 50-100',
            'test_file3.%d.exr': '50-100',
            'test_file4.###.exr': '50-100',
            'test_file5中文.###.exr': '50-100',
            'test_file6.###.exr': '100-500',
        }

    def test_all(self):
        from asset import Assets, MissingFramesDict
        first = Assets.all()
        self.assertEqual(len(nuke.allNodes('Read')), len(self.nodes))
        self.assertEqual(len(first), 6)
        dict_ = first.missing_frames_dict()
        self.assertEqual(unicode(dict_),
                         unicode(MissingFramesDict(self.expected_dict)))

    def tearDown(self):
        for n in self.nodes:
            nuke.delete(n)


class AssetMissingFrameTestCase(TestCase):
    def setUp(self):
        self.temp_dir = mkdtemp()
        self.addCleanup(os.removedirs, self.temp_dir)
        self.test_file = os.path.join(self.temp_dir, 'test_seq.%04d.exr')
        self.expected_missing_frames = nuke.FrameRanges(
            sample(xrange(1, 91), 10) + list(xrange(91, 101)))
        self.expected_missing_frames.compact()

        # Create temp file.
        path = Path(Path(self.temp_dir) / 'test_seq.%04d.exr')
        for i in set(xrange(1, 91)).difference(self.expected_missing_frames.toFrameList()):
            j = Path(path.with_frame(i))
            with j.open('w') as f:
                f.write(unicode(i))
            self.addCleanup(j.unlink)

    def _test_missing_frame(self, filename):
        from asset import Asset, CachedMissingFrames
        asset_ = Asset(filename)

        def _pop():
            ret = asset_.missing_frames()
            self.assertEqual(ret.toFrameList(),
                             self.expected_missing_frames.toFrameList())
            self.assertEqual(str(asset_.missing_frames('91-120')), '91-100')
            return ret

        _pop()

        # test cache
        cached = asset_._missing_frames
        self.assertIsInstance(cached, CachedMissingFrames)
        _pop()
        self.assertIs(cached, asset_._missing_frames)
        asset_.update_interval = -1
        _pop()
        self.assertIsNot(cached, asset_._missing_frames)

    def test_missing_frame_dry(self):
        self._test_missing_frame(self.test_file)

    def test_missing_frame_with_node(self):
        n = nuke.nodes.Read(file=self.test_file.replace('\\', '/'),
                            first=1,
                            last=100)
        self._test_missing_frame(n)
        nuke.delete(n)

    def test_get_missing_frames(self):
        from asset import Assets, MissingFramesDict
        result = Assets.all().missing_frames_dict()
        self.assertIsInstance(result, MissingFramesDict)
        self.assertIsInstance(result.as_html(), unicode)

    def test_warn_missing_frames(self):
        from asset import warn_missing_frames
        warn_missing_frames(show_ok=True)


if __name__ == '__main__':
    main()
