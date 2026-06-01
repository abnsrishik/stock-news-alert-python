# Stock News Alert — WhatsApp Notifier

A Python automation that monitors stock price movements and sends top news articles via WhatsApp when significant changes are detected.

If a stock moves more than 5% in a day, you get the top 3 related news headlines — with stock movement indicator — straight to WhatsApp.

## How It Works

1. Fetches yesterday's and the day before yesterday's closing prices from Alpha Vantage
2. Calculates the percentage change between the two days
3. If change exceeds 5% — fetches top 3 news articles about the company from NewsAPI
4. Sends each article as a separate WhatsApp message via Twilio, formatted with stock movement and brief description

## Example WhatsApp Message

```
TSLA 🔺7%
Headline: Tesla hits record deliveries in Q2.
Brief: Tesla reported its highest quarterly deliveries...
```

## Features

- **Dual API integration** — Alpha Vantage (stock) + NewsAPI (news) chained together
- **Conditional triggering** — only alerts on significant moves (>5%), no noise
- **Three messages** — one per top news article, sorted by popularity
- **Movement indicator** — 🔺 for price up, 🔻 for price down
- **Fully secure** — all credentials in environment variables

## Setup

### 1. Get API Keys

| Service | Where to get it |
|---|---|
| Alpha Vantage | [alphavantage.co](https://www.alphavantage.co/support/#api-key) — free |
| NewsAPI | [newsapi.org](https://newsapi.org/register) — free tier |
| Twilio | [twilio.com](https://www.twilio.com) — free trial |

### 2. Set Environment Variables

```bash
export STOCK_API="your_alphavantage_key"
export NEWS_API="your_newsapi_key"
export ACCOUNT_SID="your_twilio_sid"
export AUTH_TOKEN="your_twilio_auth_token"
export TO_WHATSAPP_NUMBER="whatsapp:+91XXXXXXXXXX"
```

### 3. Change the Stock (Optional)

Edit `main.py`:
```python
STOCK_NAME = "TSLA"      # ticker symbol
COMPANY_NAME = "Tesla Inc"  # used for news search
```

### 4. Run

```bash
pip install requests twilio
python main.py
```

## Automate with GitHub Actions

Run every weekday morning before market opens.

Save as `.github/workflows/stock_alert.yml`:

```yaml
name: Stock News Alert
on:
  schedule:
    - cron: '30 23 * * 1-5'  # 11:30 PM UTC = 5:00 AM IST, Mon–Fri only
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - run: pip install requests twilio
      - run: python main.py
        env:
          STOCK_API: ${{ secrets.STOCK_API }}
          NEWS_API: ${{ secrets.NEWS_API }}
          ACCOUNT_SID: ${{ secrets.ACCOUNT_SID }}
          AUTH_TOKEN: ${{ secrets.AUTH_TOKEN }}
          TO_WHATSAPP_NUMBER: ${{ secrets.TO_WHATSAPP_NUMBER }}
```

## Requirements

- Python 3.x
- requests (`pip install requests`)
- twilio (`pip install twilio`)

## What I Learned

- Chaining two REST APIs — stock data + news data in one script
- Percentage change calculation and conditional logic
- Twilio WhatsApp API for multi-message sending
- List comprehension for formatting multiple messages
- Environment variables for all credentials
- GitHub Actions cron for weekday-only scheduling (`1-5`)
