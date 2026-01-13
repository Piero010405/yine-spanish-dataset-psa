"""
IO utilities for saving data.
"""
import csv
import os
import logging
import requests

def save_csv(path, rows, fieldnames):
    """
    Save data to a CSV file.

    Args:
        path (str): The file path to save the CSV.
        rows (list): A list of dictionaries representing the rows.
        fieldnames (list): A list of field names for the CSV columns.
    
    Returns:
        None
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def safe_request(url, timeout):
    """
    Makes a safe HTTP GET request with error handling.
    Args:
        url (str): The URL to request.
        timeout (int): Timeout for the request in seconds.
    Returns:
        Response object if successful, None otherwise.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except Exception as e:
        logging.warning("Error al obtener %s: %s", url, e)
        return None

def ensure_dir(path):
    """
    Ensure that a directory exists; create it if it doesn't.
    Args:
        path (str): The directory path to ensure.
    """
    os.makedirs(path, exist_ok=True)
