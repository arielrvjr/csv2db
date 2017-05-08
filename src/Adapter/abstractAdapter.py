#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Ariel Rodriguez
import logging
import os
import settings

F_NULL = "TO_DATE('31/12/2999','dd/MM/YYYY')"

class AbstractAdapter:
	NO_CONECTADO = "There is no connection to the database."
	CONECTANDO = "Connecting..."
	CURSOR_OBTENIDO = "Cursor Obtained"
	REVISAR_CREDENCIALES = "Please check your credentials."

	def __init__(self):
		self.con = 0
		self.logger = logging.getLogger(__name__)
		self.logger.info(self.CONECTANDO)
		self.connect()

	def connect(self):
		raise NotImplementedError

	def disconnect(self):
		raise NotImplementedError

	def is_connect(self):
		if self.con:
			return True
		else:
			return False
	
	def getTypes(self,schema,tableName):
		db_types = []
		if self.is_connect():
			db_types_cur = self.con.cursor()
			db_types_cur.execute("select * from {}.{}".format(schema,tableName) )
			print db_types_cur.description
			db_types = (d[1] for d in db_types_cur.description)
			db_types_cur.close()
		return db_types

	def execute(self, tableName, columns,values, data):
		if self.is_connect():
			try:
				cur = self.con.cursor()
				self.logger.info(self.CURSOR_OBTENIDO)
				cur.bindarraysize = settings.config.CHUNK_LENGTH
				#db_types = self.getTypes(settings.config.schema, tableName)
				# cur.setinputsizes(*db_types)
				insrt = []
				insrt = [data[i:i+settings.config.CHUNK_LENGTH] for i in range(0,len(data),settings.config.CHUNK_LENGTH)]
				# cur.prepare("insert into "+ settings.config.schema +"." + tableName + " values " + values)
				#self.logger.debug(cur.bindnames())
				for row in insrt:
					try:
						query = "INSERT INTO {}.{} {} VALUES {} ".format(settings.config.schema,tableName, columns,values)
						cur.executemany(query, row)
						self.con.commit()
					except Exception as e:
						self.con.rollback()
						self.logger.error("Insert Error")
						self.logger.error(e)

				self.logger.info("Total imported rows: {}".format(cur.rowcount) )
				cur.close()
				
			except Exception as e:
				self.logger.error(e)
			finally:
				self.disconnect()
		else:
			self.logger.error(self.NO_CONECTADO)

	def set_env_variable(self,NLS_LANG, LANG, LC_ALL):
		os.environ["NLS_LANG"] = NLS_LANG
		os.environ["LANG"] = LANG
		os.environ["LC_ALL"] = LC_ALL

	def tratar_numero(num):
	    #print "before tratar_numero " + str(num)
	    if num < 10:
	        num = '0' + str(num)
	    else:
	        num = str(num)
	    #print "after tratar_numero " + num
	    return num

	def tratar_values(text):
	    mTxt =text

	    if 'F_NULL' in mTxt:
	        #print "before F_NULL in " + mTxt
	        mTxt = string.replace(mTxt,"F_NULL", F_NULL)
	        #print "after F_NULL in " + mTxt
	    if 'SYSDATE' in mTxt:
	        #print "before SYSDATE in " + mTxt
	        today = date.today()
	        #print today
	        mTxt = string.replace(mTxt,"SYSDATE", "TO_DATE('"+ tratar_numero(today.day) + "/" + tratar_numero(today.month) + "/" + tratar_numero(today.year)  +"','dd/MM/YYYY')")
	        #print "after SYSDATE in " + mTxt
	    return mTxt