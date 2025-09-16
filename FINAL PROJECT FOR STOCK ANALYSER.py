# ultimate_stock_analyzer.py
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


def show_categories():
    print("\n" + "=" * 60)
    print("📋 STOCK CATEGORIES EXAMPLES")
    print("=" * 60)

    categories = {
        "🇮🇳 INDIAN STOCKS": ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "SBIN.NS"],
        "🇺🇸 US STOCKS": ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NFLX"],
        "📊 INDIAN INDICES": ["^NSEI (Nifty 50)", "^BSESN (Sensex)", "^NSEBANK (Bank Nifty)"],
        "🌍 GLOBAL INDICES": ["^GSPC (S&P 500)", "^DJI (Dow Jones)", "^IXIC (NASDAQ)"],
        "💰 ETFs": ["GOLDBEES.NS (Gold ETF)", "SPY (S&P 500 ETF)", "QQQ (NASDAQ ETF)"],
        "⛏️ COMMODITIES": ["GC=F (Gold)", "SI=F (Silver)", "CL=F (Crude Oil)"],
        "₿ CRYPTO": ["BTC-USD (Bitcoin)", "ETH-USD (Ethereum)", "DOGE-USD (Dogecoin)"]
    }

    for category, examples in categories.items():
        print(f"\n{category}:")
        print(f"   {', '.join(examples)}")


def ultimate_stock_analyzer():
    while True:
        print("\n" + "=" * 60)
        print("🚀 ULTIMATE STOCK ANALYZER")
        print("=" * 60)

        # Show categories first
        show_categories()

        print("\n" + "-" * 60)
        # Stock symbol input
        symbol = input("\nEnter stock symbol (see examples above): ").strip().upper()
        if not symbol:
            symbol = "RELIANCE.NS"

        # Time period input
        print("\n📅 TIME PERIOD OPTIONS:")
        print("1W, 1M, 3M, 6M, 1Y, 2Y, 3Y, 4Y, 5Y, MAX")

        period = input("Enter time period: ").upper().strip() or "1Y"

        period_map = {
            '1W': '1wk', '1M': '1mo', '3M': '3mo', '6M': '6mo',
            '1Y': '1y', '2Y': '2y', '3Y': '3y', '4Y': '4y', '5Y': '5y', 'MAX': 'max'
        }

        period_param = period_map.get(period, '1y')
        period_label = period

        print(f"\n📥 Downloading {symbol} data for {period_label}...")

        try:
            data = yf.download(symbol, period=period_param, progress=True)

            if data.empty:
                print("❌ No data found! Check symbol format.")
                continue

            print(f"✅ Success! {len(data)} trading days downloaded")

        except Exception as e:
            print(f"❌ Error: {e}")
            continue

        # Fix Yahoo Finance columns
        if hasattr(data.columns, 'levels'):
            if len(data.columns) == 6:
                data.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
            else:
                data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        # Analysis
        print(f"\n📊 {symbol} COMPLETE ANALYSIS ({period_label})")
        print("=" * 60)
        print(f"Period: {data.index[0].date()} to {data.index[-1].date()}")
        print(f"Trading Days: {len(data)}")

        if 'Close' in data.columns:
            start_p = data['Close'].iloc[0]
            end_p = data['Close'].iloc[-1]
            change = ((end_p - start_p) / start_p) * 100
            volatility = data['Close'].pct_change().std() * 100

            print(f"Start Price: ₹{start_p:.2f}")
            print(f"End Price: ₹{end_p:.2f}")
            print(f"Total Return: {change:+.2f}%")
            print(f"Volatility: {volatility:.2f}%")
            print(f"Highest: ₹{data['High'].max():.2f}")
            print(f"Lowest: ₹{data['Low'].min():.2f}")

        print("\n🎨 Generating 8 Professional Charts (2 per page)...")

        # ---- Charts in 4 pages (2 charts per page) ----
        for page in range(4):
            plt.figure(figsize=(12, 6))
            chart_id = page * 2 + 1

            # -------- 1. PRICE + MOVING AVG --------
            if chart_id == 1:
                plt.subplot(2, 1, 1)
                plt.plot(data.index, data['Close'], color='blue', linewidth=2)
                plt.title('1. PRICE CHART 📈', fontweight='bold')
                plt.xlabel('Date')
                plt.ylabel('Price')
                plt.grid(True, alpha=0.3)
                plt.xticks(rotation=45)

                plt.subplot(2, 1, 2)
                plt.plot(data.index, data['Close'], label='Price', color='blue', linewidth=1, alpha=0.7)
                if len(data) > 20:
                    ma_20 = data['Close'].rolling(20).mean()
                    plt.plot(data.index, ma_20, label='20D MA', color='red', linewidth=2)
                if len(data) > 50:
                    ma_50 = data['Close'].rolling(50).mean()
                    plt.plot(data.index, ma_50, label='50D MA', color='green', linewidth=2)
                plt.title('2. MOVING AVERAGES 📊', fontweight='bold')
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.xticks(rotation=45)

            # -------- 2. VOLUME + RETURNS --------
            elif chart_id == 3:
                plt.subplot(2, 1, 1)
                plt.bar(data.index, data['Volume'], color='purple', alpha=0.7)
                plt.title('3. TRADING VOLUME 🏋️', fontweight='bold')
                plt.xlabel('Date')
                plt.ylabel('Volume')
                plt.grid(True, alpha=0.3)
                plt.xticks(rotation=45)

                plt.subplot(2, 1, 2)
                daily_returns = data['Close'].pct_change().dropna() * 100
                plt.hist(daily_returns, bins=30, color='orange', alpha=0.7, edgecolor='black')
                plt.title('4. DAILY RETURNS 📉', fontweight='bold')
                plt.xlabel('Daily Return %')
                plt.ylabel('Frequency')
                plt.grid(True, alpha=0.3)

            # -------- 3. VOLATILITY + SUPPORT/RES --------
            elif chart_id == 5:
                plt.subplot(2, 1, 1)
                if len(data) > 20:
                    volatility = data['Close'].pct_change().rolling(20).std() * 100
                    plt.plot(data.index, volatility, color='red', linewidth=2)
                    plt.title('5. 20-DAY VOLATILITY 🌊', fontweight='bold')
                    plt.xlabel('Date')
                    plt.ylabel('Volatility %')
                    plt.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)

                plt.subplot(2, 1, 2)
                plt.plot(data.index, data['Close'], color='blue', linewidth=1)
                recent_data = data.tail(30)
                support = recent_data['Low'].min()
                resistance = recent_data['High'].max()
                current_price = data['Close'].iloc[-1]
                plt.axhline(y=support, color='green', linestyle='--', alpha=0.8, label=f'Support: ₹{support:.2f}')
                plt.axhline(y=resistance, color='red', linestyle='--', alpha=0.8,
                            label=f'Resistance: ₹{resistance:.2f}')
                plt.axhline(y=current_price, color='orange', linestyle='-', alpha=0.6,
                            label=f'Current: ₹{current_price:.2f}')
                plt.title('6. SUPPORT & RESISTANCE 🎯', fontweight='bold')
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.xticks(rotation=45)

            # -------- 4. OHLC + HEATMAP --------
            elif chart_id == 7:
                plt.subplot(2, 1, 1)
                recent_data = data.tail(20)
                for i in range(len(recent_data)):
                    date = recent_data.index[i]
                    open_p = recent_data['Open'].iloc[i]
                    high_p = recent_data['High'].iloc[i]
                    low_p = recent_data['Low'].iloc[i]
                    close_p = recent_data['Close'].iloc[i]
                    plt.plot([date, date], [low_p, high_p], color='black', linewidth=1)
                    if close_p >= open_p:
                        plt.plot([date, date], [open_p, close_p], color='green', linewidth=4)
                    else:
                        plt.plot([date, date], [open_p, close_p], color='red', linewidth=4)
                plt.title('7. OHLC BARS 📊', fontweight='bold')
                plt.xlabel('Date')
                plt.ylabel('Price')
                plt.grid(True, alpha=0.3)
                plt.xticks(rotation=45)

                plt.subplot(2, 1, 2)
                numeric_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
                plt.imshow(numeric_data, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
                plt.colorbar(label='Correlation')
                plt.title('8. CORRELATION HEATMAP 🔥', fontweight='bold')
                plt.xticks(range(len(numeric_data.columns)), numeric_data.columns, rotation=45)
                plt.yticks(range(len(numeric_data.columns)), numeric_data.columns)
                for i in range(len(numeric_data.columns)):
                    for j in range(len(numeric_data.columns)):
                        plt.text(j, i, f'{numeric_data.iloc[i, j]:.2f}',
                                 ha='center', va='center',
                                 color='white' if abs(numeric_data.iloc[i, j]) > 0.5 else 'black')

            plt.tight_layout()
            plt.show()

        print(f"\n✅ 8 PROFESSIONAL CHARTS GENERATED FOR {symbol}!")

        # Continue or Exit
        print("\n" + "-" * 60)
        continue_analysis = input("\nAnalyze another stock? (y/n): ").lower().strip()
        if continue_analysis != 'y':
            print("\n🎉 Thanks for using Ultimate Stock Analyzer!")
            print("📈 Happy Investing! 🚀")
            break


# Run the ultimate analyzer
if __name__ == "__main__":
    ultimate_stock_analyzer()

