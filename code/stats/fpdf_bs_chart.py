import joblib

edus = []
businesses = []
sums = []

business_totals = {}
file = joblib.load("C:/Users/shkunn/Downloads/bs_single.joblib")

for edu, businesses in file.items():
    for business, value in businesses.items():
        if business in business_totals.keys():
            business_totals[business] += value
        else:
            business_totals[business] = value

with open ("C:/Users/shkunn/Documents/results/fpdf_bs_table.txt", "w") as f:
    f.write("business,Bottom 38.19%,38.19% to 72.32%,72.32% to 89.86%,89.86% to 99.13%,Top 0.87%,total\n")
    for b,n in business_totals.items():
        f.write(f"{b},{file[0][b]},{file[1][b]},{file[2][b]},{file[3][b]},{file[4][b]},{n}\n")