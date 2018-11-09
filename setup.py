from setuptools import setup

setup(name='aiowintest',
      version='0.0.1',
      description='Python implementation of the Win-Test UDP protocol',
      url='http://github.com/hin/wintest-python',
      author='Hans Insulander SM0UTY',
      author_email='hans@codium.se',
      license='BSD 2-Clause "Simplified" License',
      packages=['aiowintest'],
      install_requires=[
          'asyncio',
      ],
      zip_safe=False)
