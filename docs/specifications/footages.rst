素材命名要求
==============

使用文件名作为命名

必须满足此命名要求才能使用 :ref:`自动合成` 和 :ref:`批量自动合成`

范例
------------

符合标准的命名:

* ``SNJYW_ep123_01abcd_sc001abc_CH_B_asdasdqwe_asd``
* ``SNJYW_EP01_01_sc001_CH_A``
* ``EP01_01_sc001_CH_A``
* ``EP01_sc001_CH_A``
* ``CH_A``
* ``CH``

详细定义
----------------

命名由3部分组成: 

  * 前缀

    格式: [`字符`\ ``_``][``ep``\ `数字`\ ``_``][`数字`\ [`字母`]\ ``_``][``sc``\ `数字`\ [`字母`]\ ``_``]

  * 标签

    格式: `字母`\ [`字符`]\ ``_``\ [`字母`\ [`字符`]\ [``_`` 或 ``.``]]

  * 后缀

    格式不限

    后缀决定了相同标签的自动合成顺序, 参见 :doc:`comp`



.. note::

  用方括号括起的部分为可选

  字符 = 字母 + 数字  

  字符不包含 ``.``, ``\``, ``_``  

匹配所用正则表达式:

:regexp:`(?i)(?:[^_]+_)?(?:ep\\d+_)?(?:\\d+[a-zA-Z]*_)?(?:sc\\d+[a-zA-Z]*_)?((?:[a-zA-Z][^\\._]*_?){,3})`

标准标签
-------------------

推荐使用以下标签:

* ``BG_``\ `单个字母`

  例如: ``BG_A``, ``BG_B``

* ``CH_``\ `单个字母`

  例如: ``CH_A``, ``CH_B``

  CH层在自动合成中会叠加在所有BG层之上, 参见 :doc:`comp`

* ``SH`` 或 ``SH_``\ `任意`

  例如: ``SH``, ``SH_CH``
  
* ``OCC`` 或 ``OCC_``\ `任意`

  例如: ``OCC`` , ``OCC_BG``

如果文件名不含标准标签而父目录名称含标准标签时将使用父目录名称作为命名

.. note::

  部分常用别称会在识别时自动转换成标准标签

版本
-----------------------------

所有素材的后缀中应该含有 ``_v数字.`` 或者 ``_v数字_``

  例如: ``CH_A_test_v1_abc.exr`` , ``CH_B_v0.exr``  

第一个版本就要有版本号 无论之后是否会修改

只有使用了版本号的素材才能在nuke中按 ``Alt+↑`` 和 ``Alt+↓`` 切换版本

.. note::

  数字应为从0开始的正数

摄像机命名
--------------------------

推荐使用形如: ``镜头名_起始帧_结束帧_c版本.fbx`` 的摄像机

例如:

``SNJYW_EP01_01_sc001_1_999_c1.fbx``

.. note::

  使用 ``c版本`` 是nuke原生摄像机版本管理的规范  