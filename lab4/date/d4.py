import datetime

today = datetime.datetime.today()
date = datetime.datetime(2025, 1, 2)
diff = today - date
print(diff.total_seconds())