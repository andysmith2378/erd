import argparse
import csv
import glob
import graphviz
import os

from copy import copy

SUB_DIRECTORY_KEY = 'subdirectory'
GRAPH_ATTRIBUTES = {'splines': "ortho",
                    'esep': '20',
                    'nodesep': '1'}


class Table(object):
    def __init__(self, identifier, keylist=None):
        self.identifier = identifier
        self.keylist = keylist

    @property
    def label(self):
        return r"\n".join([self.identifier, r"\n".join(self.keylist)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate an entity relationship diagram from files in a subdirectory')
    parser.add_argument(SUB_DIRECTORY_KEY, type=str, nargs=1,
                        help='relative path of subdirectory')
    args = parser.parse_args(['csvfiles'])
    inputPath = os.path.join('.', getattr(args, SUB_DIRECTORY_KEY)[0], '*.csv')
    dot = graphviz.Digraph('ERD', format='png',
                           comment='Entity Relationship Diagram',
                           node_attr={'shape': 'box'})
    for key, value in GRAPH_ATTRIBUTES.items():
        dot.graph_attr[key] = value
    tables = []
    for filename in glob.glob(inputPath):
        tableName = os.path.splitext(os.path.basename(filename))[0].upper()
        newTable = Table(tableName)
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                newTable.keylist = list(row.keys())
                break
        tables.append(copy(newTable))
        dot.node(newTable.identifier, label=newTable.label)
    for n, tailTable in enumerate(tables):
        for headTable in tables[n+1:]:
            for key in tailTable.keylist:
                if key in headTable.keylist:
                    dot.edge(tailTable.identifier, headTable.identifier)
    dot.render(directory='.')