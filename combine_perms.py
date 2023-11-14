import argparse
import logging
import os
import xml.etree.ElementTree as ET

import parse_package

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
# tags which have children objects
XML_TAGS = ['applicationVisibilities', 'classAccesses', 'customMetadataTypeAccesses',
            'customSettingAccesses', 'externalDataSourceAccesses', 'fieldPermissions',
            'objectPermissions', 'pageAccesses', 'recordTypeVisibilities',
            'tabSettings', 'userPermissions', 'customPermissions',
            'flowAccesses']
# tags which do not have children - text or boolean
SINGLE_TAGS = ['description', 'has_activation_required', 'label', 'license']


def parse_args():
    """
        Function to parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='A script to create permission sets.')
    parser.add_argument('-o', '--output', default='force-app/main/default/permissionsets')
    parser.add_argument('-m', '--manifest', default=False, action='store_true')
    parser.add_argument('-p', '--package', default='manifest/package.xml')
    args = parser.parse_args()
    return args


def read_individual_xmls(perm_directory, manifest, package_path):
    """
        Read each XML file
    """
    individual_xmls = {}
    if manifest:
        package_sets = parse_package.read_package_xml(package_path)
    else:
        package_sets = None

    for filename in os.listdir(perm_directory):
        if filename.endswith('.xml') and not filename.endswith('.permissionset-meta.xml'):
            parent_perm_name = filename.split('.')[0]
            if not manifest or (manifest and parent_perm_name in package_sets):
                individual_xmls.setdefault(parent_perm_name, [])
                tree = ET.parse(os.path.join(perm_directory, filename))
                root = tree.getroot()
                individual_xmls[parent_perm_name].append(root)

    return individual_xmls


def merge_xml_content(individual_xmls):
    """
        Merge XMLs for each object
    """
    merged_xmls = {}
    for parent_perm_name, individual_roots in individual_xmls.items():
        parent_perm_root = ET.Element('PermissionSet', xmlns="http://soap.sforce.com/2006/04/metadata")

        for tag in SINGLE_TAGS:
            matching_roots = [root for root in individual_roots if root.tag == tag]
            for matching_root in matching_roots:
                # Extract text content from single-element XML and append to the parent
                text_content = matching_root.text
                if text_content:
                    child_element = ET.Element(tag)
                    child_element.text = text_content
                    parent_perm_root.append(child_element)

        for tag in XML_TAGS:
            matching_roots = [root for root in individual_roots if root.tag == tag]
            for matching_root in matching_roots:
                child_element = ET.Element(tag)
                parent_perm_root.append(child_element)
                child_element.extend(matching_root)

        merged_xmls[parent_perm_name] = parent_perm_root

    return merged_xmls


def format_and_write_xmls(merged_xmls, perm_directory):
    """
        Create the final XMLs
    """
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    for parent_perm_name, parent_perm_root in merged_xmls.items():
        parent_xml_str = ET.tostring(parent_perm_root, encoding='utf-8').decode('utf-8')
        formatted_xml = parent_xml_str.replace('><', '>\n    <')

        parent_perm_filename = os.path.join(perm_directory, f'{parent_perm_name}.permissionset-meta.xml')
        with open(parent_perm_filename, 'wb') as file:
            file.write(xml_header.encode('utf-8'))
            file.write(formatted_xml.encode('utf-8'))


def combine_perms(perm_directory, manifest, package_path):
    """
        Combine the perm sets for deployments
    """
    individual_xmls = read_individual_xmls(perm_directory, manifest, package_path)
    merged_xmls = merge_xml_content(individual_xmls)
    format_and_write_xmls(merged_xmls, perm_directory)

    logging.info('The permission sets have been compiled for deployments.')


def main(output_directory, manifest, package_path):
    """
        Main function
    """
    combine_perms(output_directory, manifest, package_path)


if __name__ == '__main__':
    inputs = parse_args()
    main(inputs.output, inputs.manifest, inputs.package)
