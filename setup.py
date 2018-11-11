from setuptools import setup

setup(name='aiowintest',
      version='0.0.2.dev1',
      description='Python implementation of the Win-Test UDP protocol',
      url='http://github.com/hin/aiowintest',
      author='Hans Insulander SM0UTY',
      author_email='hans@codium.se',
      license='BSD 2-Clause "Simplified" License',
      packages=['aiowintest'],
      install_requires=[
          'asyncio',
      ],
      test_suite='aiowintest.tests',
      zip_safe=False)
