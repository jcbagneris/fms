import os.path
from distutils.core import setup

version = __import__(os.path.join('fms','utils')).get_version()

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


setup(name='fms',
        version = version,
        description = 'Financial Market Simulator',
        author = 'Jean-Charles Bagneris',
        author_email = 'jcb@bagneris.net',
        license = 'BSD',
        long_description = long_description,
        packages = ['fms',
                    'fms.agents',
                    'fms.engines',
                    'fms.markets',
                    'fms.utils',
                    'fms.worlds',
                    ],
        scripts = ['fms.py'],
        )
