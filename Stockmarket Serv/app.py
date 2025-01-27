import os
import yfinance as yf
from flask import Flask, render_template, jsonify, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Home route - Displays the index page
@app.route('/')
def index():
    return render_template('index.html')

# Fetch stock data
@app.route('/stock_data', methods=['GET'])
def stock_data():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    try:
        # Fetch stock data for the last 5 days
        stock = yf.Ticker(symbol)
        data = stock.history(period="5d")  # Last 5 days
        
        # If no data is returned, handle the error
        if data.empty:
            return jsonify({"error": f"No stock data available for symbol {symbol}"}), 404

        # Convert the index (dates) to strings before converting to dict
        stock_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].to_dict(orient='index')
        stock_data = {str(date): value for date, value in stock_data.items()}  # Convert date to string
        return jsonify(stock_data)
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching stock data: {str(e)}"}), 500

# Calculate moving average
@app.route('/moving_average', methods=['GET'])
def moving_average():
    symbol = request.args.get('symbol')
    period = int(request.args.get('period', 5))  # Default to 5 if not specified
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="max")  # Get max available data
        
        # If no data is returned, handle the error
        if data.empty:
            return jsonify({"error": f"No stock data available for symbol {symbol}"}), 404

        close_prices = data['Close']

        # Calculate moving average
        moving_avg = close_prices.rolling(window=period).mean().tail(period)

        # Convert the moving average data to a dictionary, with date as string
        moving_avg_dict = moving_avg.to_dict()
        moving_avg_dict = {str(date): value for date, value in moving_avg_dict.items()}

        # If the moving average is not calculated properly, handle the error
        if not moving_avg_dict:
            return jsonify({"error": "Unable to calculate the moving average. Please try again later."}), 500
        
        return jsonify(moving_avg_dict)
    except Exception as e:
        return jsonify({"error": f"An error occurred while calculating moving average: {str(e)}"}), 500

# Generate stock plot
@app.route('/stock_plot', methods=['GET'])
def stock_plot():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="5d")  # Last 5 days

        # If no data is returned, handle the error
        if data.empty:
            return jsonify({"error": f"No stock data available for symbol {symbol}"}), 404

        # Plotting the stock data (Close price)
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['Close'], label='Close Price')
        plt.title(f'{symbol} Stock Price (Last 5 Days)')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.xticks(rotation=45)
        plt.grid(True)

        # Save the plot to a bytes buffer
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        img_str = base64.b64encode(img_buf.getvalue()).decode('utf-8')
        img_buf.close()

        # Return image as base64
        return jsonify({"plot_url": img_str})
    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching stock plot data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
