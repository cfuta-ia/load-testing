import csv, uuid, os

PATH = os.path.join(os.getcwd(), 'logs')
HEADERS = ['current_count', 'max_count', 'time_stamp']

def createCSV():
    """Create the csv file with the given CSV filename with a uuid appended
    
    Args:
        filename: name of the csv file
    Returns:
        the full csv file name
    """
    filename = f'load-test-{uuid.uuid4()}.csv'
    writeTo(filename, *HEADERS)
    return filename

def writeTo(filename, *values):
    """Write to the csv file by adding a row
    
    Args:
        filepath: path to the file in the logs directory to write to
        values: values for the row to write
    Returns:
        None
    """
    filepath = os.path.join(PATH, filename)
    with open(filepath, mode='a') as CSV:
        writer = csv.writer(CSV, delimiter=',')
        writer.writerow(list(values))
    return None

