from job import Job

jobs = Job.read_from_yaml()

for job in jobs:
    job.get_job_last_build_info()