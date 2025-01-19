from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/stock', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker', default='', type=str).upper()
    if not ticker:
        return jsonify({"error": "Please provide a stock ticker"}), 400
    
    stock = yf.Ticker(ticker)
    info = stock.info

    stock_data = {
        "ticker": ticker,
        "name": info.get("shortName", "N/A"),
        "current_price": info.get("currentPrice", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        "volume": info.get("volume", "N/A"),
        "avg_volume": info.get("averageVolume", "N/A"),
        "dividend_yield": info.get("dividendYield", "N/A"),
    }
    
    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
