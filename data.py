import os

# Load all file names and paths
def load_file_urls():
    files = os.listdir("./Dataset")
    collection = {}

    for i in files:
        csv_files = os.listdir(f"./Dataset/{i}")
        category = i.replace("_", " ").lower()
        catg_file = []
        for j in csv_files:
            if j.endswith(".csv"):
                file_path = f"./Dataset/{i}/{j}"
                catg_file.append({
                    "name": j.replace(".csv", "").lower(),
                    "path": file_path
                })
        collection[category] = catg_file
    return collection
    