# Electricity Grid Visualisation

The examples I created require a number of packages to be installed to work,
such as:

* numpy
* pandas
* matplotlib
* geoplot
* geopandas
* plotly
* folium
* ...

My personal research notes are stored in a OneNote notebook under the "Summer Research" folder. Each `*.one` file is a section in the notebook. 

Each folder contains a different experiment that I performed.
To follow the progression of my thoughts, the order in which I created the folders
is as follows:

## 1. initialExperiments

Found a shapefile of Australia from the Australian Bureau of Statistics:
https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files

Plotted a map of Australia with this data using GeoPandas library.

## 2. condaExperiment

Learnt how the Anaconda package manager works to install the required dependencies.

## 3. plotlyExperiment

Learnt about the Plotly library for python, which displays plots in a web browser
and has visually appealling graphs.

## 4. temperatureHistoryExample

Created a geographical plot of temperature data across Australia from 1975 to now.
Different temperatures were represented with different coloured dots.

## 5. scatterMapboxTesting

Creates the same output as the previous test.
I was going to test more functionality of the Plotly library but didn't get
round to it.

## 6. foliumTest

Very short example seeing how the Folium library for Python works.
It creates an html file that you need to manually open.

## 7. blogExample

Working through a number of examples that use the GeoPlot library for python.
Examples are from the blog post:
https://towardsdatascience.com/visualizing-geospatial-data-in-python-e070374fe621

Uncomment relevant sections of the code to do a particular example from the blog.

In the end, I created my own custom plot based off of what I learnt from the
blog post to recreate the the map from example *4. temperatureHistoryExample*
using geoplot instead of plotly.  This example does not have animation however,
and only shows the temperatures from 1975.

## 8. animationExample

Some simple animation examples using the matplotlib animation API, taken from
the matplotlib website. I was trying to understand how to do animations in
matplotlib so that I could eventually apply it to the graphs of the Queensland
grid.

`animatedDecay.py` traces out a graph of damped harmonic motion.

`animatedHistogram.py` plots histograms of a number of randomly generated
normal distributions with the same mean and standard deviation.

## 9. tempvoronoi

Created a "Voronoi" plot of the Australian temperature example data from 1975.
This automatically partitions the plot into polygons for each data point, the
colour of which is determined by the value (temperature in this case) of the
point within it.

## 10. Matlab

The example Matlab code from FeiFei.

## 11. manualTest

Unfinished example that doesn't work.

## 12. topographicExample

An example of a topographic map&mdash;essentially a continuously coloured contour
map of the vertical height above sea level of madagascar.

This really stood out to me as what I wanted to create for the electricity grid
visualisation, except using frequency (or voltage, etc.) instead of elevation.

## 13. tempContourMap

There are 3 main files here that all try to create the colour map/heat map/contour map (all very similar) of the Australian temperature data:

`main.py` creates a scatterplot with a very large number of points to create
what looks like a smooth image.

`contourfTest.py` creates a coloured contour plot using the contourf function
in matplotlib. This has discrete colours that each represent a range of values,
so the colours do not quite change continuously. However, the number of colours
used can be specified as a high number to appear almost continuous. Also note
that in this example I did not clip the plot on the outline of Australia (but
I did in the other two examples).

`imshowTest.py` creates a continuous colour map "image" using the matplotlib
imshow function (imshow means "show image"). This achieves the same result as
the scatterplot, but much more efficiently as this imshow function is designed
to show this sort of data.

## 14. frequencyTest

In `main.py`, created a static colourmap of the frequency data in Queensland.

In `voronoi.py`, created a Voronoi plot of the frequency data in Queensland.

Note that there are two different interpolation functions that can be used (can
comment out either one). The `griddata()` function does not do any extrapolation,
but the `Rbf()` (radial basis function) function does. This extrapolation is
not accurate over long distances however (grid frequency in the ~1000&nbsp;Hz to
negative Hz).

## 15. TempAnimationInJanuary

Created an animated colour map of the Australian temperature example data. This
applies the matplotlib animation API that I learned in example *8.
animationExample*.

## 16. greaterBrisbaneTest

This is a test of the frequency data, only plotting the data in and around
Greater Brisbane. It uses a map outline of Greater Brisbane in the plot.
This was done to get a more detailed view of that region, as that is where
most of the PMUs are located.

## 17. read_from_open_historian

This is the example code to use Open Historian, provided by David.

## 18. tkinterTest

These are examples taken from the internet for how to embed matplotlib plots
into a tkinter GUI. Learning how to do this is very useful for my application.

## 19. tkinterAnimation

`SOexample.py` is an example of how to do a matplotlib animation for a plot
embedded in a tkinter GUI.

`tempData.py` applies this to the Australian temperature example data.

## 20. tkinterGUI

This contains a number of tests to create a more useable GUI with tkinter.

`zooming.py` gives the ability to zoom in on different parts of the map with
the mouse scroll wheel. However, the image does not become more detailed as
you zoom, so things start to look more pixelated as you zoom in.

`zooming_with_detail.py` fixes the issue with `zooming.py` with regards to the
pixellation when you zoom in.

`zooming_plus_buttons.py` builds upon `zooming_with_detail.py`, adding buttons
to switch between map type (either continuous colour plot, scatter plot or 
Voronoi plot), and buttons to play and pause the animation. The actions for these
buttons have not yet been implemented.

The files `reset_detail.py` and `zoom_factory.py` provide utility functions for
the other files.

## 21. readDataTest

`readFuncs.py` provides a number of functions to read the csv data from a file
system into memory. It also contains a bunch of tests for these functions.

`main.py` reads in the csv data for the available PMUs on 28th July 2021 from
12:00&nbsp;a.m. until 1:00&nbsp;a.m. Then, it begins animating this data in a
colourmap overlayed on Queensland, using the tkinter GUI from example *20.
tkinterGUI*.

## 22. tkinterAskDirectoryExample

Testing out the Tkinter dialog window that asks you to open a folder
(and returns a string of the path to that folder)

## 23. tempScatterExample

Creating a scatterplot of the example Australian temperature data, but with
a nicer asthetic (larger points, slightly transparent). Not only does the
point colour vary with the temperature value but also the point size.

## 24. solution1

The first implementation of the GUI for viewing historical grid frequency data
across queensland.

The data is selected through dialog windows that ask for the folder location
of the csv files and also the locaiton of the .xlsx document containing the
GPS coordinates.

## 25. tkinterShowHide

Example from Stack Overflow demonstrating the ability to show and hide tkinter
widgets when necessary (this may be useful for the grid frequency GUI before
the csv files are chosen).

## 26. matplotlibLegend

Small test to see how a legend is created on matplotlib.