#!/bin/python
__author__ = 'steve'

import csv
import argparse
import os
from from pyproj import Proj, transform

class Coord_Converter_Error(Exception):
    pass

class Point:
    ''' handles point objects '''

    def __init__(self,x,y,epsg=None):
        '''

        :param x: x coordinate
        :param y: y coordinate
        :param epsg: epsg code of spatial coordinate system
        :return: None
        '''
        self.x=x
        self.y=y
        self.epsg = epsg
        self.proj = None
        if self.epsg:
            self.set_epsg(self.epsg)
        return

    def set_epsg(self,epsg):
        '''function to set a projection without transformation'''
        self.epsg = epsg
        self.proj = Proj(init='epsg:%d' %epsg)
        return

    def transform(self,epsg):
        '''transforms x and y to new coordinate system and returns result'''
        return transform(self.proj,Proj(init='epsg%d' %epsg),self.x,self.y)

    def transform_and_set(self,epsg):
        '''transforms coordinates and sets point to new system'''
        self.x, self.y = self.transform(epsg)
        self.epsg = epsg
        self.proj = Proj(init='epsg%d' %epsg)
        return

if __name__=='__main__':
    '''tool execution when run as command line script'''
     # create an argparse and set up command line arguments
    parser = argparse.ArgumentParser(description="Convert coordinates in a csv file to a new coordinate system")
    parser.add_argument('-i', '--input', type=str, help='CSV file')
    parser.add_argument('-x','--x', type=str, help='Field of X coordinate')
    parser.add_argument('-y','--y', type=str, help='Field of Y coordinate')
    parser.add_argument('-s','--s_srs',type=int, help='EPSG Code of input coordinates')
    parser.add_argument('-t','--t_srs',type=int, help='EPSG Code of output coordinates')
    parser.add_argment('-o','--output',type=str,default='outfile.csv',,help='Output File')
    args = parser.parse_args()

    #error checks
    if not os.path.exists(args.input):
        raise Coord_Converter_Error("Input File Does Not Exist")

    if os.path.exists(args.output):
        print "Warning: Output File %s will be overwritten" % args.output

    csv_reader = csv.DictReader(open(args.input,'wb'))

    if not args.x in csv_reader.fieldnames:
        raise Coord_Converter_Error("Column %s not Found in input file" %args.x)

    if not args.y in csv_reader.fieldnames:
        raise Coord_Converter_Error("Column %s not Found in input file" %args.y)

    csv_writer = csv.DictWriter(open(args.output,'wb'), fieldnames=csv_reader.fieldnames)

    for row in csv_reader:
        p = Point(row[args.x],row[args.y],args.s_srs)
        row['x'+_args.t_srs], ,row['y'+_args.t_srs] =  p.transform(args.t_srs)
        csv_writer.writerow(row)

