import os
import json
import re
import subprocess

leaderboard = {}

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py") and file != "update_leaderboard.py":
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

                match = re.search(r"FINAL_ACCURACY:(\d*\.?\d+)", content)
                if match:
                    acc = float(match.group(1))

                    # Get contributor name
                    try:
                        contributor = subprocess.check_output(
                            ["git", "log", "-1", "--pretty=format:%an", path]
                        ).decode("utf-8")
                    except:
                        contributor = "Unknown"

                    # Keep best accuracy per contributor
                    if contributor not in leaderboard or leaderboard[contributor] < acc:
                        leaderboard[contributor] = acc

# Convert to sorted list
sorted_board = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

# Save JSON
with open("leaderboard.json", "w") as f:
    json.dump(sorted_board, f, indent=4)

# Update README
with open("README.md", "w") as f:
    f.write("# 🏆 Leaderboard\n\n")
    for i, (name, acc) in enumerate(sorted_board, 1):
        f.write(f"{i}. {name} - {acc}\n")
