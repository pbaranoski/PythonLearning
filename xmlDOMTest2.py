import os

from xml.dom.minidom import parse
import xml.dom.minidom


inDir = r'C:\Users\user\Documents\PythonLearning\LandingDir'

# Example of XML
'''
<collection shelf="New Arrivals">
<movie title="Enemy Behind">
   <type>War, Thriller</type>
   <format>DVD</format>
   <year>2003</year>
   <rating>PG</rating>
   <stars>10</stars>
   <description>Talk about a US-Japan war</description>
'''

def processFileXML(loadFile):
    tblEntries = loadFile.getElementsByTagName("Table")
    for tblEntry in tblEntries:
        if tblEntry.hasAttribute("id"):
            if tblEntry.getAttribute("id") == "Column":
                tblColumns = tblEntry.getElementsByTagName("Column")

                for tblColumn in tblColumns:
                    if tblColumn.getAttribute("id") == "Name":
                        print("Column is "+ tblColumn.childNodes[0].data)

                    print("Column attribute:"+ tblColumn.getAttribute("id"))    
                    if len(tblColumn.childNodes) > 0:
                        print(tblColumn.childNodes[0].data)
                    else:
                        print("Value is null.")    



if __name__ == "__main__":

    xmlFile = os.path.join(inDir,"DPRconfig.xml")
    print("xmlFile: "+xmlFile)

    # Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse(xmlFile)
    collection = DOMTree.documentElement

    # Get all the movies in the collection
    loadFiles = collection.getElementsByTagName("InFile")
    for loadFile in loadFiles:
        if loadFile.hasAttribute("id"):
            if loadFile.getAttribute("id") == "157_DUE":
                processFileXML(loadFile)
            else:
                pass
                #print(loadFile.getAttribute("id"))    



