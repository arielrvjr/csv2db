#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, getopt
import string
import dbimport

from datetime import date

__author__  = "Ariel Rodriguez"
__version__ = "1.1"
__date__    = "06/05/2017"


def main(argv):
    inputfile = ''
    columnfile = ''
    outputfile = ''
    table_name = ''
    dataFile = ''
    try:
        opts, args = getopt.getopt(argv,"ht:i:d:o:a:c:",["ifile=","logfile=","dfile=","adapter=","cfile="])
    except getopt.GetoptError:
        print 'Sintax: dbloader.py -a <adapter> -t <tablename> [-c <columnfile> -i <inputfile> -d <datafile> -o <logfile>]'
    
    for opt, arg in opts:
        if opt == '-h':
            print 'Sintax: dbloader.py -a <adapter> -t <tablename> [-c <columnfile> -i <inputfile> -d <datafile> -o <logfile>]'
            print ''
            print '<adapter> (required) Type of Adapter, can be "ORACLE" or "MYSQL"'
            #print 'Tipo de Adaptador, puede ser "ORACLE" o "MYSQL"'
            print '<tablename> (required) Name table to import data.'
            #print 'Archivo en formato CSV con los datos que se desean importar.'
            print '<columnfile> (optional) Text Plain File with each column name. Default Value: <tablename>.columns Example: id,name, age' 
            print '<inputfile> (optional) Text Plain File with each column format. Default Value: <tablename>.values Example: %s,%s,to_str(%s)' 
            print '<datafile>  (optional) CSV File that contain data to import. Default Value: <tablename>.csv'
            #print 'Archivo de texto plano con los valores de cada columna.'
            #print 'Si no se introduce este parametro se usa el valor por defecto <tablename>.csv'
            print '<logfile>   (optional) Log File that contain output information. Default Value: <tablename>.log'
            #print 'Nombre del archivo log que se genera al momento de la ejecuación.'
            #print 'Si no se introduce este parametro se usa el valor por defecto <tablename>.log'

            sys.exit()
        elif opt == '-t':
            table_name = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--logfile"):
            outputfile = arg
        elif opt in ("-d", "--dfile"):
            dataFile = arg
        elif opt in ("-a","--adapter"):
            if arg in ("ORACLE", "MYSQL"):
                adapter = arg
            else:
                raise Exception("not valid adapter")

    if table_name == '':
        print ''
        sys.exit(2)
    if inputfile == '':
        inputfile = table_name + '.values'
    if columnfile == '':
        columnfile = table_name + '.columns'
    if dataFile == '':
        dataFile = table_name + '.csv'
    if outputfile == '':
        outputfile = table_name + '.log'

    try:
        f_txt = open(inputfile, 'r')
        #values = "("+ tratar_values(f_txt.read()) +")"
        values = "("+ f_txt.read() +")"
        #print "Values: " + values
        f_txt.close()
    except Exception, e:
        print e.message
        print "Error reading <inputfile> ", inputfile
        sys.exit(2)

    try:
        f_txt = open(columnfile, 'r')
        #values = "("+ tratar_values(f_txt.read()) +")"
        columns = "("+ f_txt.read() +")"
        #print "Values: " + values
        f_txt.close()
    except Exception, e:
        print e.message
        print "Error reading <columnfile> ", columnfile
        columns= ""

    try:
        convert = dbimport.DbImport(adapter,dataFile,outputfile)
        convert.execute(table_name, columns,values)
    except Exception, e:
        print e.message
        sys.exit(2)
        
if __name__ == "__main__":
    main(sys.argv[1:])