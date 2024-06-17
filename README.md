# One Trillion Row Challenge

Inspired by Gunnar Morling's [one billion row challenge](https://github.com/gunnarmorling/1brc), we thought we'd take things one step further and start the one trillion row challenge (1TRC).

We describe the 1TRC, dataset, and running the challenge with Dask on Coiled in [this blog post](https://docs.coiled.io/blog/1trc.html).

## The Challenge

Your task is to use any tool(s) you’d like to calculate the min, mean, and max temperature per weather station, sorted alphabetically. The data is stored in Parquet on S3 in the `s3://coiled-datasets-rp/1trc` requester-pays bucket in AWS region `us-east-1`. Each file is 10 million rows and there are 100,000 files. For an extra challenge, you could also [generate the data yourself](#Data-Generation).

### How To Participate

Open an issue in this repository with your submission and enough details for someone else to be able to run your implementation. This includes things like:

- Hardware
- Runtime
- Reproducible code snippet

There is no prize and everyone is a winner. Really, the idea is to solicit ideas and generate discussion.

## Data Generation

You can generate the dataset yourself using the [data generation script](generate_data.py), adapted from [Jacob Tomlinson's 1BRC data generation script](https://github.com/gunnarmorling/1brc/discussions/487). We've also hosted the dataset in a requester pays S3 bucket `s3://coiled-datasets-rp/1trc` in `us-east-1`. 

It draws a random sample of weather stations and normally distributed temperatures drawn from the mean for each station based on the values in [lookup.csv](lookup.csv).

