-- Prep
CREATE OR REPLACE EXTERNAL TABLE 'ny_taxi.taxi_rides_ny_yellow_external'
OPTIONS (
  format = 'parquet',
  uris = ['gs://dezoomcamp_hw_w3/trip_data/yellow_taxi/2024-*.parquet']
);

SELECT * FROM `ny_taxi.ny_taxi_yellow_external` LIMIT 10;

CREATE OR REPLACE TABLE ny_taxi.ny_taxi_yellow_non_partitioned as SELECT * FROM `ny_taxi.ny_taxi_yellow_external`;

-- Question 1
SELECT COUNT(*) from `ny_taxi.ny_taxi_yellow_non_partitioned`;

-- Question 2

SELECT DISTINCT PULocationID from `ny_taxi.ny_taxi_yellow_external`;

SELECT DISTINCT PULocationID from `ny_taxi.ny_taxi_yellow_non_partitioned`;

-- Question 3

SELECT PULocationID from `ny_taxi.ny_taxi_yellow_non_partitioned`;

SELECT PULocationID, DOLocationID from `ny_taxi.ny_taxi_yellow_non_partitioned`;

-- Question 4

SELECT COUNT(*) FROM `ny_taxi.ny_taxi_yellow_non_partitioned` WHERE fare_amount = 0;

-- Question 5
CREATE OR REPLACE TABLE ny_taxi.ny_taxi_yellow_dropoff_partition PARTITION BY DATE(tpep_dropoff_datetime) CLUSTER BY VendorID AS SELECT * FROM `ny_taxi.ny_taxi_yellow_non_partitioned`;

-- Question 6

SELECT DISTINCT VendorID from `ny_taxi.ny_taxi_yellow_non_partitioned` where tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <= '2024-03-15';

SELECT DISTINCT VendorID from `ny_taxi.ny_taxi_yellow_dropoff_partition` where tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <= '2024-03-15';




