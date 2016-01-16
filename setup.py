from setuptools import setup

setup(name='slack-mbta',
      version='1.0',
      description='An MBTA plugin for Slack',
      url='http://github.com:dfithian/slack-mbta.git',
      author='Dan Fithian',
      license='MIT',
      packages=['slack-mbta'],
      install_requires=[
          'argparse',
          'web.py'
      ])
