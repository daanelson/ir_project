import xml.etree.ElementTree as ET
import os

topic_path = '/Users/quinnmac/Documents/GradIR/topics2015A.xml'
tree = ET.parse(topic_path)
root = tree.getroot()
descriptions = []
for topic in root:
	# 0 for description, 1 for summary
    descriptions.append(topic[1].text)

for i, d in enumerate(descriptions):
    cmd = 'echo "%s" > topics2015A_%d.txt' % (d.encode('ascii', 'ignore'), i+1)
    os.popen(cmd)
