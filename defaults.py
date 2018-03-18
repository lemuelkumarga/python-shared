
""" =================================
    Load Packages
================================= """
failed_loads = set()
failed_loads_sub = set()
'''
@input packages a list of key value pairs, where:
                key is the alias of the module
                value is the name of the module itself
@input subpackages a list of key value pairs, where:
                   key is the alias of the submodule
                   value is the name of the submodule itself
'''
def load(packages, subpackages):

    global failed_loads;
    global failed_loads_sub;

    for k, v in packages.items():
        try:
            globals()[k] = __import__(v)
        except ImportError:
            failed_loads.add(v)
            
    for k, v in subpackages.items():
        try: 
            exec("globals()['"+k+"'] = " + v)
        except NameError:
            failed_loads_sub.add(v)
            pass;


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

    # Print uninstalled packages
    if (len(failed_loads) > 0):
        failed_str = ""
        for p in failed_loads:
            failed_str += p + " "
        print("Some modules don't exist. Please install on terminal using: sudo pip install " + failed_str)
        return;

    # Print unloaded subpackages
    if (len(failed_loads_sub) > 0):
        failed_str = ""
        for p in failed_loads_sub:
            failed_str += p + ", "
        print("Failed to load the following submodules: " + failed_str[:-2])
        return;

    # Initialize pyplot notebook
    plot.init_notebook_mode(connected=True)

    # Output HTML File
    return stylize()
