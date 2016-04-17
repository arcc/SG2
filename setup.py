#!/usr/bin/env python
from distutils.core import setup
import numpy, os, sys
from distutils.extension import Extension

setup(
    name="SG2_IMAGE",
    version = '0.0.1',
    description = 'A image library for STARGATE SG2 ',

    author = 'Luo Jing, Anthony Elite, et al.',
    author_email = 'luojing1211@gmail.com',
    url = 'https://github.com/arcc/SG2',

    packages=['sg2'],
    package_dir = {'sg2': '/Users/jingluo/Research_codes/sg2'},

    py_modules = ['sg2.core.database.sg2_database_utils',
        'sg2.core.getIMG.sg2_img',
        'sg2.core.sg2_category.sg2_category',
        'sg2.core.sg2_users.user'],
)
