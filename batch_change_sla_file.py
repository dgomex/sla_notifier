import yaml
from datetime import datetime, timedelta

# Path to your YAML file
yaml_file_path = "sla_config_prod.yaml"

# Read and process the YAML file
with open(yaml_file_path, 'r') as file:
    data = yaml.safe_load(file)

# Process and print the name and updated SLA time for each job
for record in data:
    job = record.get("Job", {})
    name = job.get("name", "Unknown")
    sla_time = job.get("sla_time", "00:00")

    # Add 15 minutes to SLA time
    try:
        sla_datetime = datetime.strptime(sla_time, "%H:%M")
        updated_sla_time = (sla_datetime + timedelta(minutes=15)).strftime("%H:%M")
    except ValueError:
        updated_sla_time = "Invalid Time Format"

    print(f"- Job: ")
    print(f"    name: \"{name}\"")
    print(f"    sla_time: \"{updated_sla_time}\"")