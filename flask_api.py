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

    # Ensure numeric values are converted properly
    def safe_float(value):
        """Converts value to float if possible, otherwise returns None."""
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    current_price = safe_float(info.get("currentPrice"))
    previous_close = safe_float(info.get("previousClose"))

    # Calculate stock price change and percentage safely
    if current_price is not None and previous_close is not None:
        price_change = round(current_price - previous_close, 2)
        price_change_pct = round((price_change / previous_close) * 100, 2)
    else:
        price_change = "N/A"
        price_change_pct = "N/A"

    # Convert market cap to billions
    market_cap_billion = safe_float(info.get("marketCap"))
    if market_cap_billion is not None:
        market_cap_billion = round(market_cap_billion / 1e9, 2)

    # Convert volume to thousands
    volume_k = safe_float(info.get("volume"))
    if volume_k is not None:
        volume_k = round(volume_k / 1e3, 2)

    stock_data = {
        "ticker": ticker,
        "name": info.get("shortName", "N/A"),
        "next_earnings_date": next_earnings_date,  # Now safely handles ETFs
        "pe_ratio": safe_float(info.get("trailingPE")),
        "forward_pe": safe_float(info.get("forwardPE")),
        "peg_ratio": safe_float(info.get("pegRatio")),
        "price_to_book": safe_float(info.get("priceToBook")),
        "ev_to_ebitda": safe_float(info.get("enterpriseToEbitda")),
        "1Y_growth": safe_float(info.get("earningsGrowth")),
        "5Y_growth": safe_float(info.get("revenueGrowth")),
        "eps": safe_float(info.get("trailingEps")),
        "current_price": current_price,
        "previous_close": previous_close,
        "market_cap_billion": market_cap_billion,
        "52_week_high": safe_float(info.get("fiftyTwoWeekHigh")),
        "52_week_low": safe_float(info.get("fiftyTwoWeekLow")),
        "open": safe_float(info.get("open")),
        "high": safe_float(info.get("dayHigh")),
        "low": safe_float(info.get("dayLow")),
        "volume_k": volume_k,
        "avg_volume": safe_float(info.get("averageVolume")),
        "dividend_yield": safe_float(info.get("dividendYield")),
        "change": price_change,
        "change_pct": f"{price_change_pct}%" if price_change_pct != "N/A" else "N/A"
    }
    
    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
