from os import path
from setuptools import setup, find_packages

from pyaestro import __version__


def load_readme():
    """
    Load the readme from the root of the package directory.

    :returns: A string containing the contents of README.md.
    """
    pkg_path = path.abspath(path.dirname(__file__))
    with open(path.join(pkg_path, 'README.md')) as f:
        long_description = f.read()

    return long_description

setup(
  name='pyaestro',
  description='A package of utilities structures for building workflows'
  ' and workflow related tools.',
  version=__version__,
  author='Francesco Di Natale',
  maintainer='Francesco Di Natale',
  author_email='frank.dinatale1988@gmail.com',
  url='https://github.com/FrankD412/pyaestro',
  license='MIT License',
  packages=find_packages(),
  entry_points={
    'console_scripts': []
  },
  install_requires=[],
  extras_require={},
  long_description=load_readme(),
  long_description_content_type='text/markdown',
  download_url='https://pypi.org/project/pyaestro/',
  python_requires='>3.4.*',
  classifiers=[
    'Development Status :: 1 - Planning',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  project_urls={
    'Source': 'https://github.com/FrankD412/pyaestro',
    'Tracker': 'https://github.com/FrankD412/pyaestro/issues',
  },
)
