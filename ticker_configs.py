import csv

INPUT_FILE = "redchip_disclosures_under_50M_with_dates.csv"

ticker_configs = []

with open(INPUT_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ticker = row["Ticker"].strip()
        date = row["Campaign_Date"].strip()
        ticker_configs.append((ticker, date))

# Print in exact Python tuple format
print("ticker_configs = [")
for t, d in ticker_configs:
    print(f"    (\"{t}\", \"{d}\"),")
print("]")

