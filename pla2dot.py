#!/usr/bin/env python
# encoding: utf8
# Author: Dennis Terhorst <d.terhorst@fz-juelich.de>
'''
Usage: convert [options] <excerpt> <dotfile>

Options:
    --rankdir=<dir>  either TB or LR [default: TB]
    -v, --verbose   tell what is going on
    -h, --help      print this text
'''

import docopt
import re

def readdata(filename):
    ' read the given file and parse the nodes and edges to python dicts '
    state = "outside"
    nodes = list()
    edges = list()
    keyname = re.compile(r'(\w*):')
    def line2dict(line):
        line = line[line.index("{"):line.index("}")+1]
        line = keyname.sub(r'"\1":', line)
        return eval(line)

    with open(filename) as infile:
        for line in infile:
            if state == 'outside':
                if "create an array with nodes" in line:
                    state = "nodes"
                elif "create an array with edges" in line:
                    state = "edges"
            elif state == 'nodes':
                if not all([brace in line for brace in '{}']):
                    state = 'outside'
                    continue
                nodes.append(line2dict(line))
            elif state == 'edges':
                if not all([brace in line for brace in '{}']):
                    state = 'outside'
                    continue
                edges.append(line2dict(line))
            else:
                raise NotImplementedError("state %s is not implemented" % repr(state))
            
    return nodes, edges

def rgb2html(r, g, b):
    return "#%02X%02X%02X" % (r,g,b)
def writedot(filename, nodes, edges, **options):
    ' write the given nodes and edges to a dot file '
    def graphopt(name):
        if name in options:
            return '    %s="%s"\n' % (name, options[name])
        return ''
    with open(filename, 'w') as outfile:
        outfile.write('digraph g {\n')
        outfile.write(graphopt('rankdir'))
        outfile.write('\n    // nodes\n')
        outfile.write('     node [style="filled" fontcolor="black" fontname="sans-serif" color="white" fillcolor="%s"]\n' % rgb2html(97,195,238))
        for node in nodes:
            sanitized = node.copy()
            sanitized['label'] = sanitized['label'].replace('"', r'\"')
            outfile.write('    node{id} [label="{label}"];\n'.format(**sanitized))
        outfile.write('\n    // edges\n')
        outfile.write('     edge [fontcolor="black" fontname="sans-serif" color="%s"]\n' % rgb2html(97,195,238))
        for edge in edges:
            outfile.write('    node{from} -> node{to};\n'.format(**edge))
        outfile.write('}\n')

def main():
    args = docopt.docopt(__doc__)
    verbose = args['--verbose']
    if verbose: print(args)

    nodes, edges = readdata(args['<excerpt>'])
    writedot(args['<dotfile>'], nodes, edges, rankdir=args['--rankdir'])

if __name__ == '__main__':
    main()
