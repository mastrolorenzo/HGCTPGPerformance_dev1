#! /usr/bin/env python

import pandas as pd
import rootpy.ROOT as ROOT

def main(input_file, output_file):
    print 'Input file: ',input_file
    print 'output file: ',output_file
    print ' --> execution of the resolution analysis'
    resolution(input_file, output_file).plotResponse()
        
    return

if __name__=='__main__':
    import sys
    from hgc_tpg.resolution.resolution import *

    import optparse
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--input', dest='input_file', help='Input file')
    parser.add_option('--output', dest='output_file', help='Output file')
    (opt, args) = parser.parse_args()
    if not opt.input_file :
        parser.print_help()
        print 'Error: Missing input file name'
        sys.exit(1)
    if not opt.output_file :
        parser.print_help()
        print 'Error: Missing output file name'
        sys.exit(1)
    main(opt.input_file, opt.output_file)

