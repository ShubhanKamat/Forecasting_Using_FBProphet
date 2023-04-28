Stock Forecasting using FBProphet
This repository contains Python code that uses the fbprophet library to forecast the stock prices of a selected company using its historical data. 
The user can select the stock ticker, start date, and end date, and the program will load the stock data from Yahoo Finance, train a Prophet model 
on the data, and generate a forecast for a specified number of years.

Dependencies
The following dependencies are required to run this code:

streamlit
datetime
yfinance
fbprophet
plotly

These dependencies can be installed using pip by running the following command:
pip install -r requirements.txt

Input

Stock Ticker: The user must input the stock ticker symbol for the company they wish to forecast. For example, AAPL for Apple Inc.
Start Date: The user must select the start date of the historical data they wish to use for training the model.
End Date: The user must select the end date of the historical data they wish to use for training the model.
Forecast Years: The user must select the number of years they wish to forecast the stock price for.

Output

The program will output the following:
Raw Data: The program will display a small portion of the loaded data, both for the first few days after the start date and the last few days before the end date.
Data Plot: The program will display a plot of the loaded data, including both the open and close prices of the stock.
Forecasted Data: The program will display the forecasted data for the specified number of years.
Forecast Plot: The program will display a plot of the forecasted data for the specified number of years.
Forecast Components: The program will display a plot of the components of the forecast, including trend, weekly seasonality, and yearly seasonality.
