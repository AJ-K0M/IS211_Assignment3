import argparse
import csv
import datetime
import re

def processData(file_path):
    """
    Processes the CSV file and returns a list of log entries as dictionaries
    """
    log_entries = []

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row) == 5:
                log_entries.append({
                    'path': row[0],                      
                    'datetime': row[1],                  
                    'user_agent': row[2],                
                    'status': int(row[3]),               
                    'size': int(row[4])                  
                })
    return log_entries

def imageHits(log_entries):
    """
    Finds image hits and prints the percentage of requests that are for images.
    
    """
    
    image_search = re.compile(r'\.(jpg|jpeg|png|gif|bmp)$', re.IGNORECASE)
    image_hits = sum(1 for entry in log_entries if image_search.search(entry['path']))
    total_hits = len(log_entries)
    if total_hits:
        print(f"Image requests account for {image_hits / total_hits * 100:.2f}% of all requests")
    else:
        print("No entries found in the log file.")

def popularBrowser(log_entries):
    """
    Analyzes browser usage from the log entries and prints the most popular browser.
    """
    
    browser_counts = {"Firefox": 0, "Chrome": 0, "IE": 0, "Safari": 0}

    for entry in log_entries:
        user_agent = entry['user_agent']  
        
        if re.search(r"Firefox", user_agent):
            browser_counts["Firefox"] += 1
        elif re.search(r"Chrome", user_agent):
            browser_counts["Chrome"] += 1
        elif re.search(r"MSIE|Trident", user_agent):  
            browser_counts["IE"] += 1
        elif re.search(r"Safari", user_agent):
            browser_counts["Safari"] += 1

    most_popular = max(browser_counts, key=browser_counts.get)
    print(f"Most popular browser: {most_popular} with {browser_counts[most_popular]} hits.")

def hourlyHits(log_entries):
    """
    Analyzes the log entries and prints the total hits per hour.
    """

    hourly_hits = [0] * 24  

    for entry in log_entries:
        dt = datetime.datetime.strptime(entry['datetime'], "%Y-%m-%d %H:%M:%S")
        hour = dt.hour
        hourly_hits[hour] += 1  

    for hour in range(24):
        print(f"Hour {hour:02} has {hourly_hits[hour]} hits.")


def main(file_path):
    print(f"Running main with file = {file_path}...")
    log_entries = processData(file_path)  
    imageHits(log_entries) 
    popularBrowser(log_entries)
    hourlyHits(log_entries)

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to the log file", type=str, required=True)
    args = parser.parse_args()
    main(args.file)
