"""
This type stub file was generated by pyright.
"""

import ctypes
import fnmatch
import functools
import io
import ntpath
import os
import posixpath
import re
import typing
import six
import sys
import nt
from __future__ import unicode_literals
from errno import EACCES, EBADF, EEXIST, EINVAL, ENOENT, ENOTDIR, EPERM
from operator import attrgetter
from stat import S_ISBLK, S_ISCHR, S_ISDIR, S_ISFIFO, S_ISLNK, S_ISREG, S_ISSOCK

"""
This type stub file was generated by pyright.
"""
supports_symlinks = ...
if os.name == "nt": ...
else: ...
_IGNORED_ERROS = ...
_IGNORED_WINERRORS = ...

class _Flavour(object):
    """A flavour implements a particular (platform-specific) set of path
    semantics."""

    def __init__(self) -> None: ...
    def parse_parts(self, parts): ...
    def join_parsed_parts(self, drv, root, parts, drv2, root2, parts2):
        """
        Join the two paths represented by the respective
        (drive, root, parts) tuples.  Return a new (drive, root, parts) tuple.
        """
        ...

class _WindowsFlavour(_Flavour):
    sep = ...
    altsep = ...
    has_drv = ...
    pathmod = ...
    is_supported = ...
    drive_letters = ...
    ext_namespace_prefix = ...
    reserved_names = ...
    def splitroot(self, part, sep=...): ...
    def casefold(self, s): ...
    def casefold_parts(self, parts): ...
    def resolve(self, path, strict=...): ...
    def is_reserved(self, parts): ...
    def make_uri(self, path: six.text_type): ...
    def gethomedir(self, username: six.text_type): ...

class _PosixFlavour(_Flavour):
    sep = ...
    altsep = ...
    has_drv = ...
    pathmod = ...
    is_supported = ...
    def splitroot(self, part, sep=...): ...
    def casefold(self, s): ...
    def casefold_parts(self, parts): ...
    def resolve(self, path, strict=...): ...
    def is_reserved(self, parts): ...
    def make_uri(self, path): ...
    def gethomedir(self, username): ...

_windows_flavour = ...
_posix_flavour = ...

class _Accessor:
    """An accessor implements a particular (system-specific or not) way of
    accessing paths on the filesystem."""

    ...

class _NormalAccessor(_Accessor):
    stat = ...
    lstat = ...
    open = ...
    listdir = ...
    scandir = ...
    chmod = ...
    if hasattr(os, "lchmod"):
        lchmod = ...
    else:
        def lchmod(self, pathobj, mode): ...
    mkdir = ...
    unlink = ...
    rmdir = ...
    rename = ...
    if sys.version_info >= (3, 3):
        replace = ...
    if nt: ...
    else:
        @staticmethod
        def symlink(a, b, target_is_directory): ...
    utime = ...
    def readlink(self, path): ...

_normal_accessor = ...
if hasattr(functools, "lru_cache"):
    _make_selector = ...

class _Selector:
    """A selector matches a specific glob pattern part against the children
    of a given path."""

    def __init__(self, child_parts) -> None: ...
    def select_from(self, parent_path):
        """Iterate over all child paths of `parent_path` matched by this
        selector.  This can contain parent_path itself."""
        ...

class _TerminatingSelector: ...

class _PreciseSelector(_Selector):
    def __init__(self, name, child_parts) -> None: ...

class _WildcardSelector(_Selector):
    def __init__(self, pat, child_parts) -> None: ...

class _RecursiveWildcardSelector(_Selector):
    def __init__(self, pat, child_parts) -> None: ...

class _PathParents(Sequence):
    """This object provides sequence-like access to the logical ancestors
    of a path.  Don't try to construct it yourself."""

    __slots__ = ...
    def __init__(self, path) -> None: ...
    def __len__(self): ...
    def __getitem__(self, idx): ...
    def __repr__(self): ...

@six.python_2_unicode_compatible
class PurePath(object):
    """PurePath represents a filesystem path and offers operations which
    don't imply any actual filesystem I/O.  Depending on your system,
    instantiating a PurePath will return either a PurePosixPath or a
    PureWindowsPath object.  You can also instantiate either of these classes
    directly, regardless of your system.
    """

    __slots__ = ...
    def __new__(cls, *args: typing.Union[six.text_type, PurePath]):
        """Construct a PurePath from one or several strings and or existing
        PurePath objects.  The strings and path objects are combined so as
        to yield a canonicalized path, which is incorporated into the
        new PurePath object.
        """
        ...
    def __reduce__(self): ...
    def __str__(self) -> six.text_type:
        """Return the string representation of the path, suitable for
        passing to system calls."""
        ...
    def __fspath__(self): ...
    def as_posix(self):
        """Return the string representation of the path with forward (/)
        slashes."""
        ...
    def __bytes__(self):
        """Return the bytes representation of the path.  This is only
        recommended to use under Unix."""
        ...
    def __repr__(self): ...
    def as_uri(self):
        """Return the path as a 'file' URI."""
        ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __lt__(self, other) -> bool: ...
    def __le__(self, other) -> bool: ...
    def __gt__(self, other) -> bool: ...
    def __ge__(self, other) -> bool: ...
    drive = ...
    root = ...
    @property
    def anchor(self):
        """The concatenation of the drive and root, or ''."""
        ...
    @property
    def name(self):
        """The final path component, if any."""
        ...
    @property
    def suffix(self):
        """The final component's last suffix, if any."""
        ...
    @property
    def suffixes(self):
        """A list of the final component's suffixes, if any."""
        ...
    @property
    def stem(self):
        """The final path component, minus its last suffix."""
        ...
    def with_name(self, name):
        """Return a new path with the file name changed."""
        ...
    def with_suffix(self, suffix):
        """Return a new path with the file suffix changed.  If the path
        has no suffix, add given suffix.  If the given suffix is an empty
        string, remove the suffix from the path.
        """
        ...
    def relative_to(self, *other):
        """Return the relative path to another path identified by the passed
        arguments.  If the operation is not possible (because this is not
        a subpath of the other path), raise ValueError.
        """
        ...
    @property
    def parts(self):
        """An object providing sequence-like access to the
        components in the filesystem path."""
        ...
    def joinpath(self, *args):
        """Combine this path with one or several arguments, and return a
        new path representing either a subpath (if all arguments are relative
        paths) or a totally different path (if one of the arguments is
        anchored).
        """
        ...
    def __truediv__(self, key): ...
    def __rtruediv__(self, key): ...
    if six.PY2:
        __div__ = ...
        __rdiv__ = ...
    @property
    def parent(self) -> PurePath: ...
    @property
    def parents(self):
        """A sequence of this path's logical parents."""
        ...
    def is_absolute(self):
        """True if the path is absolute (has both a root and, if applicable,
        a drive)."""
        ...
    def is_reserved(self):
        """Return True if the path contains one of the special names reserved
        by the system, if any."""
        ...
    def match(self, path_pattern):
        """
        Return True if this path matches the given pattern.
        """
        ...

if sys.version_info >= (3, 6): ...

class PurePosixPath(PurePath):
    _flavour = ...
    __slots__ = ...

class PureWindowsPath(PurePath):
    """PurePath subclass for Windows systems.

    On a Windows system, instantiating a PurePath should return this object.
    However, you can also instantiate it directly on any system.
    """

    _flavour = ...
    __slots__ = ...

class Path(PurePath):
    """PurePath subclass that can make system calls.

    Path represents a filesystem path but unlike PurePath, also offers
    methods to do system calls on path objects. Depending on your system,
    instantiating a Path will return either a PosixPath or a WindowsPath
    object. You can also instantiate a PosixPath or WindowsPath directly,
    but cannot instantiate a WindowsPath on a POSIX system or vice versa.
    """

    __slots__ = ...
    def __new__(cls, *args: typing.Union[six.text_type, PurePath], **kwargs): ...
    def __enter__(self): ...
    def __exit__(self, t, v, tb): ...
    @classmethod
    def cwd(cls):
        """Return a new path pointing to the current working directory
        (as returned by os.getcwd()).
        """
        ...
    @classmethod
    def home(cls):
        """Return a new path pointing to the user's home directory (as
        returned by os.path.expanduser('~')).
        """
        ...
    @property
    def parent(self) -> Path: ...
    def samefile(self, other_path):
        """Return whether other_path is the same or not as this file
        (as returned by os.path.samefile()).
        """
        ...
    def iterdir(self):
        """Iterate over the files in this directory.  Does not yield any
        result for the special paths '.' and '..'.
        """
        ...
    def glob(self, pattern):
        """Iterate over this subtree and yield all existing files (of any
        kind, including directories) matching the given relative pattern.
        """
        ...
    def rglob(self, pattern):
        """Recursively yield all existing files (of any kind, including
        directories) matching the given relative pattern, anywhere in
        this subtree.
        """
        ...
    def absolute(self):
        """Return an absolute version of this path.  This function works
        even if the path doesn't point to anything.

        No normalization is done, i.e. all '.' and '..' will be kept along.
        Use resolve() to get the canonical path to a file.
        """
        ...
    def resolve(self, strict=...):
        """
        Make the path absolute, resolving all symlinks on the way and also
        normalizing it (for example turning slashes into backslashes under
        Windows).
        """
        ...
    def stat(self):
        """
        Return the result of the stat() system call on this path, like
        os.stat() does.
        """
        ...
    def owner(self):
        """
        Return the login name of the file owner.
        """
        ...
    def group(self):
        """
        Return the group name of the file gid.
        """
        ...
    def open(self, mode=..., buffering=..., encoding=..., errors=..., newline=...):
        """
        Open the file pointed by this path and return a file object, as
        the built-in open() function does.
        """
        ...
    def read_bytes(self):
        """
        Open the file in bytes mode, read it, and close the file.
        """
        ...
    def read_text(self, encoding=..., errors=...):
        """
        Open the file in text mode, read it, and close the file.
        """
        ...
    def write_bytes(self, data):
        """
        Open the file in bytes mode, write to it, and close the file.
        """
        ...
    def write_text(self, data, encoding=..., errors=...):
        """
        Open the file in text mode, write to it, and close the file.
        """
        ...
    def touch(self, mode=..., exist_ok=...):
        """
        Create this file with the given access mode, if it doesn't exist.
        """
        ...
    def mkdir(self, mode: int = ..., parents: bool = ..., exist_ok: bool = ...) -> None:
        """
        Create a new directory at this given path.
        """
        ...
    def chmod(self, mode):
        """
        Change the permissions of the path, like os.chmod().
        """
        ...
    def lchmod(self, mode):
        """
        Like chmod(), except if the path points to a symlink, the symlink's
        permissions are changed, rather than its target's.
        """
        ...
    def unlink(self):
        """
        Remove this file or link.
        If the path is a directory, use rmdir() instead.
        """
        ...
    def rmdir(self):
        """
        Remove this directory.  The directory must be empty.
        """
        ...
    def lstat(self):
        """
        Like stat(), except if the path points to a symlink, the symlink's
        status information is returned, rather than its target's.
        """
        ...
    def rename(self, target):
        """
        Rename this path to the given path.
        """
        ...
    def replace(self, target):
        """
        Rename this path to the given path, clobbering the existing
        destination if it exists.
        """
        ...
    def symlink_to(self, target, target_is_directory=...):
        """
        Make this path a symlink pointing to the given path.
        Note the order of arguments (self, target) is the reverse of
        os.symlink's.
        """
        ...
    def exists(self):
        """
        Whether this path exists.
        """
        ...
    def is_dir(self):
        """
        Whether this path is a directory.
        """
        ...
    def is_file(self):
        """
        Whether this path is a regular file (also True for symlinks pointing
        to regular files).
        """
        ...
    def is_mount(self):
        """
        Check if this path is a POSIX mount point
        """
        ...
    def is_symlink(self):
        """
        Whether this path is a symbolic link.
        """
        ...
    def is_block_device(self):
        """
        Whether this path is a block device.
        """
        ...
    def is_char_device(self):
        """
        Whether this path is a character device.
        """
        ...
    def is_fifo(self):
        """
        Whether this path is a FIFO.
        """
        ...
    def is_socket(self):
        """
        Whether this path is a socket.
        """
        ...
    def expanduser(self):
        """Return a new path with expanded ~ and ~user constructs
        (as returned by os.path.expanduser)
        """
        ...

class PosixPath(Path, PurePosixPath):
    """Path subclass for non-Windows systems.

    On a POSIX system, instantiating a Path should return this object.
    """

    __slots__ = ...

class WindowsPath(Path, PureWindowsPath):
    """Path subclass for Windows systems.

    On a Windows system, instantiating a Path should return this object.
    """

    __slots__ = ...
    def owner(self): ...
    def group(self): ...
    def is_mount(self): ...
