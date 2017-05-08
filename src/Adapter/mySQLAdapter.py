#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Ariel Rodriguez
from .abstractAdapter import AbstractAdapter
import MySQLdb
import logging
import settings

class MySQLAdapter(AbstractAdapter):
    def __init__(self):
        "Constructor de MySQLAdapter"
        AbstractAdapter.__init__(self)
        self.logger = logging.getLogger(__name__)

    def connect(self):
        """Try to connect with mysql driver if have anything error raise that."""
        try:
            datos = [settings.config.host, settings.config.user, settings.config.password, settings.config.dbname] 
            self.logger.debug("Connection String:{}, {}, {}".format(settings.config.host, settings.config.user, settings.config.dbname) )
            self.con = MySQLdb.connect(*datos) # Conectar a la base de datos 
            self.set_env_variable(settings.config.NLS_LANG, settings.config.LANG, settings.config.LC_ALL);
        except Exception as e:
            code,message = e
            if code == 1045:
                raise Exception(self.REVISAR_CREDENCIALES)
            else:    
                raise e 

    def disconnect(self):
        """Disconnect from the database."""
        try:
            self.con.close()
        except Exception as e:
            raise e
        