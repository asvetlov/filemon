import codecs
import os
import re
from setuptools import setup, find_packages


with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'filemon', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


install_requires = ['PySide']


setup(name='filemon',
      version=version,
      description="File Monitor",
      author="Andrew Svetlov",
      license="Apache 2",
      packages=find_packages(),
      install_requires=install_requires,
      include_package_data=True,
      entry_points={'console_scripts': ['filemon_dbg = filemon.main:main'],
                    'gui_scripts': ['filemon = filemon.main:main']})
