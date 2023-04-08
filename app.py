import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config("Esios Ree Dashboard", page_icon="📊", initial_sidebar_state="expanded")
st.caption("For indicator info, see: https://airtable.com/shr3E7NdkChNqQ4Eu/tbl79pOcXNgAR8JBc")
st.sidebar.title("Welcome to ESIOS REE DASHBOARD :bar_chart:")
st.sidebar.write("#")

from api_utils import indicator_data
from visualization import visualization

genSection = st.container()
vizSection = st.container()
priceSection = st.container()

mainSection = st.container()



action = st.sidebar.radio("Select what to visualize:", ("Generation Data", "Price Data"))

if action == "Generation Data":
        
        with genSection:
            st.title("GENERATION DATA")

            genForm = st.sidebar.form(key="genform")
            
            with genForm:
                indicator = st.multiselect("Enter the indicator/s", options=[x for x in range(1, 100000)], default=84)
                
                start_date = st.date_input("Enter the start date:", max_value=datetime.today().date())
                end_date = st.date_input("Enter the end date", max_value=datetime.today().date())
                group = st.selectbox("Select how to group data", ("hour", "day", "week", "month", "year"))
                graphic_type = st.selectbox("Select type of graphic", ("bar", "area"))
                use_facets = st.checkbox("Use Facets")
                submit = st.form_submit_button("Submit")

            if submit:
                #check if first date is older than the second one and both are lower or equal to the actual date:
                df = indicator_data("generation", indicator, start_date, end_date, group)
                
                if df.shape[0] != 0:
                    fig = visualization(graphic_type, use_facets, df)
                    st.plotly_chart(fig, use_container_width=True)
                
                
                

elif action == "Price Data":

        with priceSection:
                st.title("PRICE DATA")
                priceForm = st.sidebar.form(key="priceform")
                
                with priceForm:
                    indicator = st.multiselect("Enter the indicator/s", options=[x for x in range(1, 100000)], default=84)
                    start_date = st.date_input("Enter the start date:", max_value=datetime.today().date())
                    end_date = st.date_input("Enter the end date", max_value=datetime.today().date())
                    group = st.selectbox("Select how to group data", ("hour", "day", "week", "month", "year"))
                    graphic_type = st.selectbox("Select type of graphic", ("line", "area", "bar"))
                    use_facets = st.checkbox("Use Facets")
                    submit = st.form_submit_button("Submit")

                if submit:
                    #check if first date is older than the second one and both are lower or equal to the actual date:
                    df = indicator_data("price", indicator, start_date, end_date, group)
                    
                    if df.shape[0] != 0:
                          fig = visualization(graphic_type, use_facets, df)
                          st.plotly_chart(fig, use_container_width=True)