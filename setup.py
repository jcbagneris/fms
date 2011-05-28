import os
import os.path
from setuptools import setup

import fms.version
version = fms.version.TAG

setup(name='fms',
        version = version,
        description = 'A Financial Market Simulator',
        author = 'Jean-Charles Bagneris',
        author_email = 'jcbagneris@gmail.com',
        url = 'http://github.com/jcbagneris/fms',
        license = 'BSD',
        long_description=open('README').read(),
        packages = ['fms',
                    'fms.agents',
                    'fms.engines',
                    'fms.markets',
                    'fms.utils',
                    'fms.worlds',
                    ],
        scripts = ['startfms.py'],
        install_requires = ['distribute','PyYAML',],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2",
            "Topic :: Scientific/Engineering",
        ],
        )
