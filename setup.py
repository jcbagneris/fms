import os
import os.path
from distutils.core import setup

version = __import__('fms').VERSION

long_description = """
FMS, an agent-based financial market simulator.

FMS produces transaction data from experiments.
Experiments are defined through classes :
- world
- engine and market
- agents

Basic classes are provided, but you are encouraged
to write your own and contribute to FMS.
"""

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
        description = 'Financial Market Simulator',
        author = 'Jean-Charles Bagneris',
        author_email = 'jcb@bagneris.net',
        url = 'http://fms.bagneris.net',
        license = 'BSD',
        long_description = long_description,
        packages = ['fms',
                    'fms.agents',
                    'fms.engines',
                    'fms.markets',
                    'fms.utils',
                    'fms.worlds',
                    ],
        scripts = ['startfms.py'],
        data_files = data_files,
        )
