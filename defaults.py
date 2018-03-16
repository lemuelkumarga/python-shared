
""" =================================
    Load Packages
================================= """

'''
@input packages a list of key value pairs, where:
                key is the alias of the module
                value is the name of the module itself
@input subpackages a list of key value pairs, where:
                   key is the alias of the submodule
                   value is the name of the submodule itself
'''
def load(packages, subpackages):
    uninstalled_str = ""
        
    for k, v in packages.items():
        try:
            globals()[k] = __import__(v)
        except ImportError:
            uninstalled_str += v + " "
            pass;

    if (uninstalled_str != ""):
        print("Some modules doesn't exist. Please install on terminal using: sudo pip install " + uninstalled_str);
    
    for k, v in subpackages.items():
        exec("globals()['"+k+"'] = " + v)


""" =================================
    Load Header (CSS + JS) Files
================================= """

load({"ip" : "IPython"},
     {"HTML" : "ip.core.display.HTML"})

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
    Startup Function
================================= """

load({"py" : "plotly"},
     {"plot" : "py.offline"})

def defaults():

    # Initialize pyplot notebook
    plot.init_notebook_mode(connected=True)

    # Output HTML File
    return stylize()
