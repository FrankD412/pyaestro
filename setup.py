from pyaestro import __version__
from setuptools import setup, find_packages

setup(
  name='pyaestro',
  description='A tool to easily orchestrate general computational workflows '
  'both locally and on supercomputers.',
  version=__version__,
  author='Francesco Di Natale',
  maintainer='Francesco Di Natale',
  author_email='frank.dinatale1988@gmail.com',
  url='https://github.com/llnl/maestrowf',
  license='MIT License',
  packages=find_packages(),
  entry_points={
    'console_scripts': []
  },
  install_requires=[],
  extras_require={},
  long_description_content_type='text/markdown',
  download_url='https://pypi.org/project/pyaestro/',
  python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Topic :: System :: Distributed Computing',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
