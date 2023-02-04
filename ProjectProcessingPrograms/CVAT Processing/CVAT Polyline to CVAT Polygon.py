import xml.etree.ElementTree as ET

# parse the xml file
tree = ET.parse("Files/annotations.xml")
root = tree.getroot()

# loop through all elements in the xml tree
for image in root.findall("./image"):
    for polygon in image.findall("./polyline"):
        polygon.tag = "polygon"

# write the updated xml tree to a file
tree.write("annotationsNew.xml")
print("Done")



