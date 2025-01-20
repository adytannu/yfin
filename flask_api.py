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

    # Handle ETFs (No earnings date)
    earnings_dates = stock.earnings_dates if hasattr(stock, "earnings_dates") else None
    next_earnings_date = str(earnings_dates.index[0]) if earnings_dates is not None and not earnings_dates.empty else "N/A"

    # Calculate stock price change and percentage
    current_price = info.get("currentPrice", 0)
    previous_close = info.get("previousClose", 0)
    price_change = round(current_price - previous_close, 2) if current_price and previous_close else "N/A"
    price_change_pct = round((price_change / previous_close) * 100, 2) if previous_close else "N/A"

    # Convert market cap to billions
    market_cap_billion = round(info.get("marketCap", 0) / 1e9, 2) if info.get("marketCap") else "N/A"

    # Convert volume to thousands
    volume_k = round(info.get("volume", 0) / 1e3, 2) if info.get("volume") else "N/A"

    stock_data = {
        "ticker": ticker,
        "name": info.get("shortName", "N/A"),
        "next_earnings_date": next_earnings_date,  # Now safely handles ETFs
        "pe_ratio": info.get("trailingPE", "N/A"),
        "forward_pe": info.get("forwardPE", "N/A"),
        "peg_ratio": info.get("pegRatio", "N/A"),
        "price_to_book": info.get("priceToBook", "N/A"),
        "ev_to_ebitda": info.get("enterpriseToEbitda", "N/A"),
        "1Y_growth": info.get("earningsGrowth", "N/A"),
        "5Y_growth": info.get("revenueGrowth", "N/A"),
        "eps": info.get("trailingEps", "N/A"),
        "current_price": current_price,
        "previous_close": previous_close,
        "market_cap_billion": market_cap_billion,
        "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        "open": info.get("open", "N/A"),
        "high": info.get("dayHigh", "N/A"),
        "low": info.get("dayLow", "N/A"),
        "volume_k": volume_k,
        "avg_volume": info.get("averageVolume", "N/A"),
        "dividend_yield": info.get("dividendYield", "N/A"),
        "change": price_change,
        "change_pct": f"{price_change_pct}%" if price_change_pct != "N/A" else "N/A"
    }
    
    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
