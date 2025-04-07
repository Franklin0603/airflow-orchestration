#!/bin/bash
set -e

# Simple script to run dbt commands

# Default values
DBT_COMMAND=${1:-"run"}
DBT_TARGET=${2:-"dev"}
DBT_MODELS=${3:-"all"}

# Assuming dbt project is mounted/available at this location
# DBT_PROJECT_DIR=${DBT_PROJECT_DIR:-"/usr/local/airflow/dbt"}
# PROFILES_DIR=${PROFILES_DIR:-"/usr/local/airflow/include/dbt/profiles"}

# Get the dbt project directory from environment variable
DBT_PROJECT_DIR=${DBT_PROJECT_DIR:-"/opt/dbt"}
PROFILES_DIR=${PROFILES_DIR:-"${DBT_PROJECT_DIR}/profiles"}

echo "Running dbt ${DBT_COMMAND} with target ${DBT_TARGET} and models ${DBT_MODELS}"

# Change to dbt project directory
cd ${DBT_PROJECT_DIR}

# Execute dbt
dbt ${DBT_COMMAND} \
  --target ${DBT_TARGET} \
  --profiles-dir ${PROFILES_DIR} \
  ${DBT_MODELS:+--models ${DBT_MODELS}}

echo "dbt command completed successfully"