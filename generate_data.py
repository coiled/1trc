# This script was adapted from Jacob Tomlinson's 1BRC submission
# https://github.com/gunnarmorling/1brc/discussions/487

import os
import tempfile
import coiled
import fsspec
import numpy as np
import pandas as pd
from dask.distributed import progress

n = 1_000_000_000_000  # Total number of rows of data to generate
chunksize = 10_000_000  # Number of rows of data per file
std = 10.0  # Assume normally distributed temperatures with a standard deviation of 10
lookup_df = pd.read_csv("lookup.csv")  # Lookup table of stations and their mean temperatures
bucket = "s3://coiled-datasets-rp/1trc"


def generate_chunk(partition_idx, bucket, chunksize, std, lookup_df):
    """Generate some sample data based on the lookup table."""

    rng = np.random.default_rng(partition_idx)  # Determinisitic data generation
    df = pd.DataFrame(
        {
            # Choose a random station from the lookup table for each row in our output
            "station": rng.integers(0, len(lookup_df) - 1, int(chunksize)),
            # Generate a normal distibution around zero for each row in our output
            # Because the std is the same for every station we can adjust the mean for each row afterwards
            "measure": rng.normal(0, std, int(chunksize)),
        }
    )

    # Offset each measurement by the station's mean value
    df.measure += df.station.map(lookup_df.mean_temp)
    # Round the temprature to one decimal place
    df.measure = df.measure.round(decimals=1)
    # Convert the station index to the station name
    df.station = df.station.map(lookup_df.station)

    # Save this chunk to the output file
    filename = f"measurements-{partition_idx}.parquet"
    with tempfile.TemporaryDirectory() as tmpdir:
        local = os.path.join(tmpdir, filename)
        df.to_parquet(local, engine="pyarrow")
        fs = fsspec.filesystem("s3")
        fs.put(local, f"{bucket}/{filename}")


if __name__ == "__main__":

    with coiled.Cluster(
        n_workers=500,
        worker_cpu=1,
        arm=True,
        region="us-east-1",
        spot_policy="spot_with_fallback",
    ) as cluster:
        with cluster.get_client() as client:
            # Generate partitioned dataset
            results = client.map(
                generate_chunk,
                range(int(n / chunksize)),
                bucket=bucket,
                chunksize=chunksize,
                std=std,
                lookup_df=lookup_df,
            )
            progress(results)
