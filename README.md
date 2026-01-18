# FlightOps Data Engineering Pipeline

A production-style Data Engineering portfolio project that ingests real-time global flight telemetry data, builds curated Parquet datasets, calculates KPIs with historical tracking, and serves analytics through both SQL (Athena) and an interactive dashboard.

This project is designed to demonstrate end-to-end pipeline thinking: ingestion, transformation, data quality, cloud analytics, automation, and cost-aware operation.

## Demo

![FlightOps Demo](assets/demo/demo.gif)

## Project overview

The pipeline collects live aircraft state data, transforms it into a structured analytical format, and exposes insights through multiple consumption layers. It emphasizes reliability, clarity, and production-oriented design choices rather than experimental features.

Key goals:
- Demonstrate a realistic Data Engineering workflow
- Work with real, continuously changing data
- Separate raw ingestion from curated analytical data
- Enable both SQL analytics and dashboard-based exploration
- Apply basic production hardening (logging, cost control, permissions)

## Architecture

Local pipeline flow:
1. Fetch global flight states and store raw JSON snapshots
2. Transform raw data into a curated silver layer in Parquet format
3. Apply data quality checks and compute KPIs
4. Store KPI snapshots for historical trend analysis
5. Upload curated outputs to Amazon S3

Cloud analytics:
- Amazon S3 stores Parquet datasets and KPI reports
- Amazon Athena queries Parquet through an external table
- Athena views implement business logic such as region segmentation
- An Athena workgroup enforces per-query cost limits

## Project structure

FlightOps-DE-Pipeline/
  assets/
    demo/
      demo.gif
  athena/
    q01_region_kpi.sql
    q02_top_corridors.sql
    q03_speed_outliers.sql
  data/
    raw/
    silver/
    reports/
      history/
  logs/
    runs/
  scripts/
    run_all.sh
    upload_to_s3.sh
  src/
    flightops/
      fetch_states.py
      build_silver.py
      kpi_report.py
      region_kpi_report.py
  dashboard.py
  README.md

## Data pipeline

Raw layer:
- JSON snapshots of live aircraft state data
- Immutable, timestamped files

Silver layer:
- Parquet format optimized for analytics
- Normalized columns
- Explicit data quality flags

KPIs:
- Total aircraft count
- Aircraft with valid position
- On-ground vs in-air distribution
- Average and maximum velocity
- Data quality success rate
- Region-based aggregation

Each pipeline run generates a unique run identifier and a corresponding log file.

## Data quality

Basic data quality rules are applied during transformation, including:
- Valid latitude and longitude ranges
- Non-negative velocity values
- Controlled null handling for optional fields

Each record is marked with a boolean data quality flag, and aggregate data quality rates are tracked over time.

## Dashboard

The Streamlit dashboard provides:
- A global aircraft position map
- Current KPI overview
- KPI trend history based on stored snapshots
- Regional KPI breakdown
- Velocity distribution awareness

The dashboard reads from the latest curated outputs and reflects the most recent successful pipeline run.

## Athena analytics

The project includes ready-to-run Athena SQL queries:
- Region-level KPI aggregation
- Top origin-country and region corridors
- Velocity outlier inspection

Business logic for regional classification is implemented as an Athena view to keep transformations transparent and queryable.

## Running the pipeline

Run the full pipeline with:
./scripts/run_all.sh

This executes the full pipeline, writes logs, updates KPIs, and uploads results to S3.

## Cloud configuration notes

- Curated data and reports are stored in Amazon S3
- Athena queries Parquet data via an external table
- An Athena workgroup enforces per-query data scan limits
- Query metrics are published to CloudWatch
- Credentials are never committed to the repository

## Cost and security considerations

- Project-scoped IAM user with limited permissions
- No wildcard administrative access required
- Athena workgroup with strict per-query scan limits
- Separation between raw, curated, and analytical layers
- No sensitive data stored or transmitted

## Intended use

This project is intended as:
- A Data Engineering portfolio reference
- A technical discussion artifact for interviews
- A foundation for extending into cloud-native orchestration or BI tooling

It is not intended as a production aviation tracking system.

## License

MIT License
