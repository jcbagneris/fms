import os
import os.path
from distutils.core import setup

version = __import__('fms').VERSION

data_files = []

data_dir = (
        'docs/examples',
        'docs/en/man',
        'docs/en/html',
        )

for directory in data_dir:
    for dirpath, dirnames, filenames in os.walk(directory):
        newpath = os.path.join('Doc', 
                'fms-documentation', dirpath.split(os.sep, 1)[1])
        data_files.append([newpath, 
            [os.path.join(dirpath, f) for f in filenames]])


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
        requires = ['PyYAML'],
        data_files = data_files,
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
