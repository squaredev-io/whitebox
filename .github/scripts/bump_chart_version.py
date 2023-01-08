import yaml
import sys

with open("helm_charts/christmas-package/Chart.yaml", "r") as f:
    chart = yaml.safe_load(f)

if len(sys.argv) < 2:
    raise Exception("Version number not provided")

# If it starts with a v, remove it
if sys.argv[1].startswith("v"):
    sys.argv[1] = sys.argv[1][1:]

chart["version"] = sys.argv[1]

with open("helm_charts/whitebox/Chart.yaml", "w") as f:
    yaml.dump(chart, f)

print(f"Updated chart version to {sys.argv[1]}")
