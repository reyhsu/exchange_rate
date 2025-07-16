import requests
from bs4 import BeautifulSoup
import urllib3

# === 你的 Telegram 設定 ===
TELEGRAM_BOT_TOKEN = ''
CHAT_ID = ''

# 關閉 SSL 警告
urllib3.disable_warnings()

def fetch_currency_digital_rate(currency_name):
    url = "https://www.cathaybk.com.tw/cathaybk/personal/product/deposit/currency-billboard/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, verify=False)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, "html.parser")

        currency_blocks = soup.select(".cubre-o-table__item.currency")

        for block in currency_blocks:
            name = block.select_one(".cubre-m-currency__name")
            if name and currency_name in name.text:
                rows = block.select("tbody tr")
                for row in rows:
                    label = row.select_one("td div.cubre-m-rateTable__name")
                    if label and "數位通路優惠匯率" in label.text:
                        tds = row.select("td")[1:]
                        buy = tds[0].div.text.strip()
                        sell = tds[1].div.text.strip()
                        msg = (
                            f"[{currency_name} 數位通路優惠匯率]\n"
                            f"Bank buy: {buy}\n"
                            f"Bank sell: {sell}"
                        )
                        return msg
        return f"找不到 {currency_name} 的數位通路優惠匯率"
    except Exception as e:
        return f"查詢 {currency_name} 匯率錯誤: {e}"

def send_telegram_message(message):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        res = requests.post(api_url, json=payload)
        if res.status_code != 200:
            print("Telegram 發送失敗:", res.text)
    except Exception as e:
        print("Telegram 錯誤:", e)

if __name__ == "__main__":
    usd_msg = fetch_currency_digital_rate("美元USD")
    jpy_msg = fetch_currency_digital_rate("日圓JPY")
    full_message = usd_msg + "\n" + jpy_msg
#    print(full_message)
    send_telegram_message(full_message)

