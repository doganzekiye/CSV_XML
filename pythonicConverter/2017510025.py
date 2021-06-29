import csv
import sys
import xml.etree.ElementTree as ET
from lxml import etree
from io import  StringIO

#to make easier to execute program arguments are given as a string data
#if you want to use argumants please chane the commented lines
inputFile = 'DEPARTMENTS.xml'
#inputFile = sys.argv[1]

outputFile = 'DEPARTMENTS.xsd'
#outputFile = sys.argv[2]

typeF = 7
#typeF = sys.argv[3]

# to check arguments are true
"""print(inputFile)
print(outputFile)
print(typeF)"""

#read csv file , convert to xml and write the xml file part
def convertCSV2XML(inputFile,outputFile):
    with open(inputFile,"r", encoding='utf-8') as csvFile:#reading csv file
        csvReader = csv.reader(csvFile, delimiter=';')#spliting in order to delimiter
        lineCount = 0
        data = []
        for row in csvReader:#read  row by row
            data.append(row)
            lineCount += 1

    def convert_row(row):#creating xml
        return """\t<univercity uName="%s" uType="%s">
        \t\t<item id="%s" faculty="%s">
        \t\t\t<name lang="%s" second="%s">%s</name>
        \t\t\t<period>%s</period>
        \t\t\t<quota spec="%s">%s</quota>
        \t\t\t<field>%s</field>
        \t\t\t<last_min_score order="%s">%s</last_min_score>
        \t\t\t<grant>%s</grant>
        \t\t</item>
        \t</univercity>""" % (row[1], row[0], row[3], row[2], row[5], row[6], row[4],row[8], row[11], row[10], row[9], row[12], row[13], row[7])
    f =open(outputFile,"w",encoding="utf-8")
    f.write('<departmants>')

    for row in data[1:]:#writing xml to file
        f.write("\n".join([convert_row(row)]))
    f.write('</departmants>')
    f.close()

def xsdValidationVersion1(inputFile,outputFile):#validate xml to xsd part version 1
    with open(outputFile,'r') as schemaFile:#reading xsd file
        schemaCheck=schemaFile.read()
    with open(inputFile,'r') as xmlFile:#reading xml file
        xmlCheck=xmlFile.read()

    xmlShemaDoc = etree.parse(StringIO(schemaCheck))
    xmlShema = etree.XMLSchema(xmlShemaDoc)
    #check for the errors
    try:
        doc = etree.parse(StringIO(xmlCheck))
        print('xml well formed')
        
    except IOError:
        print('Invalid File')

    except etree.XMLSyntaxError as err:
        print('XML Syntax Error, see error_syntax.log')
        with open('error_syntax.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
        quit()

    except:
        print('Unknown error, exiting.')
        quit()

    # validate against schema
    try:
        xmlShema.assertValid(doc)
        print('XML valid, schema validation ok.')

    except etree.DocumentInvalid as err:
        print('Schema validation error, see error_schema.log')
        with open('error_schema.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
        quit()

    except:
        print('Unknown error, exiting.')
        quit()

def xsdValidationVersion2(inputFile,outputFile): #validate xml to xsd part version 2
    doc = ET.parse(inputFile)
    root = doc.getroot()
    xmlschema_doc = etree.parse(outputFile)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.XML(ET.tostring(root))
    validation_result = xmlschema.validate(doc)
    print(validation_result)
    xmlschema.assert_(doc)
#check the translation type and execute the right option
if typeF==1:
    convertCSV2XML(inputFile,outputFile)
if typeF==7:
    #xsdValidationVersion1(inputFile,outputFile)
    xsdValidationVersion2(inputFile,outputFile)

#xsdValidationVersion1(inputFile,outputFile)
#xsdValidationVersion2(inputFile,outputFile)
#convertCSV2XML(inputFile,outputFile)