"""Main module for memory app.
"""

import bokeh.io
import bokeh.layouts
import bokeh.models
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

    plot.line('time', 'memory', source=source)

    return source, plot


SOURCE, PLOT = memory_plot()


def memory_update():

    """Streams data to memory plot.
    """

    if MESSAGES['memory']:
        data = {key: val for key, val in MESSAGES['memory'].iteritems()}
        SOURCE.stream(data, 50)


DOC.add_periodic_callback(memory_update, 500)

LAYOUT = bokeh.layouts.row([PLOT], sizing_mode='stretch_both')

DOC.add_root(LAYOUT)
