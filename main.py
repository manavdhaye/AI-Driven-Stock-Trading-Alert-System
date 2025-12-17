# main.py
from config import STOCKS
from feature_enginerring import generate_signals,compute_rsi,backtest
from fetch_data import fetch_stock_data
from ml_model import train_model
from google_sheet import log_to_sheets
from telegram_alert import send_alert
from utils import format_telegram_message

final_message = "📊 My Algo Trading Report\n\n"

for stock in STOCKS:
    print(f"Processing {stock}...")
    df = fetch_stock_data(stock)
    df = generate_signals(df)
    
    strategy_pnl, trades, trade_pnls, win_ratio = backtest(df)
    trade_index = 0

    print(f"{stock} - PnL: {strategy_pnl}, Win Ratio: {win_ratio}")
    trade_index = 0
    
    for trade in trades:
        action, date, price = trade
        trade_pnl = ""
        if action == "SELL":
            trade_pnl = trade_pnls[trade_index]
            trade_index += 1

        log_to_sheets([stock,action,str(date.date()),round(price, 2),trade_pnl,round(strategy_pnl, 2),round(win_ratio, 2)])
    
    # ML prediction
    model, acc = train_model(df)
    print(f"Prediction Accuracy for {stock}: {acc}")
    
    # Telegram alert
    final_message += format_telegram_message(stock, strategy_pnl, acc) + "\n"
send_alert(final_message)
    # send_alert(f"{stock} - Final PnL: {pnl}, Accuracy: {acc}")

   