
""" =================================
    Load Packages
================================= """
import importlib
import pip

'''
@input packages a list of key value pairs, where:
                key is the alias of the module
                value is the name of the module itself
'''
# Courtesy of rominf
# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
def load(packages):

    for k, v in packages.items():
        try:
            globals()[k] = importlib.import_module(v)
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
def load_css_vars(css_files):
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

""" =================================
    Get CSS Colors And Fonts
================================= """

load({"collections":"collections"})

def init_colors_n_fonts(css_vars):

    globals()['bg_color'] = css_vars["--pri"]
    globals()['txt_color'] = css_vars["--font-color"]
    globals()['ltxt_color'] = css_vars["--font-color-75"]

    globals()['color_palette'] = [ v for k, v in css_vars.items() if "--color-" in k ]

    hue_colors = ["yellow",
                  "orange",
                  "red",
                  "purple",
                  "blue",
                  "cyan",
                  "green"]
    globals()['hue_palette'] = collections.OrderedDict()
    for h in hue_colors:
        globals()['hue_palette'][h] = css_vars["--" + h]

    globals()['def_font'] = css_vars["--font-family"][0]

# Function courtesy of John 1024
# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
def hex_to_rgb(color):
    hex_c = color.lstrip("#")
    return tuple(int(hex_c[i:i+2],16) for i in (0,2,4))

# Interpolate between two colors
def color_intermediary(col_start, col_end, ratio):
    col0 = hex_to_rgb(col_start)
    col1 = hex_to_rgb(col_end)
    val = [0.,0.,0.]
    for i in range(0,len(val)):
        val[i] = int((1. - ratio) * col0[i] + ratio * col1[i])
    return '#%02x%02x%02x' % tuple(val)

# Returns a gradient palette. 
# For the output, users can get an arbitrary amount of colors
# by specifying the number he/she prefers using n_colors
def color_brewer_palette(colors):
    
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
            col_output.append(color_intermediary(colors[ind_t], colors[ind_tp1],ratio))

        return col_output

    return color_gradient_fn

# Fades the color depending on the fading factor (0 to 1)
def fade_color(color, fadingFactor):
    return color_intermediary(bg_color, color, fadingFactor)
    
def get_color(inp = "", fadingFactor = 1.0):
    
    fader = lambda c : fade_color(c, fadingFactor)
    tmp_color_palette = [ fader(c) for c in color_palette]
    tmp_hue_palette = collections.OrderedDict((k,fader(c)) for k, c in hue_palette.items())

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
        return color_brewer_palette(list(tmp_hue_palette.values()))
    else:
        return bg_color

""" =================================
    Static Plot settings
================================= """

load({"mpl" : "matplotlib"})

def set_static_plots():
    # Default Fonts
    mpl.rcParams['font.family'] = def_font
    mpl.rcParams['text.color'] = txt_color
    mpl.rcParams['font.size'] = 25
    # Title Size
    mpl.rcParams['figure.titlesize'] = 30
    mpl.rcParams['axes.titlepad'] = 20

    # Figure
    mpl.rcParams['figure.facecolor'] = bg_color

    # Axes Sizes
    mpl.rcParams['axes.facecolor'] = bg_color
    mpl.rcParams['axes.edgecolor'] = ltxt_color
    mpl.rcParams['axes.titlesize'] = 25
    mpl.rcParams['axes.labelpad'] = 10
    mpl.rcParams['axes.labelsize'] = 20
    mpl.rcParams['xtick.color'] = ltxt_color
    mpl.rcParams['ytick.color'] = ltxt_color
    
    # Legend
    mpl.rcParams['legend.loc'] = 'upper right'
    mpl.rcParams['legend.frameon'] = False
    mpl.rcParams['legend.facecolor'] = bg_color
    mpl.rcParams['legend.fontsize'] = 20

""" =================================
    Startup Function
================================= """

def defaults():

    # Initialize CSS Variables
    css_vars = load_css_vars(['../../shared/css/definitions.css',
                              'shared/css/defaults.css'])

    # Initialize Colors
    init_colors_n_fonts(css_vars)

    # Initialize Static Plots
    set_static_plots()

    # Output HTML File
    return stylize()
