import pandas as pd

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def generate_signals(df):
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA50'] = df['Close'].rolling(50).mean()
    df['RSI'] = compute_rsi(df['Close'])
    
    df['Signal'] = 0
    df.loc[(df['RSI'] < 30) & (df['MA20'] > df['MA50']), 'Signal'] = 1  # Buy
    df.loc[(df['RSI'] > 70) & (df['MA20'] < df['MA50']), 'Signal'] = -1 # Sell
    
    return df

def backtest(df, initial_capital=100000):
    capital = initial_capital
    position = 0
    buy_price = 0
    trades = []
    trade_pnls = []

    for i in range(len(df)):
        if df['Signal'].iloc[i] == 1 and position == 0:
            buy_price = df['Close'].iloc[i]
            position = capital / buy_price
            capital = 0
            trades.append(("BUY", df.index[i], buy_price))

        elif df['Signal'].iloc[i] == -1 and position > 0:
            sell_price = df['Close'].iloc[i]
            capital = position * sell_price
            trade_pnl = capital - initial_capital
            trade_pnls.append(trade_pnl)
            position = 0
            trades.append(("SELL", df.index[i], sell_price))

    final_value = capital + position * df['Close'].iloc[-1]
    strategy_pnl = final_value - initial_capital
    win_ratio = sum(1 for p in trade_pnls if p > 0) / max(1, len(trade_pnls))

    return strategy_pnl, trades, trade_pnls, win_ratio

