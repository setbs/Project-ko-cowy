import argparse
import json
import yaml
import xml.etree.ElementTree as Etree

def parse_arguments():
    parser = argparse.ArgumentParser(description='Narzędzie do konwersji danych')
    parser.add_argument('input_file', type=str, help='Ścieżka do pliku wejściowego')
    parser.add_argument('output_file', type=str, help='Ścieżka do pliku wyjściowego')
    return parser.parse_args()

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as e:
        print(f"Błąd podczas odczytu pliku JSON: {e}")
        return None

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except yaml.YAMLError as e:
        print(f"Błąd podczas odczytu pliku YAML: {e}")
        return None

def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file)

def load_xml(file_path):
    try:
        tree = Etree.parse(file_path)
        root = tree.getroot()
        return root
    except Etree.ParseError as e:
        print(f"Błąd podczas odczytu pliku XML: {e}")
        return None

def xml_to_dict(element):
    data = {}
    for child in element:
        if len(child):
            data[child.tag] = xml_to_dict(child)
        else:
            data[child.tag] = child.text
    return data

def dict_to_xml(data, root_tag='root'):
    root = Etree.Element(root_tag)
    _dict_to_xml_recurse(data, root)
    return root

def _dict_to_xml_recurse(data, parent):
    for key, value in data.items():
        if isinstance(value, dict):
            child = Etree.SubElement(parent, key)
            _dict_to_xml_recurse(value, child)
        else:
            child = Etree.SubElement(parent, key)
            child.text = str(value)

def save_xml(data, file_path):
    tree = Etree.ElementTree(data)
    tree.write(file_path)

if __name__ == "__main__":
    args = parse_arguments()
    
    data = None

    if args.input_file.endswith('.json'):
        data = load_json(args.input_file)
    elif args.input_file.endswith('.yaml') or args.input_file.endswith('.yml'):
        data = load_yaml(args.input_file)
    elif args.input_file.endswith('.xml'):
        data = load_xml(args.input_file)
        if data is not None:
            data = xml_to_dict(data)
    else:
        print("Nieobsługiwany format pliku wejściowego")

    if data is not None:
        if args.output_file.endswith('.json'):
            save_json(data, args.output_file)
        elif args.output_file.endswith('.yaml') or args.output_file.endswith('.yml'):
            save_yaml(data, args.output_file)
        elif args.output_file.endswith('.xml'):
            xml_data = dict_to_xml(data)
            save_xml(xml_data, args.output_file)
        else:
            print("Nieobsługiwany format pliku wyjściowego")
    else:
        print("Nieudało się załadować pliku wejściowego")