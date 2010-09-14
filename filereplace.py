import sys
import os.path
import re

if len(sys.argv) >= 2:
	templateFilePath = sys.argv[1]

if len(sys.argv) >= 3:
	valueFilePath = sys.argv[2]

if len(sys.argv) >= 4:
	resultFilePath = sys.argv[3]

templateFile = None

# The value file will have one variable per line
# in this format:
# VARIABLE_NAME=value
# variable names can contain letters and underscores only
# variable names and values are separated by a single equals (=) sign
# variable values can contain any characters

# load up the variable values into a dictionary
variables = {}
if os.path.isfile(valueFilePath):
	valueFile = None
	valueFile = open(valueFilePath, 'r')
	for line in valueFile:
		splitLine = line.partition('=')
		variables[splitLine[0]] = splitLine[2].rstrip("\n")
	valueFile.close()

# print variables.keys()

# load up the template file
if os.path.isfile(templateFilePath):
	templateFile = open(templateFilePath, 'r')

# delete the result file
os.remove(resultFilePath)

# load up the result file
resultFile = open(resultFilePath, 'w')

if templateFile != None and resultFile != None:
	for line in templateFile:
		# see if we have variables to replace
		# variables to replace in the template file
		# will look like this:
		# @DB_NAME@
		resultLine = line
		matches = re.finditer("@[A-Za-z_]*@", line)
		for match in matches:
			varName = match.group(0)
			varKey = varName.replace("@", "")
			varVal = ""
			if varKey in variables:
				varVal = variables[varKey]
			print "replacing \"" + varName + "\" with \"" + varVal + "\""
			resultLine = resultLine.replace(varName, varVal)
		resultFile.write(resultLine)

if templateFile != None:
	templateFile.close()

if resultFile != None:
	resultFile.close()

print "File Replace Successful."