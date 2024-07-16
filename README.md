# conda-forge-cdf

## Overview

This repository contains a script that analyzes the download counts of packages from the conda-forge feedstocks repository. It retrieves download data, processes it to create a cumulative distribution function (CDF) plot, and visualizes it using Altair. The plot shows the number of packages with download counts less than or equal to a given number, using a logarithmic scale for the x-axis.

## Purpose

The primary purpose of this analysis is to visualize and understand the distribution of download counts across different packages in the conda-forge feedstocks repository. This can help in identifying the popularity distribution of packages and in making data-driven decisions.

## Getting Started

### Requirements

- Python 3.x
- `requests` library
- `pandas` library
- `altair` library
- `git` (for cloning the repository)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/fxwiegand/conda-forge-cdf.git
   cd conda-forge-cdf
   ```

2. **Install required libraries:**

   You can install the necessary Python libraries using pip:

   ```bash
   pip install requests pandas altair
   ```

### Running the Script

1. **Run the analysis script:**

   Execute the script to fetch download counts, process the data, and generate the plot:

   ```bash
   python main.py
   ```

   The script will create a file named `downloads_cdf.html` in the current directory. This file contains the interactive CDF plot.

### Interpreting the Plot

- **X-axis (Downloads):** This axis represents the number of downloads for packages, displayed on a logarithmic scale to handle a wide range of values.
- **Y-axis (Number of Packages):** This axis shows the cumulative number of packages with download counts less than or equal to the corresponding value on the x-axis.
- **Red Dot:** Indicates the position of the `datavzrd` package within the distribution.

## Data Storage

The script saves intermediate results to `download_counts_checkpoint.json` to allow for resuming the analysis if interrupted. This file contains the download counts for each package processed so far.

## Notes

- Ensure you have a stable internet connection, as the script fetches data from the web.
- The script may take some time to run, depending on the number of packages being processed.