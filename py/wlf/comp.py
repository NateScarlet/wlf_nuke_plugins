# -*- coding=UTF-8 -*-
"""Comp footages to a .nk file."""

import json
import locale
import os
import pprint
import re
import sys
import threading
import time
import traceback
from subprocess import PIPE, Popen

import nuke
import nukescripts

FPS = 25
FORMAT = 'HD_1080'
__version__ = 1.1

SYS_CODEC = locale.getdefaultlocale()[1]
SCRIPT_CODEC = 'UTF-8'
reload(sys)
sys.setdefaultencoding('UTF-8')


class Comp(object):
    """Create .nk file from footage that taged in filename."""

    default_config = {
        'footage_pat': r'^.+_sc.+_.+\..+$',
        'dir_pat': r'^.{8,}$',
        'tag_pat': r'sc.+?_([^.]+)',
        'output_dir': 'E:/precomp',
        'input_dir': 'Z:/SNJYW/Render/EP',
        'mp': r"\\192.168.1.4\f\QQFC_2015\Render\mp\Brooklyn-Bridge-Panorama.tga",
        'autograde': True,
        'exclude_existed': True,
    }
    default_tag = '_OTHER',
    tag_knob_name = u'wlf_tag'
    with open(os.path.join(__file__, '../comp.tags.json')) as f:
        tags = json.load(f)
        regular_tags = tags['regular_tags']
        tag_convert_dict = tags['tag_convert_dict']
        del tags

    def __init__(self, config=None, multiple=False):
        if not config:
            config = {}
        self._config = dict(self.default_config)
        self._config.update(config)
        self._errors = []

        for key, value in self._config.iteritems():
            if isinstance(value, str):
                self._config[key] = value.replace(u'\\', '/')

        if multiple:
            self.comp_shots()
        else:
            self.comp_shot(config)

    def comp_shots(self):
        """Comp multipe shots from footage folder that stored in config json file."""

        _shot_list = self.get_shot_list(self._config)

        for i, shot in enumerate(_shot_list):
            _savepath = '{}.nk'.format(os.path.join(
                self._config['output_dir'], shot))
            print(_savepath)
            self._config['footage_dir'] = os.path.join(
                self._config['input_dir'], shot)

            print(u'\n## [{1}/{2}]:\t\t{0}'.format(shot,
                                                   i + 1, len(_shot_list)))

            self.comp_shot()
            self.output()

    def comp_shot(self, config=None):
        """Comp footages, import them if needed."""

        pprint.pprint(config)
        if config:
            print(u'\n# {}'.format(config['shot']))
            nuke.scriptClear()
            self.import_resource()
        self.setup_nodes()
        self.create_nodes()
        if config:
            self.output()
        print(u'{:-^50s}\n'.format(u'全部结束'))

    @staticmethod
    def get_shot_list(config):
        """Return shot_list generator from a config dict."""

        _dir = config['input_dir']
        if not os.path.isdir(_dir):
            return

        _ret = os.listdir(_dir)
        if isinstance(_ret[0], str):
            # _ret = map(lambda x: unicode(x, SYS_CODEC), _ret)
            _ret = (unicode(i, SYS_CODEC) for i in _ret)
        if config['exclude_existed']:
            # _ret = filter(lambda path: not os.path.exists(os.path.join(
            #     config[u'output_dir'], u'{}.nk'.format(path))), _ret)
            _ret = (i for i in _ret if os.path.exists(os.path.join(
                config[u'output_dir'], u'{}.nk'.format(i))))
        # _ret = filter(lambda path: re.match(config['dir_pat'], path), _ret)
        # _ret = filter(lambda dirname: os.path.isdir(
        #     os.path.join(_dir, dirname)), _ret)
        _ret = (i for i in _ret if (
            re.match(config['dir_pat'], i) and os.path.isdir(os.path.join(_dir, i))))

        if not _ret:
            _dir = _dir.rstrip('\\/')
            _dirname = os.path.basename(_dir)
            if re.match(config['dir_pat'], _dir):
                _ret = [_dir]
        return _ret

    @staticmethod
    def show_dialog():
        """Show a dialog for user using this class."""

        CompDialog().showModalDialog()

    def import_resource(self):
        """Import footages from config dictionary."""

        # Get all subdir
        dirs = list(x[0] for x in os.walk(self._config['footage_dir']))
        print(u'{:-^30s}'.format(u'开始 导入素材'))
        for dir_ in dirs:
            # Get footage in subdir
            print(u'文件夹 {}:'.format(dir_))
            if not re.match(self._config['dir_pat'], os.path.basename(dir_.rstrip('\\/'))):
                print(u'\t\t\t不匹配文件夹正则, 跳过\n')
                continue

            _footages = [i for i in nuke.getFileNameList(dir_) if (
                not i.endswith(('副本', '.lock')) and re.match(self._config['footage_pat'], i))]
            if _footages:
                for f in _footages:
                    nuke.createNode(u'Read', 'file {{{}/{}}}'.format(dir_, f))
                    print(u'\t' * 3 + f)
            print('')
        print(u'{:-^30s}'.format(u'结束 导入素材'))

        if not nuke.allNodes(u'Read'):
            raise FootageError(self._config['footage_dir'], u'没有素材')

    def setup_nodes(self):
        """Add tag knob to read nodes, then set project framerange."""

        _nodes = nuke.allNodes(u'Read')
        if not _nodes:
            raise FootageError(u'没有读取节点')

        n = None
        for n in _nodes:
            self._setup_node(n)
        if n:
            nuke.Root()['first_frame'].setValue(n['first'].value())
            nuke.Root()['last_frame'].setValue(n['last'].value())
            nuke.Root()['lock_range'].setValue(True)

    def create_nodes(self):
        """Create nodes that a comp need."""
        def _merge_mp(input_node, mp_file='', lut=''):
            def _add_lut(input_node):
                if not lut:
                    return input_node

                n = nuke.nodes.Vectorfield(
                    inputs=[input_node],
                    file_type='vf',
                    label='[basename [value this.knob.vfield_file]]')
                n['vfield_file'].fromUserText(lut)
                return n

            n = nuke.nodes.Read(file=mp_file)
            n['file'].fromUserText(mp_file)
            n.setName(u'MP')

            n = nuke.nodes.Reformat(inputs=[n], resize='fit')
            n = nuke.nodes.Transform(inputs=[n])
            n = _add_lut(n)
            n = nuke.nodes.ColorCorrect(inputs=[n])
            n = nuke.nodes.Grade(
                inputs=[n, nuke.nodes.Ramp(p0='1700 1000', p1='1700 500')])
            n = nuke.nodes.ProjectionMP(inputs=[n])
            n = nuke.nodes.SoftClip(
                inputs=[n], conversion='logarithmic compress')
            n = nuke.nodes.Defocus(inputs=[n], disable=True)
            n = nuke.nodes.Crop(inputs=[n], box='0 0 root.width root.height')
            n = nuke.nodes.Merge(inputs=[n, input_node], label='MP')

            return n

        n = self._bg_ch_nodes()
        print(u'{:-^30s}'.format('BG CH 节点创建'))

        n = self._merge_depth(n, self.get_nodes_by_tags(['BG', 'CH']))

        print(u'{:-^30s}'.format(u'整体深度节点创建'))
        self._add_zdefocus_control(n)
        print(u'{:-^30s}'.format(u'添加虚焦控制'))
        self._add_depthfog_control(n)
        print(u'{:-^30s}'.format(u'添加深度雾控制'))
        n = _merge_mp(
            n, mp_file=self._config['mp'], lut=self._config['mp_lut'])
        print(u'{:-^30s}'.format(u'MP节点创建'))

        n = nuke.nodes.wlf_Write(inputs=[n])
        n.setName(u'_Write')
        print(u'{:-^30s}'.format(u'输出节点创建'))
        _read_jpg = nuke.nodes.Read(
            file='[value _Write.Write_JPG_1.file]',
            label='输出的单帧',
            disable='{{! [file exist [value this.file]]}}',
            tile_color=0xbfbf00ff,
        )
        _read_jpg.setName('Read_Write_JPG')
        print(u'{:-^30s}'.format(u'读取输出节点创建'))

        map(nuke.delete, nuke.allNodes(u'Viewer'))
        nuke.nodes.Viewer(inputs=[n, n.input(0), n, _read_jpg])
        print(u'{:-^30s}'.format(u'设置查看器'))

        autoplace_all()

    @classmethod
    def get_nodes_by_tags(cls, tags):
        """Return nodes that match given tags."""

        ret = []
        if isinstance(tags, str):
            tags = [tags]
        tags = tuple(unicode(i).upper() for i in tags)

        for n in nuke.allNodes(u'Read'):
            knob_name = u'{}.{}'.format(n.name(), cls.tag_knob_name)
            if nuke.value(knob_name.encode(SCRIPT_CODEC), '').startswith(tags):
                ret.append(n)

        def _nodes_order(n):
            return (
                u'_' + n[cls.tag_knob_name].value()).replace(u'_BG', '1_').replace(u'_CH', '0_')
        ret.sort(key=_nodes_order, reverse=True)
        return ret

    def output(self):
        """Save .nk file and render .jpg file."""

        print(u'{:-^30s}'.format(u'开始 输出'))
        _path = self._config['save_path'].replace('\\', '/')
        _dir = os.path.dirname(_path)
        if not os.path.exists(_dir):
            os.makedirs(_dir)

        # Save nk
        print(u'保存为:\n\t\t\t{}\n'.format(_path))
        nuke.Root()['name'].setValue(_path)
        nuke.scriptSave(_path)

        # Render Single Frame
        write_node = nuke.toNode(u'_Write')
        if write_node:
            write_node = write_node.node(u'Write_JPG_1')
            frame = int(nuke.numvalue(u'_Write.knob.frame'))
            write_node['disable'].setValue(False)
            try:
                nuke.execute(write_node, frame, frame)
            except RuntimeError:
                # Try first frame.
                try:
                    nuke.execute(write_node, write_node.firstFrame(),
                                 write_node.firstFrame())
                except RuntimeError:
                    # Try last frame.
                    try:
                        nuke.execute(
                            write_node, write_node.lastFrame(), write_node.lastFrame())
                    except RuntimeError:
                        self._errors.append(
                            u'{}:\t渲染出错'.format(os.path.basename(_path)))
                        raise RenderError('Write_JPG_1')
        print(u'{:-^30s}'.format(u'结束 输出'))

    def _setup_node(self, n):
        def _add_knob(k):
            _knob_name = k.name()
            if nuke.exists('{}.{}'.format(n.name(), k.name())):
                k.setValue(n[_knob_name].value())
                n.removeKnob(n[_knob_name])
            n.addKnob(k)
        _tag = nuke.value(u'{}.{}'.format(n.name(), self.tag_knob_name), '')

        if not _tag:
            _tag = self._get_tag(nuke.filename(n))
            if not 'rgba.alpha' in n.channels():
                _tag = '_OTHER'

        k = nuke.Tab_Knob('吾立方')
        _add_knob(k)

        k = nuke.String_Knob(self.tag_knob_name, '素材标签')
        _add_knob(k)
        k.setValue(_tag)

        n.setName(_tag, updateExpressions=True)

    def _get_tag_from_pattern(self, str_):
        _tag_pat = re.compile(self.default_config['tag_pat'], flags=re.I)
        _ret = re.search(_tag_pat, str_)
        if _ret:
            _ret = _ret.group(1).upper()
        else:
            _ret = self.default_tag
        return _ret

    def _get_tag(self, filename):
        _ret = self._get_tag_from_pattern(os.path.basename(filename))

        if _ret not in self.regular_tags:
            _dir_result = self._get_tag_from_pattern(
                os.path.basename(os.path.dirname(filename)))
            if _dir_result != self.default_tag:
                _ret = _dir_result

        if _ret in self.tag_convert_dict:
            _ret = self.tag_convert_dict[_ret]

        return _ret

    def _bg_ch_nodes(self):
        bg_ch_nodes = self.get_nodes_by_tags(['BG', 'CH'])

        if not bg_ch_nodes:
            raise FootageError(u'BG', u'CH')

        for i, _read_node in enumerate(bg_ch_nodes):
            n = _read_node
            if 'SSS.alpha' in _read_node.channels():
                n = nuke.nodes.Keyer(
                    inputs=[n],
                    input='SSS',
                    output='SSS.alpha',
                    operation='luminance key',
                    range='0 0.007297795507 1 1'
                )
            n = nuke.nodes.Reformat(inputs=[n], resize='fit')
            if 'depth.Z' not in _read_node.channels():
                _constant = nuke.nodes.Constant(
                    channels='depth',
                    color=1,
                    label='**用渲染出的depth层替换这个**\n或者手动指定数值'
                )
                n = nuke.nodes.Merge2(
                    inputs=[n, _constant],
                    also_merge='all',
                    label='add_depth'
                )

            if i == 0:
                n = self._merge_occ(n)
                n = self._merge_shadow(n)
                n = self._merge_screen(n)
            n = nuke.nodes.DepthFix(inputs=[n])
            if get_max(_read_node, 'depth.Z') > 1.1:
                n['farpoint'].setValue(10000)

            n = nuke.nodes.Grade(
                inputs=[n],
                unpremult='rgba.alpha',
                label='白点: [value this.whitepoint]\n混合:[value this.mix]\n使亮度范围靠近0-1'
            )
            if self._config['autograde']:
                print(u'{:-^30s}'.format(u'开始 自动亮度'))
                _max = self._autograde_get_max(_read_node)
                if _max < 0.5:
                    _mix = 0.3
                else:
                    _mix = 0.6
                n['whitepoint'].setValue(_max)
                n['mix'].setValue(_mix)
                print(u'{:-^30s}'.format(u'结束 自动亮度'))
            n = nuke.nodes.Unpremult(inputs=[n])
            n = nuke.nodes.ColorCorrect(inputs=[n], label='亮度调整')
            n = nuke.nodes.ColorCorrect(
                inputs=[n], mix_luminance=1, label='颜色调整')
            if 'SSS.alpha' in _read_node.channels():
                n = nuke.nodes.ColorCorrect(
                    inputs=[n],
                    maskChannelInput='SSS.alpha',
                    label='SSS调整'
                )
            n = nuke.nodes.HueCorrect(inputs=[n])
            n = nuke.nodes.Premult(inputs=[n])

            n = self._depthfog(n)

            n = nuke.nodes.SoftClip(
                inputs=[n], conversion='logarithmic compress')
            n = nuke.nodes.ZDefocus2(
                inputs=[n],
                math='depth',
                center='{{[value _ZDefocus.center curve]}}',
                focal_point='1.#INF 1.#INF',
                dof='{{[value _ZDefocus.dof curve]}}',
                blur_dof='{{[value _ZDefocus.blur_dof curve]}}',
                size='{{[value _ZDefocus.size curve]}}',
                max_size='{{[value _ZDefocus.max_size curve]}}',
                label='[\nset trg parent._ZDefocus\n'
                'knob this.math [value $trg.math depth]\n'
                'knob this.z_channel [value $trg.z_channel depth.Z]\n'
                'if {[exists _ZDefocus]} '
                '{return \"由_ZDefocus控制\"} '
                'else '
                '{return \"需要_ZDefocus节点\"}\n]',
                disable='{{![exists _ZDefocus] '
                '|| [if {[value _ZDefocus.focal_point \"200 200\"] == \"200 200\" '
                '|| [value _ZDefocus.disable]} {return True} else {return False}]}}'
            )
            n = nuke.nodes.Crop(
                inputs=[n],
                box='0 0 root.width root.height'
            )

            if i > 0:
                n = nuke.nodes.Merge2(
                    inputs=[bg_ch_nodes[i - 1], n],
                    label=_read_node[self.tag_knob_name].value()
                )
            bg_ch_nodes[i] = n
        return n

    @staticmethod
    def _autograde_get_max(n):
        rgb_max = get_max(n, 'rgb')
        erode_size = 0
        erode_node = nuke.nodes.Dilate(inputs=[n], size=erode_size)
        # Exclude small highlight
        while rgb_max > 1 and erode_size > n.height() / -100.0:
            erode_node['size'].setValue(erode_size)
            rgb_max = get_max(erode_node, 'rgb')
            if rgb_max < 1:
                break
            erode_size -= 1
            print(u'收边 {}'.format(erode_size))
        nuke.delete(erode_node)

        return rgb_max

    @staticmethod
    def _merge_depth(input_node, nodes):
        if len(nodes) < 2:
            return

        merge_node = nuke.nodes.Merge2(
            inputs=nodes[:2] + [None] + nodes[2:],
            tile_color=2184871423L,
            operation='min',
            Achannels='depth', Bchannels='depth', output='depth',
            label='Depth',
            hide_input=True)
        copy_node = nuke.nodes.Copy(
            inputs=[input_node, merge_node], from0='depth.Z', to0='depth.Z')
        return copy_node

    @staticmethod
    def _depthfog(input_node):
        _group = nuke.nodes.Group(
            inputs=[input_node],
            tile_color=0x2386eaff,
            label="深度雾\n由_DepthFogControl控制",
            disable='{{![exists _DepthFogControl] || _DepthFogControl.disable}}',
        )
        _group.setName(u'DepthFog1')

        _group.begin()
        _input_node = nuke.nodes.Input(name='Input')
        n = nuke.nodes.DepthKeyer(
            inputs=[_input_node],
            disable='{{![exists _DepthFogControl] || _DepthFogControl.disable}}',
        )
        n['range'].setExpression(
            u'([exists _DepthFogControl.range]) ? _DepthFogControl.range : curve')
        n = nuke.nodes.Grade(
            inputs=[_input_node, n],
            black='{{([exists _DepthFogControl.fog_color]) ? _DepthFogControl.fog_color : curve}}',
            unpremult='rgba.alpha',
            mix='{{([exists _DepthFogControl.fog_mix]) ? _DepthFogControl.fog_mix : curve}}',
            disable='{{![exists _DepthFogControl] || _DepthFogControl.disable}}',
        )
        n = nuke.nodes.Output(inputs=[n])
        _group.end()

        return _group

    @staticmethod
    def _merge_occ(input_node):
        _nodes = Comp.get_nodes_by_tags(u'OC')
        n = input_node
        for _read_node in _nodes:
            _reformat_node = nuke.nodes.Reformat(
                inputs=[_read_node], resize='fit')
            n = nuke.nodes.Merge2(
                inputs=[n, _reformat_node],
                operation='multiply',
                screen_alpha=True,
                label='OCC'
            )
        return n

    @staticmethod
    def _merge_shadow(input_node):
        _nodes = Comp.get_nodes_by_tags(['SH', 'SD'])
        n = input_node
        for _read_node in _nodes:
            _reformat_node = nuke.nodes.Reformat(
                inputs=[_read_node], resize='fit')
            n = nuke.nodes.Grade(
                inputs=[n, _reformat_node],
                white="0.08420000225 0.1441999972 0.2041999996 0.0700000003",
                white_panelDropped=True,
                label='Shadow'
            )
        return n

    @staticmethod
    def _merge_screen(input_node):
        _nodes = Comp.get_nodes_by_tags(u'FOG')
        n = input_node
        for _read_node in _nodes:
            _reformat_node = nuke.nodes.Reformat(
                inputs=[_read_node], resize='fit')
            n = nuke.nodes.Merge2(
                inputs=[n, _reformat_node],
                operation='screen',
                maskChannelInput='rgba.alpha',
                label=_read_node[Comp.tag_knob_name].value(),
            )
        return n

    @staticmethod
    def _add_zdefocus_control(input_node):
        # Use for one-node zdefocus control
        n = nuke.nodes.ZDefocus2(inputs=[input_node], math='depth', output='focal plane setup',
                                 center=0.00234567, blur_dof=False, label='** 虚焦总控制 **\n在此拖点定虚焦及设置')
        n.setName(u'_ZDefocus')
        return n

    @staticmethod
    def _add_depthfog_control(input_node):
        node_color = 596044543
        n = nuke.nodes.DepthKeyer(
            label='**深度雾总控制**\n在此设置深度雾范围及颜色',
            range='1 1 1 1',
            gl_color=node_color,
            tile_color=node_color,
        )

        n.setName(u'_DepthFogControl')
        # n = n.makeGroup()

        k = nuke.Text_Knob('颜色控制')
        n.addKnob(k)

        k = nuke.Color_Knob('fog_color', '雾颜色')
        k.setValue((0.009, 0.025133, 0.045))
        n.addKnob(k)

        k = nuke.Double_Knob('fog_mix', 'mix')
        k.setValue(1)
        n.addKnob(k)

        n.setInput(0, input_node)
        return n


if not nuke.GUI:
    nukescripts.PythonPanel = object


class CompDialog(nukescripts.PythonPanel):
    """Dialog UI of class Comp."""

    knob_list = [
        (nuke.Tab_Knob, 'general_setting', '常用设置'),
        (nuke.File_Knob, 'input_dir', '输入文件夹'),
        (nuke.File_Knob, 'output_dir', '输出文件夹'),
        (nuke.File_Knob, 'mp', '指定MP'),
        (nuke.File_Knob, 'mp_lut', 'MP LUT'),
        (nuke.Boolean_Knob, 'exclude_existed', '排除已输出镜头'),
        (nuke.Boolean_Knob, 'autograde', '自动亮度'),
        (nuke.Tab_Knob, 'filter', '正则过滤'),
        (nuke.String_Knob, 'footage_pat', '素材名'),
        (nuke.String_Knob, 'dir_pat', '路径'),
        (nuke.String_Knob, 'tag_pat', '标签'),
        (nuke.EndTabGroup_Knob, 'end_tab', ''),
        (nuke.Multiline_Eval_String_Knob, 'info', ''),
    ]
    config_file = os.path.expanduser(u'~/.nuke/wlf.comp.config.json')

    def __init__(self):
        nukescripts.PythonPanel.__init__(self, '吾立方批量合成', 'com.wlf.multicomp')
        self.config = Comp.default_config
        self._shot_list = None
        self.read_config()

        for i in self.knob_list:
            k = i[0](i[1], i[2])
            try:
                k.setValue(self.config.get(i[1]))
            except TypeError:
                pass
            self.addKnob(k)
        self.knobs()['exclude_existed'].setFlag(nuke.STARTLINE)
        # self.update()

    def read_config(self):
        """Read config from disk."""

        if os.path.isfile(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config.update(json.load(f))
        else:
            self.write_config()

    def write_config(self):
        """Write config to disk."""

        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def knobChanged(self, knob):
        """Overrride for buttons."""

        if knob is self.knobs()['OK']:
            threading.Thread(target=self.progress).start()
        elif knob is self.knobs()['info']:
            self.update()
        else:
            self.config[knob.name()] = knob.value()
            self.update()

    def progress(self):
        """Start process all shots with a processbar."""

        task = nuke.ProgressTask('批量合成')
        errors = ''

        for i, shot in enumerate(self._shot_list):
            if task.isCancelled():
                break
            task.setMessage(shot)

            self.config['shot'] = os.path.basename(shot)
            self.config['save_path'] = os.path.join(
                self.config['output_dir'], '{}.nk'.format(self.config['shot']))
            self.config['footage_dir'] = shot if os.path.isdir(
                shot) else os.path.join(self.config['input_dir'], self.config['shot'])
            self.write_config()
            _cmd = u'"{nuke}" -t {script} "{config}"'.format(
                nuke=nuke.EXE_PATH,
                script=os.path.normcase(__file__).rstrip(u'c'),
                config=json.dumps(self.config).replace(
                    u'"', r'\"').replace(u'^', r'^^')
            ).encode(SYS_CODEC)
            proc = Popen(_cmd, shell=True, stderr=PIPE)
            stderr = proc.communicate()[1]
            if stderr:
                print(stderr)
                errors += u'<tr><td>{}</td><td>{}</td></tr>\n'.format(
                    self.config['shot'], stderr.strip().split('\n')[-1])
            if proc.returncode:
                errors += u'<tr><td>{}</td><td>非正常退出码:{}</td></tr>\n'.format(
                    self.config['shot'], proc.returncode)
            task.setProgress((i + 1) // len(self._shot_list) * 100)

        if errors:
            errors = u'<style>td{{padding:8px;}}</style>'\
                u'<table><tr><th>镜头</th><th>错误</th>'\
                u'</tr>\n{}</table>'.format(errors)
            with open(os.path.join(self.config['output_dir'], u'批量合成日志.html'), 'w') as f:
                f.write(errors.encode('UTF-8'))
            nuke.executeInMainThread(nuke.message, args=(errors,))
        nukescripts.start(self.config['output_dir'].encode(SCRIPT_CODEC))

    def update(self):
        """Update ui info and button enabled."""

        def _info():
            _info = u'测试'
            self._shot_list = list(Comp.get_shot_list(self.config))
            if self._shot_list:
                _info = u'# 共{}个镜头\n'.format(len(self._shot_list))
                _info += u'\n'.join(self._shot_list)
            else:
                _info = u'找不到镜头'
            self.knobs()['info'].setValue(_info.encode(SCRIPT_CODEC))

        def _button_enabled():
            _knobs = [
                'output_dir',
                'mp',
                'exclude_existed',
                'autograde',
                'info',
                'OK',
            ]

            _isdir = os.path.isdir(self.config['input_dir'])
            if _isdir:
                for k in ['exclude_existed', 'info']:
                    self.knobs()[k].setEnabled(True)
                if self._shot_list:
                    for k in _knobs:
                        self.knobs()[k].setEnabled(True)
                else:
                    for k in set(_knobs) - set(['exclude_existed']):
                        self.knobs()[k].setEnabled(False)
            else:
                for k in _knobs:
                    self.knobs()[k].setEnabled(False)

        _info()
        _button_enabled()


class FootageError(Exception):
    """Indicate not found needed footage."""

    def __init__(self, *args):
        super(FootageError, self).__init__()
        self.tags = args

    def __str__(self):
        return u' # '.join(self.tags)


class RenderError(Exception):
    """Indicate some problem caused when rendering."""

    def __init__(self, *args):
        super(RenderError, self).__init__()
        self.tags = args

    def __str__(self):
        return u' # '.join(self.tags)


def insert_node(node, input_node):
    """Insert @node after @input_node."""

    for n in nuke.allNodes():
        for i in range(n.inputs()):
            if n.input(i) == input_node:
                n.setInput(i, node)

    node.setInput(0, input_node)


def get_max(n, channel='rgb'):
    '''
    Return themax values of a given node's image at middle frame

    @parm n: node
    @parm channel: channel for sample
    '''
    # Get middle_frame
    middle_frame = (n.frameRange().first() + n.frameRange().last()) // 2

    # Create nodes
    invert_node = nuke.nodes.Invert(channels=channel, inputs=[n])
    mincolor_node = nuke.nodes.MinColor(
        channels=channel, target=0, inputs=[invert_node])

    # Execute
    try:
        nuke.execute(mincolor_node, middle_frame, middle_frame)
        max_value = mincolor_node['pixeldelta'].value() + 1
    except RuntimeError, ex:
        if 'Read error:' in str(ex):
            max_value = -1
        else:
            raise RuntimeError, ex

    # Avoid dark frame
    if max_value < 0.7:
        nuke.execute(mincolor_node, n.frameRange().last(),
                     n.frameRange().last())
        max_value = max(max_value, mincolor_node['pixeldelta'].value() + 1)
    if max_value < 0.7:
        nuke.execute(mincolor_node, n.frameRange().first(),
                     n.frameRange().first())
        max_value = max(max_value, mincolor_node['pixeldelta'].value() + 1)

    # Delete created nodes
    for i in (mincolor_node, invert_node):
        nuke.delete(i)

    # Output
    print(u'getMax({1}, {0}) -> {2}'.format(channel, n.name(), max_value))

    return max_value


def autoplace_all():
    """Place all nodes position so them won't overlap."""

    for n in nuke.allNodes():
        nuke.autoplace(n)


def main():
    """Run this moudule as a script."""

    reload(sys)
    sys.setdefaultencoding('UTF-8')
    try:
        Comp(json.loads(sys.argv[1]))
    except FootageError as ex:
        print(u'** FootageError: {}\n\n'.format(ex).encode(SYS_CODEC))
        traceback.print_exc()


def pause():
    """Pause prompt with a countdown."""

    print(u'')
    for i in range(5)[::-1]:
        sys.stdout.write(u'\r{:2d}'.format(i + 1))
        time.sleep(1)
    sys.stdout.write(u'\r          ')
    print(u'')


if __name__ == '__main__':
    main()
