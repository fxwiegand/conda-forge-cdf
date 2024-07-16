import os
import time
import requests
import re
import subprocess
import json
import pandas as pd
import altair as alt

repo_url = 'https://github.com/conda-forge/feedstocks.git'
repo_dir = 'feedstocks'

if not os.path.exists(repo_dir):
    subprocess.run(['git', 'clone', repo_url])

feedstocks_dir = os.path.join(repo_dir, 'feedstocks')
package_names = [name for name in os.listdir(feedstocks_dir) if os.path.isdir(os.path.join(feedstocks_dir, name))]

checkpoint_file = 'download_counts_checkpoint.json'


def get_download_count(package_name):
    url = f'https://anaconda.org/conda-forge/{package_name}/badges/downloads.svg'
    response = requests.get(url)
    if response.status_code == 200:
        match = re.search(r'<title>downloads:\s*(\d+(?:\.\d+)?[kM]?)\s*total</title>', response.text)
        if match:
            count_str = match.group(1)
            if 'k' in count_str:
                count = int(float(count_str.replace('k', '')) * 1000)
            elif 'M' in count_str:
                count = int(float(count_str.replace('M', '')) * 1000000)
            else:
                count = int(count_str)
            return count
    return 0


# Load intermediate results if available
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        download_counts = json.load(f)
else:
    download_counts = []

start_index = len(download_counts)

start_time = time.time()

for i, package in enumerate(package_names[start_index:], start=start_index):
    count = get_download_count(package)
    download_counts.append((package, count))

    if (i + 1) % 100 == 0:
        elapsed_time = time.time() - start_time
        processed_packages = i + 1
        total_packages = len(package_names)

        avg_time_per_package = elapsed_time / processed_packages

        remaining_packages = total_packages - processed_packages
        estimated_remaining_time = remaining_packages * avg_time_per_package

        minutes, seconds = divmod(estimated_remaining_time, 60)

        print(f"{processed_packages} packages of {total_packages} processed in {elapsed_time:.2f} seconds")
        print(f"Estimated time to finish: {int(minutes)} minutes and {int(seconds)} seconds")

        with open(checkpoint_file, 'w') as f:
            json.dump(download_counts, f)

with open(checkpoint_file, 'w') as f:
    json.dump(download_counts, f)

df = pd.DataFrame(download_counts, columns=['package', 'downloads'])

# Filter out packages with zero downloads for log scale
df = df[df['downloads'] > 0]

if 'datavzrd' in df['package'].values:
    datavzrd_downloads = df[df['package'] == 'datavzrd']['downloads'].values[0]

    df = df.sort_values(by='downloads')
    df['cumulative_count'] = range(1, len(df) + 1)

    # Define the selection
    selection = alt.selection_single(on='mouseover', fields=['package'], nearest=True)

    # Base chart
    base = alt.Chart(df).mark_line().encode(
        x=alt.X('downloads:Q', scale=alt.Scale(type='log'), title='Downloads (log scale)'),
        y=alt.Y('cumulative_count:Q', title='# of packages with less or equal x downloads'),
        tooltip=['package', 'downloads']
    ).properties(
        width=600,
        height=400,
        title='Datavzrd Downloads'
    )

    points = base.mark_point().encode(
        x=alt.X('downloads:Q', scale=alt.Scale(type='log')),
        y='cumulative_count:Q',
        opacity=alt.value(0),
    ).add_selection(
        selection
    )

    datavzrd_point = alt.Chart(df[df['package'] == 'datavzrd']).mark_point(color='red', size=100).encode(
        x=alt.X('downloads:Q', scale=alt.Scale(type='log')),
        y='cumulative_count:Q'
    )

    final_chart = base + points + datavzrd_point

    final_chart.save('downloads_cdf.html')
else:
    print("Package 'datavzrd' not found in the data.")
