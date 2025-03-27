import os
import json
import csv
import xml.etree.ElementTree as ET

def check_dir_exists(filepath):
    """Check if folder exists, if not, create it."""
    if os.path.isdir(os.path.dirname(filepath)) == False:
        os.makedirs(os.path.dirname(filepath))

def read_json(path : str) -> dict:
    """Read a json file"""
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() == ".json":
            with open(path, 'r') as f:
                return json.load(f)
        else:
            print(f"{path} is not a json file.")
            return None
    else:
        print(f"{path} doesn't exist.")
        return None

def read_txt(path : str) -> str:
    """Read a file as raw text."""
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f.read()
    else:
        print(f"{path} doesn't exist.")
        return None

def read_csv(path : str, delimiter : str = ',', quotechar : str = '"') -> list[list]:
    """Read a csv file and return 2D list."""
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() == ".csv":
            content = []
            with open(path, 'r') as f:
                csv_reader = csv.reader(f, delimiter = delimiter, quotechar = quotechar)
                for row in csv_reader:
                    content.append(row)
            return content
        else:
            print(f"{path} is not a csv file.")
            return None
    else:
        print(f"{path} doesn't exist.")
        return None
    
def read_xml(path : str) -> ET:
    """Read an xml file and return as xml.etree.ElementTree"""
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() == ".xml":
            tree = ET.parse(path)
            root = tree.getroot()
            return root
        else:
            print(f"{path} is not an xml file.")
            return None
    else:
        print(f"{path} doesn't exist.")
        return None
    
def write_json(path : str, content : dict, indent : int = 4) -> None:
    """
    Write to json. Will create folder if doesn't exist.
    """
    if os.path.splitext(path)[1] == ".json":
        check_dir_exists(path)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii = False, indent = indent)
    else:
        print(f"{path} needs to be a json file.")

def write_txt(path : str, content : str) -> None:
    """
    Write to raw text. Will create folder if doesn't exist.
    """
    check_dir_exists(path)

    with open(path, 'w') as f:
        f.write(content)

def write_csv(path : str, content : list[list]) -> None:
    """
    Write to csv. Will create folder if doesn't exist.
    """
    if os.path.splitext(path)[1] == ".csv":
        check_dir_exists(path)

        with open(path, mode='w') as f:
            writer = csv.writer(f)
            for row in content:
                writer.writerow(row)
    else:
        print(f"{path} needs to be a csv file.")

def write_xml(path : str, content : ET) -> None:
    """
    Write to xml. Will create folder if doesn't exist.
    """
    if os.path.splitext(path)[1] == ".xml":
        check_dir_exists(path)

        content.write(path)
    else:
        print(f"{path} needs to be a xml file.")