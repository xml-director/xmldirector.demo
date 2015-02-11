# -*- coding: utf-8 -*-

################################################################
# xmldirector.plonecore
# (C) 2014,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

import os
from xmldirector.plonecore.transformer_registry import TransformerRegistryUtility

import xmldocument  # NOQA
import bibledocument  # NOQA

cwd = os.path.dirname(__file__)
TransformerRegistryUtility.register_transformation(
    'demo', 'shakespeare.xsl', os.path.join(cwd, 'shakespeare.xsl'))
