import json, csv, logging

def save_results(data, filename):
    if filename.endswith(".json"):
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    elif filename.endswith(".csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
    else:
        logging.error("Unsupported file format. Use .json or .csv")
