#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Ariel Rodriguez

import logging 
#conexion a base de datos
user=""
password = ""
host=""
DBNAME=""
schema=""
tnsname=""
#maximo numero de transacciones por commit
CHUNK_LENGTH=1
#nivel de log
LOG_LEVEL=logging.DEBUG
#variables de entorno de cliente orcle
NLS_LANG=".WE8ISO8859P1"
LANG="es_ES.utf8"
LC_ALL="es_ES.utf8"