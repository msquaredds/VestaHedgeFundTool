"""
Defines all the info around a particular manager.

:class ManagerPool: Define the set of managers that we want to look at.
"""

from VestaHedgeFundTool import DBTools
from VestaHedgeFundTool import GlobalVariables as vhft_gv

import logging


class ManagerPool(object):
    """
    Define the set of managers that we want to look at.
    """

    def __init__(self, managers: list = None, most_recent: bool = False,
                 **kwargs)\
            -> None:
        """
        :param managers: The set of managers in our pool.
        :param most_recent: Whether we want just the most recent managers
            in the portfolio.
        :param kwargs: Currently used for connecting to a database and so
            should be a dictionary with the following keys: 'user',
            'password'.
        """
        self.logger = logging.getLogger('main_logger')

        self.most_recent = most_recent
        for k, v in kwargs.items():
            setattr(self, k, v)
        # load the manager list if one is not provided
        self.managers = self._get_all_mgrs() if managers is None else managers

    def _get_all_mgrs(self) -> list:
        """
        Get all the managers in the database.
        :return mgr_list: A list of all the managers in the database
            with each as a tuple of (fund name, whether in portfolio)
            where in portfolio = 1 if in portfolio, 0 if not.
        """

        # make sure we can connect to the database
        if not hasattr(self, 'user') or not hasattr(self, 'password'):
            log_str = (f"*******************Error*******************\n"
                       f"You must provide a 'user' and 'password' "
                       f"attribute to the ManagerPool class to use it.")
            self.logger.exception(log_str)
            raise ValueError(log_str)

        # connect to the database
        con_engine = DBTools(profile=vhft_gv.SUPERINVESTOR_DB_INFO['database'],
                             host=vhft_gv.SUPERINVESTOR_DB_INFO['host'],
                             user=self.user, password=self.password)
        con = con_engine.build_con()
        cur = con.cursor()

        # get the list of managers or raise an error if it fails
        try:
            sql = 'SELECT fund, inPort ' \
                  'FROM superinvestor.investors;'
            cur.execute(sql)
            mgrs = cur.fetchall()
        except Exception as e:
            self.logger.exception('Error getting managers: %s' % e)
            raise e

        # only pull the managers in the portfolio if we want
        if self.most_recent:
            mgr_list = [(x[0], x[1]) for x in mgrs if x[1] == 1]
        else:
            mgr_list = [(x[0], x[1]) for x in mgrs]

        # clean up the connection
        cur.close()
        con.close()

        return mgr_list

    def pretty_mgr_names(self, sort: str = 'portfolio',
                         include_portfolio: bool = True) -> list:
        """
        Get the pretty names of the managers in the pool.
        :param sort: Whether to sort the managers by whether they're in
            the portfolio or alphabetically (in the portfolio then
            sub-sorts alphabetically). Takes 'portfolio' or 'alphabetic'.
        :param include_portfolio: Whether to include if the fund is in
            the portfolio.
        :return pretty_mgr_list: A list of the pretty names of the
            managers in the pool.
        """

        # first make sure the list is sortable by replacing nulls with
        # zeroes and then sort the managers
        mgr_list = [[x[0], x[1]] if x[1] == 1 else [x[0], 0]
                    for x in self.managers]
        if sort == 'portfolio':
            sorted_mgr_list = sorted(mgr_list, key=lambda x: (-x[1], x[0]))
        elif sort == 'alphabetic':
            sorted_mgr_list = sorted(mgr_list, key=lambda x: x[0])
        else:
            log_str = (f"*******************Error*******************\n"
                       f"The sort variable must be either 'portfolio' or "
                       f"'alphabetic'.")
            self.logger.exception(log_str)
            raise ValueError(log_str)

        pretty_mgr_list = []
        for mgr in sorted_mgr_list:
            # format the name as the fund name in natural case plus
            # whether it's in the portfolio, if we want that
            if include_portfolio:
                pretty_mgr = mgr[0].title() + ' ' +\
                             ('(in portfolio)' if mgr[1] == 1
                              else '(not in portfolio)')
                pretty_mgr_list.append(pretty_mgr)
            else:
                pretty_mgr_list.append(mgr[0].title())

        return pretty_mgr_list
