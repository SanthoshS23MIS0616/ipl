import os
import requests
import zipfile
import io
import json
from datetime import datetime
import csv

# ---- Configuration ----

IPL_JSON_ZIP_URL = "https://cricsheet.org/downloads/ipl_json.zip"
TARGET_YEARS = set(range(2008, 2026))  # 2008 to 2025
OUTPUT_CSV = "ipl_2008_2025_matches.csv"

COLUMNS = [
    "id","city","date","player_of_match","venue","neutral_venue",
    "team1","team2","toss_winner","toss_decision","winner",
    "result","result_margin","eliminator","method","umpire1","umpire2"
]

# ---- Functions ----

def download_and_extract_zip(url, extract_to):
    resp = requests.get(url)
    resp.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    z.extractall(extract_to)

def parse_match_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    info = data.get("info", {})
    dates = info.get("dates", [])
    if not dates:
        return None
    try:
        match_date = datetime.fromisoformat(dates[0])
    except Exception:
        match_date = datetime.strptime(dates[0], "%Y-%m-%d")
    if match_date.year not in TARGET_YEARS:
        return None

    row = {}
    row["id"] = os.path.basename(filepath).replace(".json", "")

    city = info.get("city", "")
    if city == "Bengaluru":
        city = "Bangalore"
    row["city"] = city

    row["date"] = match_date.strftime("%d-%m-%Y")

    pom = info.get("player_of_match")
    if isinstance(pom, list):
        row["player_of_match"] = pom[0] if pom else ""
    else:
        row["player_of_match"] = pom or ""

    # Always "venue"
    row["venue"] = "venue"
    row["neutral_venue"] = 1 if info.get("neutral_venue", False) else 0

    teams = info.get("teams", [])
    row["team1"] = teams[0] if len(teams) > 0 else ""
    row["team2"] = teams[1] if len(teams) > 1 else ""

    toss = info.get("toss", {})
    row["toss_winner"] = toss.get("winner", "")
    row["toss_decision"] = toss.get("decision", "")

    outcome = info.get("outcome", {})
    row["winner"] = outcome.get("winner", "")

    by = outcome.get("by", {})
    if "runs" in by:
        row["result"] = "runs"
        row["result_margin"] = by["runs"]
    elif "wickets" in by:
        row["result"] = "wickets"
        row["result_margin"] = by["wickets"]
    else:
        row["result"] = outcome.get("result", "")
        row["result_margin"] = ""

    row["eliminator"] = "Y" if outcome.get("eliminator") else "N"
    row["method"] = outcome.get("method", "NA")

    umps = info.get("officials", {}).get("umpires", [])
    row["umpire1"] = umps[0] if len(umps) > 0 else ""
    row["umpire2"] = umps[1] if len(umps) > 1 else ""

    return row

def main():
    workdir = "ipl_json"
    if not os.path.exists(workdir):
        os.makedirs(workdir)

    print("📥 Downloading IPL data...")
    download_and_extract_zip(IPL_JSON_ZIP_URL, workdir)
    print("✅ Download & extraction done.")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
        writer.writeheader()
        for fname in os.listdir(workdir):
            if fname.endswith(".json"):
                path = os.path.join(workdir, fname)
                row = parse_match_file(path)
                if row:
                    writer.writerow(row)

    print(f"🎉 Done! Created {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
