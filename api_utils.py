import json
import requests
import pandas as pd
import streamlit as st
from datetime import datetime
from functools import reduce

with open ('credentials.json', 'r') as f:
            headers = json.load(f)


def process_indicator(action, indicator, start_date, end_date, time_trunc, time_agg='sum'):

    
    """
    action --> 'generation' for getting electric generation data or 'price' for electric price values
    indicator --> unique id for the energy technology
    start_date, end_date --> time range for the data
    time_trunc --> type of data agrupation (hour, day, month, year)
    time_agg --> register joins (sum by default)
    
    * FOR GENERATION DATA: Returns the dataframe with the desired indicator energy generation data at a specific time range where each register represents a (hour/month/year)
    
    * FOR PRICE DATA: Returns the dataframe with the desired indicator energy price data at a specific time range where each register represents a (hour/month/year)
    """
    
    with open ('credentials.json', 'r') as f:
            headers = json.load(f)

    if start_date < end_date and start_date <= datetime.today().date() and end_date <= datetime.today().date():
         
        if action == "generation": #user want to get generation data:
            
            url = f"https://api.esios.ree.es/indicators/{indicator}?start_date={start_date}&end_date={end_date}&time_trunc={time_trunc}&time_agg={time_agg}"

            res = requests.get(url, headers=headers)

            data = res.json() #convertimos la data a .json
      
            if "indicator" not in data: #if there is not register (bad indicator id)
                st.warning("Invalid indicator ID")
                return pd.DataFrame()

            # else:
                
            #     df = pd.DataFrame(data['indicator']['values'])

            #     col_name = data['indicator']['short_name']

            #     df = df.rename({'value':col_name}, axis=1)

            #     df.datetime_utc = pd.to_datetime(df.datetime_utc, format='mixed') # dayfirst=True
 
            #     df = df[[col_name, 'datetime_utc']] 
    
            #     df = df.set_index('datetime_utc')

            #     if df.shape[0] == 0: #data doesn´t exist
            #         st.warning("Data not found")
            #         return pd.DataFrame()

            #     else:     
            #         return df.loc[f'{start_date}' : f'{end_date}']

            else:
                        
                    df = pd.DataFrame(data['indicator']['values'])
                    col_name = data['indicator']['short_name']
                    df = df.rename({'value': col_name}, axis=1)
            
                    try:
                        df['datetime_utc'] = pd.to_datetime(df['datetime_utc'], format='mixed')  # dayfirst=True if needed
                    except Exception as e:
                        st.warning(f"Date parsing error: {e}")
                        return pd.DataFrame()
            
                    df = df[[col_name, 'datetime_utc']]
                    df = df.set_index('datetime_utc')
            
                    if df.shape[0] == 0:  # Check if data doesn't exist
                        st.warning("Data not found")
                        return pd.DataFrame()
                    else:
                        return df.loc[start_date: end_date]
                        
                    elif action == "price": #otherwise, user want to see energy prices:
            
            
            url = f"https://api.esios.ree.es/indicators/{indicator}?start_date={start_date}T00:00&end_date={end_date}T23:59&time_trunc={time_trunc}&time_agg={time_agg}"

            res = requests.get(url, headers=headers)

            
            data = res.json() #convertimos la data a .json
           


            if "indicator" not in data: #if there is not register (bad indicator id)
                st.warning("Invalid indicator ID")
                return pd.DataFrame()

            else:
                df = pd.DataFrame(data['indicator']['values'])

                col_name = data['indicator']['short_name']

                df = df.rename({'value':col_name}, axis=1)

                df.datetime_utc = pd.to_datetime(df.datetime_utc)

                df = df[[col_name, 'datetime_utc']] 

                df = df.set_index('datetime_utc')

                if df.shape[0] == 0: #data doesn´t exist
                    st.warning("Data not found")
                    return pd.DataFrame()

                else:      

                    return df
                
            
        else:
            print("Select a valid action (price/generation) data")

    else:
         st.warning("Invalid Date Range")
         st.caption("Make sure the first date is older than the second!")
         return pd.DataFrame()




def indicator_data(action, indicators, start_date, end_date, time_trunc):
     
     if len(indicators) == 1: #the user only wants to visualize one indicator:
           
        df = process_indicator(action="generation", indicator=indicators[0],
                                start_date=start_date, end_date=end_date, time_trunc=time_trunc)
                  
        
        if df.shape[0] != 0: #-------------------

                    if time_trunc == "hour": #ensure that register are grouped as user wants
                         df = df.resample('1H').sum() 
                    elif time_trunc == "day":
                         df = df.resample("1D").sum()
                    elif time_trunc == "week":
                         df = df.resample("1W").sum()   
                    elif time_trunc == "month":
                         df = df.resample("1M").sum()  
                    elif time_trunc == "year":
                         df = df.resample("1Y").sum()

                    #for generation data, sort values, for price data, leave normal distribution
                    if action == "generation":
                        dfviz = df.melt(ignore_index=False).reset_index()
                        dfviz = dfviz.sort_values("value",ascending=False)

                    elif action == "price":
                        dfviz = df.melt(ignore_index=False).reset_index()
                    
                    return dfviz

        else:
              return pd.DataFrame()
        
     elif len(indicators) > 1: #otherwise, user want to visualize more than one indicator at the same time:
                
             
                data_list = []
                


                for indicator in indicators:
                        
                    data = process_indicator(action="generation", indicator=indicator, start_date=start_date,
                                            end_date=end_date, time_trunc=time_trunc) 
                    
                    if data.shape[0] != 0: 
                        
                        data_list.append(data)
                        
                    else:
                         st.error(f"Indicator {indicator} is an invalid ID or it hasn't no data")
                         return pd.DataFrame()
                        
                try:
                
                    df = pd.concat(data_list, axis=1)
                   
                    


                except:
                        

                        df = reduce( #we'll join each dataframe
                                    lambda left,right:
                                        pd.merge(left,right,left_index=True, right_index=True, how='outer'),
                                    data_list
                                ) #!  
                        df = df.fillna(0)
                        df = df.drop_duplicates()
                


                if time_trunc == "hour": #ensure that register are grouped as user wants
                         df = df.resample('1H').sum() 
                elif time_trunc == "day":
                        df = df.resample("1D").sum()
                elif time_trunc == "week":
                        df = df.resample("1W").sum()   
                elif time_trunc == "month":
                        df = df.resample("1M").sum()  
                elif time_trunc == "year":
                        df = df.resample("1Y").sum()

                if action == "generation":
                    dfviz = df.melt(ignore_index=False).reset_index()
                    dfviz = dfviz.sort_values("value",ascending=False)
                elif action == "price":
                     dfviz = df.melt(ignore_index=False).reset_index()
                
                return dfviz
                
    








