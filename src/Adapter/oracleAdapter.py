import cx_Oracle
import os
import settings
class OracleAdapter(AbstractAdapter):
    "Clase que representa al adaptador de Oracle"

    def __init__(self):
        "Constructor de OracleAdapter"
        # llamamos al constructor de AbstractAdapter
        AbstractAdapter.__init__(self)

    def connect(self):
        """Try to connect with oracle driver if have anything error raise that."""
        try:
            self.logging.debug("Cadena de Conexion:")
            if len(settings.config.tnsname) == 0:
                connection_string = settings.config.user+"/"+ settings.config.password + "@" + settings.config.host + "/" + settings.config.dbname
                self.logging.debug(connection_string)
                self.con = cx_Oracle.connect(connection_string)
            else:
                self.logging.debug(settings.config.user+"/"+settings.config.password + ":" + settings.config.tnsname)
                self.con = cx_Oracle.connect(settings.config.user, settings.config.password, settings.config.tnsname)

            self.set_env_variable(settings.config.NLS_LANG, settings.config.LANG, settings.config.LC_ALL);
        except cx_Oracle.DatabaseError as e:
            raise e
            #error, = e.args
            # if error.code == 1017:
            #   self.logging.error(self.REVISAR_CREDENCIALES)
            # else:
            #   self.logging.error(e)

    def disconnect(self):
        """Disconnect from the database. If this fails, for instance
        if the connection instance doesn't exist we don't really care.
        """
        try:
            self.con.close()
        except cx_Oracle.DatabaseError as e:
            raise e

    