"""Installs package.
"""

from setuptools import setup

setup(name='bokeh_apps',
      version='0.1',
      packages=[
          'bokeh_apps',
          'bokeh_apps.bokeh',
          'bokeh_apps.bokeh.memory',
          'bokeh_apps.http',
          ],
      entry_points={
          'console_scripts': [
              'bokeh-server = bokeh_apps.bokeh.bokeh_server:main',
              'http-server = bokeh_apps.http.http_server:main',
          ]
      }
     )
