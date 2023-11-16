import argparse
import logging
import xml.etree.ElementTree as ET
import os

ns = {'sforce': 'http://soap.sforce.com/2006/04/metadata'}
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

# tags which have children objects
XML_TAGS = ['applicationVisibilities', 'classAccesses', 'customMetadataTypeAccesses',
            'customSettingAccesses', 'externalDataSourceAccesses', 'fieldPermissions',
            'objectPermissions', 'pageAccesses', 'recordTypeVisibilities',
            'tabSettings', 'userPermissions', 'customPermissions',
            'flowAccesses']
# tags which do not have children - text or boolean
SINGLE_TAGS = ['description', 'has_activation_required', 'label', 'license', 'userLicense']


def parse_args():
    """
        Function to parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='A script to create permissionsets.')
    parser.add_argument('-o', '--output', default='force-app/main/default/permissionsets')
    args = parser.parse_args()
    return args


def extract_full_name(element, namespace):
    """Extract the full name from a given XML element."""
    name_tags = ['application', 'apexClass', 'name', 'externalDataSource', 'flow',
                'object', 'apexPage', 'recordType', 'tab', 'field']

    full_name_element = None
    for name_tag in name_tags:
        full_name_element = element.find(f'sforce:{name_tag}', namespace)
        if full_name_element is not None:
            return full_name_element.text
    return None


def create_single_element_xml_file(tag_name, value, perm_directory, parent_perm_name):
    """Create a new XML file for a single element."""
    output_filename = f'{perm_directory}/{parent_perm_name}.{tag_name}.xml'
    # Create an ElementTree with a root element
    root = ET.Element(tag_name)

    # Set the text content for the element
    root.text = value

    # Create an ElementTree object
    tree = ET.ElementTree(root)

    # Write the ElementTree to a file
    with open(output_filename, "wb") as file:
        tree.write(file)



def create_sub_element_xml_file(label, perm_directory, parent_perm_name, tag, full_name):
    """Create a new XML file for a element with sub-elements."""
    output_filename = f'{perm_directory}/{parent_perm_name}.{tag}_{full_name}.xml'

    # Remove the namespace prefix from the element tags
    for element in label.iter():
        if '}' in element.tag:
            element.tag = element.tag.split('}')[1]

    # Create a new XML ElementTree with the label as the root
    element_tree = ET.ElementTree(label)

    # Create a new XML file for each element
    with open(output_filename, 'wb') as file:
        # Add the XML header to the file
        file.write(b'<?xml version="1.0" encoding="UTF-8"?>\n    ')
        element_tree.write(file, encoding='utf-8')

    logging.info(f"Saved {tag} element content to {output_filename}")


def process_perm_file(perm_directory, filename):
    """Process a single perm set file and extract elements."""
    # Extract the parent perm set name from the XML file name
    parent_perm_name = filename.split('.')[0]
    perm_file_path = os.path.join(perm_directory, filename)

    tree = ET.parse(perm_file_path)
    root = tree.getroot()

    # Extract values for invididual elements
    for tag in SINGLE_TAGS:
        full_name_element = root.find(f'sforce:{tag}', ns)
        if full_name_element is not None:
            create_single_element_xml_file(tag, full_name_element.text, perm_directory, parent_perm_name)

    # Iterate through the specified XML tags
    for tag in XML_TAGS:
        for _, label in enumerate(root.findall(f'sforce:{tag}', ns)):
            full_name = extract_full_name(label, ns)
            if full_name:
                create_sub_element_xml_file(label, perm_directory, parent_perm_name, tag, full_name)
            else:
                logging.info(f"Skipping {tag} element without fullName")


def separate_perms(perm_directory):
    """Separate perm sets into individual XML files."""
    # Iterate through the directory to process files
    for filename in os.listdir(perm_directory):
        if filename.endswith(".permissionset-meta.xml"):
            process_perm_file(perm_directory, filename)


def main(output_directory):
    """
    Main function
    """
    separate_perms(output_directory)


if __name__ == '__main__':
    inputs = parse_args()
    main(inputs.output)
