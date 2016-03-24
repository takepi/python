import xml.etree.ElementTree as ET

tree = ET.parse("/home/pi/program/camera/polecolor.xml")
root = tree.getroot()

for child in root:
	print child.tag, child.attrib
for neighbor in root.iter("place"):
	print neighbor.attrib
for i in root.getiterator("red"):
	print i[0][0]
val = root.find(".//val")
