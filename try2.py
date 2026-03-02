import csv

input_csv = "IPL Ball-by-Ball 2008-2025.csv"
output_csv = "IPL Ball-by-Ball 2008-2025-fixed.csv"

# Mapping of team IDs to names
TEAM_MAPPING = {
    "129": "Chennai Super Kings",
    "1": "Royal Challengers Bangalore",
    "252": "Delhi Capitals",
    "494": "Punjab Kings",
    "6": "Kolkata Knight Riders",
    "2": "Sunrisers Hyderabad",
    "134": "Rajasthan Royals",
    "614": "Lucknow Super Giants",
    "615": "Gujarat Titans",
    "3": "Mumbai Indians"
}

# Read all rows
with open(input_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    header = reader.fieldnames

# Update batting_team and bowling_team from line 243817 onward (0-indexed: 243816)
for i in range(243816, len(rows)):
    row = rows[i]
    row["batting_team"] = TEAM_MAPPING.get(str(row["batting_team"]), row["batting_team"])
    row["bowling_team"] = TEAM_MAPPING.get(str(row["bowling_team"]), row["bowling_team"])

# Write fixed CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Team IDs replaced with names from line 243817 onward. Saved as {output_csv}")
