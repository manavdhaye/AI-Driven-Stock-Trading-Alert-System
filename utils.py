
def format_telegram_message(stock, pnl, accuracy):
    if pnl > 0:
        result = f"PROFIT of ₹{pnl:.2f}"
        performance = "Good ✅"
    elif pnl < 0:
        result = f"LOSS of ₹{abs(pnl):.2f}"
        performance = "Poor ❌"
    else:
        result = "No Profit / No Loss"
        performance = "Neutral ⚖️"

    acc_percent = round(accuracy * 100)

    message = (
        f"📌 Stock: {stock}\n"
        f"💰 Result: {result}\n"
        f"🎯 ML Accuracy: {acc_percent}%\n"
        f"📊 Performance: {performance}\n"
        "----------------------"
    )

    return message
