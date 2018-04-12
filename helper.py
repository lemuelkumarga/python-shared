import defaults as _d

""" =================================
    Caching Functions
================================= """
_d.load({"pck":"pickle",
         "os":"os"},
         globals())

__cache_folder = "cache/"

def cache(fun, name, override=False):
	
	filename = __cache_folder + name + ".pkl"
	
	if (os.path.isfile(filename)):
	    with open(filename, 'rb') as f:
	        tmp = pck.load(f)
	        f.close()
	else:
	    tmp = fun()
	    with open(filename, 'wb') as f:
	        pck.dump(tmp, f, pck.HIGHEST_PROTOCOL)
	        f.close()
	
	return tmp