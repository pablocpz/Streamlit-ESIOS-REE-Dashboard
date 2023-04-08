import streamlit as st
import pandas as pd
import plotly.express as px




def visualization(graphic_type, use_facets, dfviz):

    
    st.caption("Use full screen for better visualization")

    if dfviz.shape[0] != 0:

        
            if graphic_type == "bar" and use_facets == True:
                
                return px.bar(dfviz, x="datetime_utc", y="value", color="variable", 
                                    facet_col_wrap=2)
                
            
            elif graphic_type == "bar" and use_facets == False:
                return  px.bar(dfviz, x="datetime_utc", y="value", color="variable")
                    


            elif graphic_type == "area" and use_facets == True: #bar
                return px.area(dfviz, x="datetime_utc", y="value", color="variable",
                                facet_col="variable", facet_col_wrap=2)
            elif graphic_type == "area" and use_facets == False:
                return px.area(dfviz, x="datetime_utc", y="value", color="variable")

            # st.plotly_chart(fig, use_container_width=True)



             
            
            if graphic_type == "bar" and use_facets == True: #bar
            
                return px.bar(dfviz, x="datetime_utc", y="value", color="variable", 
                                facet_col="variable", facet_col_wrap=2)
            
        
            elif graphic_type == "bar" and use_facets == False: #bar
                return  px.bar(dfviz, x="datetime_utc", y="value", color="variable")
                

        #---

            elif graphic_type == "area" and use_facets == True: #area
                return px.area(dfviz, x="datetime_utc", y="value", color="variable",
                            facet_col_wrap=4)
            elif graphic_type == "area" and use_facets == False:
                return px.area(dfviz, x="datetime_utc", y="value", color="variable")

        #-
            elif graphic_type == "line" and use_facets == True: #line
                return px.line(dfviz, x="datetime_utc", y="value", color="variable",
                            facet_col="variable", facet_col_wrap=2)
            elif graphic_type == "line" and use_facets == False:
                return px.line(dfviz, x="datetime_utc", y="value", color="variable")

    
            #  st.plotly_chart(fig, use_container_width=True)



   


