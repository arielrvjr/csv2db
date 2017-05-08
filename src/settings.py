#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Ariel Rodriguez

import ConfigParser
import config
import base64
try:
    settings = ConfigParser.ConfigParser()
    settings.read("config.ini")
except Exception, e:
    print e

if settings:
    #database config
    if settings.get("DB","user"):
        config.user = settings.get("DB","user")
    if settings.get("DB","password"):
        config.password = base64.b64decode(settings.get("DB","password"))
    if settings.get("DB","host"):
        config.host = settings.get("DB","host")
    if settings.get("DB","DBNAME"):
        config.dbname = settings.get("DB","DBNAME")
    if settings.get("DB","schema"):
        config.schema = settings.get("DB","schema")
    if settings.get("DB","TNSNAME"):
        config.tnsname = settings.get("DB","TNSNAME")
    #transactions
    if settings.get("TRANSACTION","CHUNK_LENGTH"):
        config.CHUNK_LENGTH = int(settings.get("TRANSACTION","CHUNK_LENGTH"))
    #LOG LEVEL
    if settings.get("LOG","LOG_LEVEL"):
        config.LOG_LEVEL =settings.get("LOG","LOG_LEVEL")
    #ENVIRONMENT
    if settings.get("ENVIRONMENT","NLS_LANG"):
        config.NLS_LANG =settings.get("ENVIRONMENT","NLS_LANG")
    if settings.get("ENVIRONMENT","LANG"):
        config.LANG =settings.get("ENVIRONMENT","LANG")
    if settings.get("ENVIRONMENT","LC_ALL"):
        config.LC_ALL =settings.get("ENVIRONMENT","LC_ALL")
