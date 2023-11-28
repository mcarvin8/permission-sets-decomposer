import logging
import sys
import xml.etree.ElementTree as ET

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
PERM_TYPE = ['PermissionSet']
ns = {'sforce': 'http://soap.sforce.com/2006/04/metadata'}

def read_package_xml(package_path):
    """Read the package.xml file to get a list of PermissionSet names."""
    permission_sets = []
    tree = ET.parse(package_path)
    root = tree.getroot()

    for metadata_type in root.findall('sforce:types', ns):
        metadata_name = metadata_type.find('sforce:name', ns).text
        if metadata_name in PERM_TYPE:
            metadata_members = metadata_type.findall('sforce:members', ns)
            for member in metadata_members:
                permission_sets.append(member.text)
    if not permission_sets:
        logging.info('Permission sets were not found in the package.')
        logging.info('Skipping permission set compilation.')
        sys.exit(0)
    return permission_sets
