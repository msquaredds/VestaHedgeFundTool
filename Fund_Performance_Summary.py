"""
This is the entry point for running the full program.

The program will run a Streamlit web app that will allow the user to see
metrics, charts and other interesting information about hedge funds.
"""

from VestaHedgeFundTool import BasicPageSetup

import logging


def main():
    # set up logger
    logger = logging.getLogger('main_logger')

    # the first output is a chart showing the fund's performance over time
    # versus other important benchmarks, such as the fund's listed
    # benchmark, the S&P 500, the JPN Global Agg Bond Index, the model of
    # the fund, etc.


if __name__ == '__main__':
    BasicPageSetup.basic_page_setup()
    BasicPageSetup.user_selection_fund()

    main()
