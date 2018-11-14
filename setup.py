from setuptools import setup
import os
import io
import re

_docs_path = os.path.dirname(__file__)
_version_path = os.path.abspath(os.path.join(_docs_path,
                                             'aiowintest', '__init__.py'))
with io.open(_version_path, 'r', encoding='latin1') as fp:
    try:
        _version_info = re.search(r"^__version__ = '"
                                  r"(?P<major>\d+)"
                                  r"\.(?P<minor>\d+)"
                                  r"\.(?P<patch>\d+)"
                                  r"(?P<tag>.*)?'$",
                                  fp.read(), re.M).groupdict()
    except IndexError:
        raise RuntimeError('Unable to determine version.')

setup(name='aiowintest',
      version='{major}.{minor}.{patch}{tag}'.format(**_version_info),
      description='Python implementation of the Win-Test UDP protocol',
      long_description=open('README.rst').read(),
      url='https://github.com/hin/aiowintest',
      author='Hans Insulander SM0UTY',
      author_email='hans@codium.se',
      license='BSD 2-Clause "Simplified" License',
      packages=['aiowintest'],
      install_requires=[
          'asyncio',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      test_suite='aiowintest.tests',
      zip_safe=False)
