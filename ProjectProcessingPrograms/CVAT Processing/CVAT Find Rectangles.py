import xml.etree.ElementTree as ET


# parse the xml file
tree = ET.parse("annotations.xml")
root = tree.getroot()

has_rectangles = False  # initialize flag to False

# loop through all elements in the xml tree
for image in root.findall("./image"):
    for rectangle in image.findall("./box"):
        has_rectangles = True
        break  # exit the loop as soon as a rectangle is found


if has_rectangles:
    print("Yes")
else:
    print("No")