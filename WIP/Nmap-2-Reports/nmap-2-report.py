#!/usr/bin/python3

import json
import xmltodict

xml_file_name = 'ad-set.xml'


# Function to read xml data and create dictionary with json format 
def xml_convert(xml_file_name):
	with open(xml_file_name) as xml_file:
     
	    data_dict = xmltodict.parse(xml_file.read())
	    xml_file.close()
	     
	    # dumps the data and uses loads to put it into a dictonary format
	    json_data = json.loads(json.dumps(data_dict))
	    return json_data


def pretty_print(json_object):
	return json.dumps(json_object, sort_keys=True, indent=4, separators=(',', ': '))


json_data = xml_convert(xml_file_name)
json_dump = json.dumps(json_data)
print(json_data.keys())
print(json_data['nmaprun'].keys())
print(json_data['nmaprun']['host'][3]['ports'].keys())
# print(pretty_print(json_data['nmaprun']['host'][3]['ports']['port'][2]['service']))

holdme = json_data['nmaprun']['host'][0]['ports']['port']

print("\n" + "-" * 10 + "Open Ports" + "-" * 10)
for i in range(len(holdme)):
	print(f"Port: {holdme[i]['@portid']}")
	# print(f"{pretty_print(holdme[i]['service'])}")
	print(f"Method: {holdme[i]['service']['@method']}")
	print(f"Name: {holdme[i]['service']['@name']}")
	try:
		print(f"Product: {holdme[i]['service']['@product']}")	
	except:
		pass
	try:
		print(f"Product: {holdme[i]['service']['@extrainfo']}")	
	except:
		pass
	try:
		print(f"Product: {holdme[i]['service']['@hostname']}")	
	except:
		pass
	print('\n')
