# google_sheets_logger.py
import gspread
from config import SHEET_ID, SERVICE_ACCOUNT_FILE

def log_to_sheets(data, tab="Trade Log"):
    try:
        client = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        # client = gspread.service_account(filename="service_account.json")
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(tab)
        worksheet.append_row(data)
    except Exception as e:
        print("❌ Google Sheet Error:", e)
    #worksheet.append_row(data)