"""
This defines some basic Streamlit setup that is reused across multiple
pages.

:method basic_page_setup: This function will set up the basic page layout.
:method user_selection_fund: This function will allow the user to select a
    fund from a drop-down menu. It will then return the fund's name and
    the fund's ticker.
"""

from VestaHedgeFundTool import GlobalVariables as vhft_gv
from VestaHedgeFundTool import ManagerPool

import streamlit as st


def basic_page_setup():
    """
    This function will set up the basic page layout.
    """

    # set up the page
    st.set_page_config(page_title="Vesta Hedge Fund Tool", layout="wide")

    # give the user basic info about the tool
    # formatting done with css/html
    col1_title, col2_title, col3_title = st.columns(3)
    with col2_title:
        title_writing = "Vesta Hedge Fund Tool"
        title_format = f'<p style="text-align: center; font-family: ' \
                       f'Arial; color: #808080; font-size: 40px; ' \
                       f'font-weight: bold;">{title_writing}</p>'
        st.markdown(title_format, unsafe_allow_html=True)


def user_selection_fund():
    """
    This function will allow the user to select a fund from a drop-down
    menu. It will then return the fund's name and the fund's ticker.
    """

    # get the set of possible funds
    manager_pool_recent = st.sidebar.radio("Would you like to see all funds "
                                           "or just the funds currently in "
                                           "the portfolio?", ["All Funds",
                                                              "Portfolio"])
    if manager_pool_recent == "All Funds":
        most_recent = False
    else:
        most_recent = True
    mgr_engine = ManagerPool(most_recent=most_recent,
                             user="alex",
                             password="msquaredds2022")

    # we first sort to make this easier to read for the user
    if manager_pool_recent == "All Funds":
        with st.sidebar.expander("Change sort order"):
            sort_order = st.radio("Sort by",
                                  ["In Portfolio, Then Alphabetic",
                                   "Just Alphabetic"],
                                  label_visibility="collapsed")
    if 'sort_order' not in locals() or\
            sort_order == "In Portfolio, Then Alphabetic":
        sort_order = 'portfolio'
    else:
        sort_order = 'alphabetic'

    # determine whether to include a qualifier for whether in portfolio
    if manager_pool_recent == "Portfolio":
        include_portfolio = False
    else:
        include_portfolio = True

    # get the user selection for specific fund
    # saved as a global variable so it can be used across tabs
    pretty_mgr_list = mgr_engine.pretty_mgr_names(sort=sort_order,
                                                  include_portfolio=include_portfolio)
    vhft_gv.USER_SELECTION_FUND = st.sidebar.selectbox("Which fund would you "
                                                       "like to look at?",
                                                       pretty_mgr_list)
