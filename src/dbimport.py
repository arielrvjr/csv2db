#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Ariel Rodriguez
import csv
import logging
import logging.config

import settings
import importlib


CSV_LEIDO = "CSV file has been read"
LEYENDO_CSV = "Open CSV:"


#definimos variables de lenguaje
__author__  = "Ariel Rodriguez"
__version__ = "1.1"
__date__    = "06/05/2017"

class DbImport:

    def __init__(self,driver,csv_file, outputfile):
        logging.config.fileConfig('logging.ini')

        handler = logging.FileHandler(outputfile, mode='w')
        handler.setLevel(settings.config.LOG_LEVEL)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)

        self.logger = logging.getLogger(__name__)
        self.rows = []
        if driver == "ORACLE":
            importado = getattr(importlib.import_module("Adapter.oracleAdapter"),"OracleAdapter")
        elif driver == "MYSQL":
            importado = getattr(importlib.import_module("Adapter.mySQLAdapter"),"MySQLAdapter")
        self.driver = importado()
        try:
            self.logger.info(LEYENDO_CSV + csv_file)
            with open(csv_file, 'rb') as f:
                reader = csv.reader(f, delimiter=",")
                self.rows = list(reader)
            self.logger.info(CSV_LEIDO)
        except Exception, e:
            self.logger.error(e)   

    def has_data(self):
        if len(self.rows):
            return True
        else:
            return False
           
    def execute(self,tableName,columns, values):
        self.logger.debug("Call execute function with tableName {} and values {}".format(tableName,values))
        self.driver.execute(tableName,columns,values,self.rows)


