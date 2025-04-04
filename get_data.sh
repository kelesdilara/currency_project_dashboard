#!/usr/bin/env bash

# Prompt the user for currency codes
read -p "Enter currency codes separated by spaces (e.g., USD TRY SEK): " -a currencies

# European Central Bank URL for XML files
base_url="https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html"

# Loop through the each currency code provided
for currency in "${currencies[@]}"; do
  # Construct the URL for the currency's XML file
  xml_url="${base_url}/${currency,,}.xml"

  # Define the output CSV file name
  csv_file="${currency,,}.csv"

  # Download the XML file using curl
  echo "Downloading data for ${currency}..."
  curl -s "$xml_url" -o "${currency,,}.xml"

  # Check if the XML file was downloaded successfully.
  if [[ ! -f "${currency,,}.xml" ]]; then
    echo "Failed to download ${xml_url}"
    continue
  fi
  # Parse the XML and convert to CSV
  echo "Converting ${currency} data to CSV..."
  echo "date,value" > $csv_file
  grep '<Obs ' "${currency,,}.xml" | \
  sed -E 's/.*TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]+)".*/\1,\2/' >> "$csv_file"

  # Clean up the downloaded XML file
  rm "${currency,,}.xml"
  echo "${currency} data has been saved to ${csv_file}"

  python data_handler.py "${currency,,}"
  echo "Data saved into the db"
  echo "Removing csv file"
  rm "${currency,,}.xml"
done