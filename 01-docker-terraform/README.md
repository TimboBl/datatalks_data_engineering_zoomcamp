#### Local env setup

I have chosen to go with a local conda env using miniconda. I have installed miniconda via homebrew and created a new env using the command below:
```conda env create -f environment.yml```

The environment.yml file contains the following packages:
- sqlalchemy
- pandas

The file is stored in the root folder of the repo. 
The environemnt file will give a name to the conda env and also pull from the conda-forge channel. The python version is also set to 3.12.8 to ensure consistency across the project. 

Using the conda env also makes sure to not install packages into the global scope of the machine. This makes it easier to keep the machine clean and to avoid conflicts with other packages or projects using the same packages in diffrent versions.

To activate the env, the command below can be used:
```conda activate data-engineering```

#### Question 1 
Running docker in interactive mode
> docker run -it python:3.12.8 bash

Pip version in this image is 24.3.1

#### Question 2
##### Connecting to Postgres via PGAdmin
> The hostname and port to use for pgadmin should be postgres:5433

##### Connecting and uploading data
In order to connect to the local postgres instance I have created an ingest script. The script used sqlachemy and pandas to read the data from the csv file and upload it to the postgres database. Parameters such as the username, password, host, port, database name and table name can be provided as command linearguments when running the script.

The script is located in the src folder of the repo and can be run using the following command:
```bash
python ingest_data.py \
    --user=your_username \
    --password=your_password \
    --host=localhost \
    --port=5432 \
    --db=your_database \
    --table_name=your_table \
    --url=path_to_your_csv
```

The script will inform the user about the time it took to read and then upload the data to the desired table. 
The data was exluded from the repo to save space and also because it contains an archive file which is not ideal for historization in git. The data was obtained using these two commands: 
> wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz

> wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

The script will also work with a remote database. All that would have to be changed is the host parameter to point to the remote host.

#### Question 3

Trips up to 1 mile
 ```sql 
    select
	    COUNT(*)
    from
	    public.green_tripdata_2019_10
    where
        "trip_distance" <= 1.0
        and "lpep_dropoff_datetime" between  '2019-10-01'
        and '2019-11-01';
```
Trips between 1 and 3 miles
```sql
    select
        COUNT(*)
    from
        public.green_tripdata_2019_10 gt
    where
        gt.trip_distance > 1.0
        and gt.trip_distance <= 3.0
        and gt.lpep_dropoff_datetime between '2019-10-01'
        and '2019-11-01';
```

Trips between 3 and 7 miles
```sql
    select
        COUNT(*)
    from
        public.green_tripdata_2019_10 gt
    where
        gt.trip_distance > 3.0
        and gt.trip_distance <= 7.0
        and gt.lpep_dropoff_datetime between '2019-10-01'
        and '2019-11-01';
```

Trips between 7 and 10 miles
```sql
    select
        COUNT(*)
    from
        public.green_tripdata_2019_10 gt
    where
        gt.trip_distance > 7.0
        and gt.trip_distance <= 10.0
        and gt.lpep_dropoff_datetime between '2019-10-01'
        and '2019-11-01';
```

Trips over 10 miles
```sql
    select
        COUNT(*)
    from
        public.green_tripdata_2019_10 gt
    where
        gt.trip_distance > 10.0
        and gt.lpep_dropoff_datetime between '2019-10-01'
        and '2019-11-01';
```

#### Question 4
The longest trip was on October 31st 2019 with a distance of 515.89 miles.

```sql
    select
        MAX(trip_distance) as max_distance,
        DATE(gt.lpep_pickup_datetime) as trip_date
    from
        public.green_tripdata_2019_10 gt
    group by
        trip_date
    order by
        max_distance desc;
```

#### Question 5
This query will provide the zone with the most revenue on October 18th 2019 where the total amount is greater than 13,000. Filtered by pickup date.
```sql
    SELECT 
        tz."Zone",
        DATE(gt.lpep_pickup_datetime) as pickup_date,
        SUM(gt.total_amount) as amount_sum
    FROM 
        public.green_tripdata_2019_10 gt
    LEFT JOIN 
        public.taxi_zones tz ON gt."PULocationID" = tz."LocationID"
    WHERE 
        DATE(gt.lpep_pickup_datetime) = '2019-10-18'
    GROUP BY 
        DATE(gt.lpep_pickup_datetime), tz."Zone" 
    HAVING 
        SUM(gt.total_amount) > 13000;
```

#### Question 6
Largest tip in dropoff area where pickup zone was East Harlem North and date is in October 2019.
```sql
    select
        GTT.LPEP_PICKUP_DATETIME,
        PUZ."Zone",
        DOZ."Zone",
        GTT.TIP_AMOUNT
    from
        public.green_tripdata_2019_10 as GTT
    join public.taxi_zones as PUZ on
        GTT."PULocationID" = PUZ."LocationID"
    join public.taxi_zones as DOZ on
        GTT."DOLocationID" = DOZ."LocationID"
    where
        LPEP_PICKUP_DATETIME >= '2019-10-01'
        and LPEP_PICKUP_DATETIME < '2019-11-01'
        and PUZ."Zone" = 'East Harlem North'
    order by
	    GTT.TIP_AMOUNT desc;
```