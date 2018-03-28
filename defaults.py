
""" =================================
    Load Packages
================================= """
import importlib
import pip

'''
@input ipython_globals globals of parent
@input packages a list of key value pairs, where:
                key is the alias of the module
                value is the name of the module itself
'''
# Courtesy of rominf
# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
def load(packages,
         ipython_globals=globals()):

    for k, v in packages.items():
        try:
            ipython_globals[k] = importlib.import_module(v)
        except ImportError:
            print("Module " + v + " does not exist. Please search installation instructions for " + v + ".")
            pass
            
""" =================================
    Load Header (CSS + JS) Files
================================= """

load({"ip" : "IPython"})
from IPython.core.display import HTML

def stylize():

    css_files = ['shared/css/defaults.css',
                 '../../shared/css/definitions.css',
                 '../../shared/css/general.css',
                 'shared/css/python.css']

    js_files = ['https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
                'shared/js/styles.js',
                'shared/js/popover.js']

    head_str = ""
    for css_file in css_files:
        head_str += '<link href="' + css_file + '" rel="stylesheet">'
    for js_file in js_files:
        head_str += '<script src="' + js_file + '"></script>'

    return HTML(head_str)

""" =================================
    Get CSS Variables
================================= """

load({"re" : "re",
      "os" : "os"})

# Perform a cascading load, i.e. the first file to be found 
# will be used to load all the css vars
def __load_css_vars(css_files):
    for css_file in css_files:
        if os.path.isfile(css_file):
            css_contents = open(css_file,'r').read()
            # Remove all spacelines
            css_contents = re.sub('[\r\n\t]','',css_contents)
            # Remove all comments
            css_contents = re.sub("/\*[^\*]*\*/",'',css_contents)
            # Find root blocks
            css_contents = re.findall(":root[ ]*\{([^\{\}]*)\}",css_contents)
            # Get all variables
            css_contents = " ".join(css_contents).split(";")
            # Trim each variable strings
            css_contents = [ v.lstrip().rstrip() for v in css_contents ]
            # Split each variable string to get key value pairings
            css_contents = [ re.split("[ ]*:[ ']*|[' ]*,[' ]*",v) for v in css_contents ]
            # Assign key value pairs
            css_dictionary = dict((v[0], v[1] if len(v) == 2 else tuple(v[1:])) for v in css_contents if len(v) >= 2)

            return css_dictionary

__css_vars = __load_css_vars(['../../shared/css/definitions.css',
                              'shared/css/defaults.css'])

""" =================================
    Get CSS Colors And Fonts
================================= """

load({"collections":"collections"})

### Helper Functions ###

__color_palette = [ v for k, v in __css_vars.items() if "--color-" in k ]
__hue_palette = collections.OrderedDict((h,__css_vars["--" + h]) for h in ["yellow",
                                                                          "orange",
                                                                          "red",
                                                                          "purple",
                                                                          "blue",
                                                                          "cyan",
                                                                          "green"])

# Function courtesy of John 1024
# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
def __hex_to_rgb(color):
    hex_c = color.lstrip("#")
    return tuple(int(hex_c[i:i+2],16) for i in (0,2,4))

# Returns a gradient palette. 
# For the output, users can get an arbitrary amount of colors
# by specifying the number he/she prefers using n_colors
def __color_brewer_palette(colors):
    
    def color_gradient_fn(n_colors):

        # Create information about input of colors
        stop_points = list(map(lambda i : 1. * i / (len(colors) - 1), range(0, len(colors))))
        
        # Create stops for which to be outputed
        col_output_stops = list(map(lambda i : 1. * i / (n_colors - 1), range(0, n_colors)))
        col_output = []

        ind_t = 0
        ind_tp1 = 1
        for s in col_output_stops:

            # Check if we are in the correct interval
            while s > stop_points[ind_tp1]:
                ind_t += 1
                ind_tp1 += 1

            # Now we should have stop_points[ind_t] < s <= stop_points[ind_tp1]
            ratio = (s - stop_points[ind_t]) / (stop_points[ind_tp1] - stop_points[ind_t])
            col_output.append(pollute_color(colors[ind_t], colors[ind_tp1],ratio))

        return col_output

    return color_gradient_fn

### Public Functions ###

def_font = __css_vars["--font-family"][0]
bg_color = __css_vars["--pri"]
txt_color = __css_vars["--font-color"]
ltxt_color = __css_vars["--font-color-75"]

# Interpolate between two colors
# Ratio determines the degree of pollution
# 0 means no pollution 1 means all polluted color
def pollute_color(original_col, pollute_col, ratio):
    col0 = __hex_to_rgb(original_col)
    col1 = __hex_to_rgb(pollute_col)
    val = [0.,0.,0.]
    for i in range(0,len(val)):
        val[i] = int((1. - ratio) * col0[i] + ratio * col1[i])
    return '#%02x%02x%02x' % tuple(val)

# Fades the color depending on the fading factor (0 to 1)
def fade_color(color, fadingFactor):
    return pollute_color(bg_color, color, fadingFactor)
    
def get_color(inp = "", fadingFactor = 1.0):
    
    fader = lambda c : fade_color(c, fadingFactor)
    tmp_color_palette = [ fader(c) for c in __color_palette]
    tmp_hue_palette = collections.OrderedDict((k,fader(c)) for k, c in __hue_palette.items())

    if (inp == ""):
        # If nothing is specified, return the list of color palettes
        return tmp_color_palette
    elif (isinstance(inp,int)):
        # If index is specified, return the index of the color palette
        return tmp_color_palette[(inp + len(tmp_color_palette)) % len(tmp_color_palette)]
    elif (inp in tmp_hue_palette):
        # If palette is requested, return the palette
        return tmp_hue_palette[inp]
    elif (inp == "palette"):
        # If palette is requested, return the palette
        return __color_brewer_palette(list(tmp_hue_palette.values()))
    else:
        return bg_color

""" =================================
    Static Plot settings
================================= """

load({"mpl" : "matplotlib"})

# Default Fonts
mpl.rcParams['font.family'] = def_font
mpl.rcParams['text.color'] = txt_color
mpl.rcParams['font.size'] = 25
# Title Size
mpl.rcParams['axes.titlesize'] = 30
mpl.rcParams['axes.titlepad'] = 20

# Figure
mpl.rcParams['figure.facecolor'] = bg_color

# Axes Sizes
mpl.rcParams['axes.facecolor'] = bg_color
mpl.rcParams['axes.edgecolor'] = ltxt_color
mpl.rcParams['axes.labelsize'] = 25
mpl.rcParams['axes.labelpad'] = 10
mpl.rcParams['axes.labelcolor'] = ltxt_color
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['ytick.labelsize'] = 20
mpl.rcParams['xtick.color'] = ltxt_color
mpl.rcParams['ytick.color'] = ltxt_color

# Legend
mpl.rcParams['legend.loc'] = 'upper right'
mpl.rcParams['legend.frameon'] = False
mpl.rcParams['legend.facecolor'] = bg_color
mpl.rcParams['legend.fontsize'] = 20

""" =================================
    Dynamic Plot settings
================================= """

load({"plotly":"plotly"})
import plotly.graph_objs as py_go

plotly.offline.init_notebook_mode(connected=True)

py_layout = py_go.Layout(
    font = dict(
        family = def_font,
        color = txt_color
    ),
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
    xaxis = dict(color=ltxt_color),
    yaxis = dict(color=ltxt_color),
    # Polar Variables
    polar = dict(
        bgcolor = bg_color,
        angularaxis = dict(
            color=ltxt_color,
            direction="clockwise"
        ),
        radialaxis = dict(
            color=ltxt_color
        )
    )
)
