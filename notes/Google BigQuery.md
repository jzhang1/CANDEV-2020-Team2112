### ETL
- Python libais parse raw data into fields => CSV
- Upload processed CSV into Google Cloud Storage
- Setup a job to load data from csv into BigQuery
- Run this as a Google Cloud Function once per day

### Access Control
- Only Cloud Function has write access
- Authenticated users have read access

### Computed Fields
- Speed from time and position data
  - Use BigQuery Views
- Dynamic computing this is too expensive
  - Compute this at the data loading stage

### SQL Support

### Power BI integration

### Support for R and Python clients

### Cost Model
- Maintenance labor
- Prices