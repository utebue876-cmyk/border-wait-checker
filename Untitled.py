time_text = "0:00"

parts = time_text.split(":")

hours = int(parts[0])
minutes = int(parts[1])

total_minutes = hours * 60 + minutes


lambda row: row["crossing"]
print(row)

print(total_minutes)