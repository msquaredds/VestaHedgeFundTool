"""
Tools for accessing a database and pulling or pushing data.

:class DBTools: Tools for accessing a database and pulling or pushing
    data.
"""

from VestaHedgeFundTool import GlobalVariables as vhft_gv

import logging

from mysql import connector


class DBTools(object):
    """
    Tools for accessing a database and pulling or pushing data.

    :method build_con: Builds a connection to the MySQL database.
    """

    def __init__(self, profile: str = 'sec_master', host: str = None,
                 user: str = None, password: str = None) -> None:
        """
        :param profile: The MySQL profile to use, this is equivalent to
            database in the MySQL lingo.
        :param host: The host name of the MySQL server
        :param user: The username
        :param password: The password
        """
        self.logger = logging.getLogger('main_logger')

        self.profile = profile
        self.host = host
        self.user = user
        self.password = password

    def build_con(self) -> connector.connection.MySQLConnection:
        """
        Builds a connection to the MySQL database.
        :return: A connection to the MySQL database.
        """

        p = {'host': self.host,
             'user': self.user,
             'password': self.password}

        # get the profile
        for k, v in vhft_gv.DATABASE_PROFILES.items():
            if k == self.profile:
                p['database'] = v
                break

        # let the user know if it fails
        if self.profile not in vhft_gv.DATABASE_PROFILES:
            log_str = (f"*******************Error*******************\n"
                       f"The 'profile' attribute must be either "
                       f"'sec_master', 'rosetree', 'adr' or 'REIT'. If you "
                       f"would like to add a new profile, please contact the "
                       f"code admin.")
            self.logger.exception(log_str)
            raise ValueError(log_str)

        return connector.connect(**p)
