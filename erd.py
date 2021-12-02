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
#TABLES_TO_MERGE = [('chefmozcuisine', 'chefmozparking', 'placeID'),
#                   ('usercuisine', 'userpayment', 'userID'),]
TABLES_TO_MERGE = []
#TABLES_TO_GROUP = [('rating_final', 'service_rating'),
#                   ('chefmozaccepts', 'Rpayment'),]


class Table(object):
    def __init__(self, identifier, keylist=None):
        self.identifier = identifier
        self.keylist = keylist

    def merge(self, other, mergeKey, infix=" merged with "):
        newName = infix.join([self.identifier, other.identifier])
        return Table(newName, list(set(self.keylist + other.keylist)))

    @property
    def label(self):
        return r"\n".join([self.identifier, r"\n".join(self.keylist)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate an entity relationship diagram from files in a subdirectory')
    parser.add_argument(SUB_DIRECTORY_KEY, type=str, nargs=1,
                        help='relative path of subdirectory')
    #args = parser.parse_args(['csvfiles'])
    args = parser.parse_args()
    inputPath = os.path.join('.', getattr(args, SUB_DIRECTORY_KEY)[0], '*.csv')
    dot = graphviz.Digraph('ERD', format='png',
                           comment='Entity Relationship Diagram',
                           node_attr={'shape': 'box'})
    for key, value in GRAPH_ATTRIBUTES.items():
        dot.graph_attr[key] = value
    tableDict = {}
    for filename in glob.glob(inputPath):
        tableName = os.path.splitext(os.path.basename(filename))[0].upper()
        newTable = Table(tableName)
        with open(filename, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                newTable.keylist = list(row.keys())
                break
        tableDict[newTable.identifier] = copy(newTable)
    for left, right, mergeOn in TABLES_TO_MERGE:
        leftName = left.upper()
        rightName = right.upper()
        mergedTables = tableDict[leftName].merge(tableDict[rightName], mergeOn)
        tableDict[mergedTables.identifier] = mergedTables
        del tableDict[leftName]
        del tableDict[rightName]
    tables = list(tableDict.values())
    for table in tables:
        dot.node(table.identifier, label=table.label)
    for n, tailTable in enumerate(tables):
        for headTable in tables[n+1:]:
            for key in tailTable.keylist:
                if key in headTable.keylist:
                    dot.edge(tailTable.identifier, headTable.identifier)
    dot.render(directory='.')