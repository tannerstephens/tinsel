from setuptools import setup

setup(
  name='Tinsel',
  version='1.0.0',
  author='Tanner Stephens',
  author_email='me@tannerstephens.com',
  packages=['tinsel'],
  license='LICENSE.md',
  description='An Advent of Code utils package',
  package_data={'tinsel': ['runner/day_template/*']},
  entry_points={
    'console_scripts': [
      'aoc = tinsel.runner:main',
    ]
  }
)
