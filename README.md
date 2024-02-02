# One Trillion Row Challenge

Inspired by Gunnar Morling's [one billion row challenge](https://github.com/gunnarmorling/1brc), we thought we'd take things one step further and start the one trillion row challenge (1TRC).

## Data Generation

You can generate the dataset yourself using the [data generation script](generate_data.py), adapted from [Jacob Tomlinson's data generation script](https://github.com/gunnarmorling/1brc/discussions/487). We've also hosted the dataset in a requester pays S3 bucket `s3://coiled-datasets-rp/1trc` in `us-east-1`. 

It draws a random sample of weather stations and normally distributed temperatures drawn from the mean for each station based on the values in [lookup.csv](lookup.csv).

## The Challenge

The main task, like the 1BRC, is to calculate the min, mean, and max values per weather station, sorted alphabetically.


