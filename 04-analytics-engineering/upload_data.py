import argparse
import os
import requests
from google.cloud import storage
import gzip


def upload_to_gcs(
    bucket_name, source_file_name, destination_blob_name, credentials_path, folder_name=None
):
    """Uploads a file to the bucket, optionally into a specified folder."""
    storage_client = storage.Client.from_service_account_json(credentials_path)
    bucket = storage_client.bucket(bucket_name)
    if folder_name:
        destination_blob_name = f"{folder_name}/{destination_blob_name}"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def main(params):
    url_file_path = params.url_file_path  # Path to the file containing URLs
    bucket_name = params.bucket_name
    credentials_path = params.credentials_path
    folder_name = params.folder_name  # Folder name within the bucket

    # Read URLs from file
    with open(url_file_path, "r") as file:
        url_list = [line.strip() for line in file if line.strip()]

    for url in url_list:
        # Download the file
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to download {url}. Status code: {response.status_code}")
            continue

        source_file_name = os.path.basename(url)
        with open(source_file_name, "wb") as f:
            f.write(response.content)

        # Extract if it's a .gz file
        if source_file_name.endswith(".gz"):
            csv_file_name = source_file_name[:-3]  # Remove .gz extension
            try:
                with gzip.open(source_file_name, "rb") as f_in, open(
                    csv_file_name, "wb"
                ) as f_out:
                    f_out.write(f_in.read())
                os.remove(source_file_name)  # Remove the .gz file
            except gzip.BadGzipFile:
                print(f"The file {source_file_name} is not a valid gzipped file.")
                os.remove(source_file_name)  # Remove the invalid file
                continue
        else:
            csv_file_name = source_file_name

        # Upload CSV to GCS
        upload_to_gcs(bucket_name, csv_file_name, csv_file_name, credentials_path, folder_name)

        # Remove the local CSV file
        os.remove(csv_file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload files from URLs to Google Storage Bucket"
    )
    parser.add_argument(
        "--url_file_path", help="Path to the file containing URLs", required=True
    )
    parser.add_argument(
        "--bucket_name", help="Google Storage bucket name", required=True
    )
    parser.add_argument(
        "--credentials_path",
        help="Path to the service account JSON file",
        required=True,
    )
    parser.add_argument(
        "--folder_name", help="Folder name within the bucket", required=False
    )
    args = parser.parse_args()
    main(args)
