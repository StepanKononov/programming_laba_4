from datetime import datetime
t = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

datetime.strptime(t[0], '%m/%d/%y')