"""Installs package.
"""

from setuptools import setup

setup(name='bokeh_apps',
      version='0.1',
      packages=[
          'bokeh_apps',
          'bokeh_apps.bokeh',
          'bokeh_apps.bokeh.memory',
          ],
      entry_points={
          'console_scripts': [
              'bokeh-server = bokeh_apps.bokeh.bokeh_server:main',
          ]
      }
     )
