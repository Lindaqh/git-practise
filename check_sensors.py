import yaml
import pandas as pd
import json

# Les config.yml
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Hent grensen for kalibrering og filnavnet fra konfigurasjonsfilen
max_days = config["max_days_since_calibration"]
output_file = config["output_file"]

# Les sensor- og kalibreringsdata
sensors = pd.read_excel("sensors.xlsx")
calibrations = pd.read_csv("calibrations.csv")

# Slå sammen sensor- og kalibreringsdata ved å bruke sensor_id
data = pd.merge(sensors, calibrations, on="sensor_id")

# Filtrer sensorer som har overskredet grensen for kalibrering
overdue = data[data["days_since_calibration"] > max_days]

# Velg nødvendig informasjon
result = overdue[
    ["sensor_id", "lab_room", "owner", "days_since_calibration"]
].to_dict(orient="records")

# Eksporter sensorer som har overskredet grensen som formatert JSON
with open(output_file, "w") as file:
    json.dump(result, file, indent=2)

print(f"Created {output_file}")