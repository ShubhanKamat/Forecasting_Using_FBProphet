# importing the necessary modules and libraries
import subprocess

# Define the package you want to install
package = 'fbprophet'
subprocess.check_call(['pip', 'install', 'numpy'])
subprocess.check_call(['pip', 'install', 'pandas'])

# Run the pip command to install the package
subprocess.check_call(['pip', 'install', package])

import sys
import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
from Source.exception import CustomException
from Source.logger import logging
#Title of the page
st.title('Stock Forecasting using FBProphet')

#This line is to create the text box for entering the ticker, ticker gets saved in the 'selected_stock' variable
selected_stock = st.text_input('Enter the ticker for the stock (e.g. AAPL)')

#These lines take the input from the user for start and dates
start_date = st.date_input("Start date")
end_date = st.date_input("End date")

#This helper function will check for leap years
def count_leap_years(start_date, end_date):
    count = 0
    for year in range(start_date.year, end_date.year+1):
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            count += 1
    return count #Number of leap years

#Number of years taken from user
n_years = st.slider('For how many years do you want to forecast?:', 1, 10)
leap_years = count_leap_years(start_date, end_date) #checking for leap
period = n_years * 365 + leap_years

def DataLoader(ticker): #Helper function to load data from yahoo finance
    logging.debug("Started loading data")
    try:
        Stock_data = yf.download(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        Stock_data.reset_index(inplace=True)
        logging.debug("Started loading data")
    except Exception as e:
        raise CustomException(e,sys)
    return Stock_data
def app():
    if selected_stock:
        try: # loading the data
            Loading_progress = st.text('Please wait, data is being loaded')
            Stock_data = DataLoader(selected_stock)
            Loading_progress.text('Yay! Data loading complete')
        except Exception as e:
            raise CustomException(e,sys)
        
        #Displaying a small portion of the data
        st.subheader('Data for first few days after start date')
        st.write(Stock_data.head())

        st.subheader('Data for last few days before end date')
        st.write(Stock_data.tail())

        #Plotting the loaded data
        def Data_Plotter():
            Plot = go.Figure()
            Plot.add_trace(go.Scatter(x=Stock_data['Date'], y=Stock_data['Open'], name="stock_open"))
            Plot.add_trace(go.Scatter(x=Stock_data['Date'], y=Stock_data['Close'], name="stock_close"))
            Plot.layout.update(title_text='Raw time series data (Use slider to zoom in)', xaxis_rangeslider_visible=True)
            st.plotly_chart(Plot)

        Data_Plotter()

        #Getting the training set
        Training = Stock_data[['Date','Close']]
        Training = Training.rename(columns={"Date": "ds", "Close": "y"})

        Model = Prophet() #Model
        try:
            Model.fit(Training) #training
            logging.debug("Model succesfuly trained")
            Next = Model.make_future_dataframe(periods=period)
            Forecast = Model.predict(Next)
            logging.debug("Forecasting complete")
        except Exception as e:
            raise CustomException(e,sys)

        # Plotting the forecast
        st.subheader('Forecasted data')
        st.write(Forecast.tail())

        st.subheader(f'Forecast plot for {n_years} years (Use slider to zoom in)')
        fig1 = plot_plotly(Model, Forecast)
        st.plotly_chart(fig1)

        st.subheader("Forecast components")
        fig2 = Model.plot_components(Forecast)
        st.write(fig2)
    else:
        st.subheader('Enter a stock ticker.') 

if __name__ == "__main__":
    app()
