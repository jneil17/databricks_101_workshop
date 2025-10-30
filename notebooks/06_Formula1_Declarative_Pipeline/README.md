# Sprint Qualifying Results Pipeline

## Overview

This pipeline ingests and processes Formula 1 sprint qualifying results data using Databricks Declarative Pipelines with streaming CDC (Change Data Capture).

## Pipeline Architecture

### 1. Bronze Layer (Raw Ingestion)
- **Table**: `bronze_sprint_qualifying_results_cdc`
- Incrementally ingests CSV files from cloud object storage
- Uses Auto Loader for scalable file ingestion
- Source: `/Volumes/main/default/streaming_formula1/`

### 2. Data Quality (Cleansing)
- **View**: `bronze_sprint_qualifying_results_cdc_clean`
- Applies data quality expectations:
  - Drops rows with rescued data (malformed records)
  - Validates Track is not null
  - Validates Driver is not null

### 3. CDC Target
- **Table**: `bronze_sprint_qualifying_results`
- Processes changes using Track and Driver as composite keys
- Sequences updates by Q1 time
- Maintains current state of sprint qualifying results

## Data Quality Rules

| Rule | Action | Description |
|------|--------|-------------|
| no_rescued_data | Drop | Removes malformed CSV records |
| valid_track | Drop | Ensures Track field exists |
| valid_driver | Drop | Ensures Driver field exists |

## Usage

Run this pipeline in a Databricks Declarative Pipeline workflow to continuously process sprint qualifying data as new files arrive in the source location.