"""Main module for memory app.
"""

import bokeh.client
import bokeh.io
import bokeh.layouts
import bokeh.models
import bokeh.models.widgets
import bokeh.plotting
import copy

from bokeh.models.tools import BoxSelectTool, BoxZoomTool, HoverTool, \
    ResizeTool, ResetTool, WheelZoomTool
from bokeh_apps.bokeh import MESSAGES


DOC = bokeh.io.curdoc()

def memory_plot():

    """Creates the memory plot.
    """

    names = ['time', 'memory', 'pid', 'rank', 'host']
    source = bokeh.models.ColumnDataSource(data={key: [] for key in names})

    hover = HoverTool()
    hover.tooltips = [
        ('host', '@host'),
        ('pid', '@pid'),
        ('rank', '@rank'),
        ('time', '@time'),
        ('memory', '@memory')
    ]

    tools = [BoxSelectTool(), BoxZoomTool(), hover, ResizeTool(), ResetTool(),
             WheelZoomTool()]

    plot = bokeh.plotting.figure(tools=tools)
    plot.xaxis.axis_label = "Time"
    plot.yaxis.axis_label = "Memory [MiB]"

    return source, plot


SOURCE, PLOT = memory_plot()

LAYOUT = bokeh.layouts.row([PLOT])
TABS_LIST = [bokeh.models.widgets.Panel(child=LAYOUT, title='BRYAN')]
TABS = bokeh.models.widgets.Tabs(name='memory_tabs', tabs=TABS_LIST)

HOSTNAMES = []
HOST_SOURCES = {}
HOST_PLOTS = {}

def memory_update():

    """Streams data to memory plot.
    """

    if MESSAGES['memory']:
        for hostname in MESSAGES['memory']:
            if hostname not in HOSTNAMES:
                add_host_tab(hostname)
#       data = {key: val for key, val in MESSAGES['memory'].iteritems()}
#       SOURCE.stream(data, 50)

def add_host_tab(hostname):

    """Adds a new tab to figure.
    """

    HOSTNAMES.append(hostname)
    print("NEW HOSTNAME Detected:", hostname)

    names = ['time', 'memory', 'pid', 'rank', 'host']
    source = bokeh.models.ColumnDataSource(data={key: [] for key in names})

    HOST_SOURCES[hostname] = source

    hover = HoverTool()
    hover.tooltips = [
        ('host', '@host'),
        ('pid', '@pid'),
        ('rank', '@rank'),
        ('time', '@time'),
        ('memory', '@memory')
    ]

    tools = [BoxSelectTool(), BoxZoomTool(), hover, ResizeTool(), ResetTool(),
             WheelZoomTool()]

    plot = bokeh.plotting.figure(tools=tools)
    plot.xaxis.axis_label = "Time"
    plot.yaxis.axis_label = "Memory [MiB]"
    plot.line('time', 'memory', source=source)

    HOST_PLOTS[hostname] = plot

    layout = bokeh.layouts.row([plot])

    TABS_LIST.append(bokeh.models.widgets.Panel(child=layout, title=hostname))
    TABS.update(tabs=TABS_LIST)
    print("MY HOST", hostname)
#   DOC.remove_root(TABS)
    DOC.add_root(TABS)
#   bokeh.client.push_session(DOC)

DOC.add_periodic_callback(memory_update, 500)

#DOC.add_root(TABS)
