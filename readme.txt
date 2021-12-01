Call with

python erd.py csvfiles

where 'csvfiles' is the relative path of the directory containing the input files


If you want to change the layout or other attributes of the graph (such as whether the edges are straight or curved) modify the dictionary at the top of the file that looks like this:

 GRAPH_ATTRIBUTES = {'splines': "ortho",
                    'esep': '20',
                    'nodesep': '1'}

The list of available graph attributes is at https://graphviz.org/doc/info/attrs.html