from utils.excel_reader import read_excel_data

data = read_excel_data("PositiveFlights")
print("Total rows read:", len(data))
print("Data:")
for row in data:
    print(row)