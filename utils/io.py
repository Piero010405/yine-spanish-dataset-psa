"""
IO utilities for saving data.
"""
import csv
import os

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
