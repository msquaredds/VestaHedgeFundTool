
import streamlit as st

from VestaHedgeFundTool import BasicPageSetup


def main():
    BasicPageSetup.basic_page_setup()

    st.warning("This page is just a test page for now.")


if __name__ == '__main__':
    main()
