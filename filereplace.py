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
	valueFile = open(valueFilePath, 'r')
	
	lineNum = 0
	for line in valueFile:
		
		lineNum += 1
		# lines that begin with hash or pound sign (#) are comments
		if line[0] != "#" and line[0] != '\n':
			if '=' in line:
				splitLine = line.partition('=')
				variables[splitLine[0]] = splitLine[2].rstrip("\n")
			else:
				print "Warning: Invalid syntax in value file at line " + str(lineNum) + ": missing \"=\""
		
	valueFile.close()	
else:
	sys.exit("Error: Value file does not exist.")

# load up the template file
if os.path.isfile(templateFilePath):
	templateFile = open(templateFilePath, 'r')
else:
	sys.exit("Error: Template file does not exist.")

# delete the result file if necessary
if os.path.isfile(resultFilePath):
	os.remove(resultFilePath)

# load up the result file
resultFile = open(resultFilePath, 'w')

if templateFile != None and resultFile != None:

	# add all vars to this list to begin with and remove them as they are used
	notUsedVars = []
	for key in variables.keys():
		notUsedVars.append(key)
		
	missingVars = []
	
	for line in templateFile:
	
		# see if we have variables to replace
		# variables to replace in the template file
		# will look like this:
		# @DB_NAME@
		# @ can be escaped in a template when preceeded by a single \
		resultLine = line
		matches = re.finditer("(?<!\\\\)@[A-Za-z_]*(?<!\\\\)@", line)
		
		for match in matches:
		
			varName = match.group(0)
			varKey = varName.replace("@", "")
			varVal = ""
			
			if varKey in variables:
				varVal = variables[varKey]
			elif varKey not in missingVars:
				missingVars.append(varKey)
			
			if varKey in notUsedVars:
				notUsedVars.remove(varKey)
			
			resultLine = resultLine.replace(varName, varVal)
			
		# write the resulting line to the result file
		# make sure escaped @'s (\@) are replaced with regular old @'s
		resultFile.write(resultLine.replace("\\@", "@"))
	
	if len(missingVars) > 0: 
		for var in missingVars:
			print "Warning: Missing variable in value file: \"" + var + "\""

	if len(notUsedVars) > 0:
		for notUsed in notUsedVars:
			print "Warning: Variable not used in template file: \"" + notUsed + "\""
			
if templateFile != None:
	templateFile.close()

if resultFile != None:
	resultFile.close()

print "\nFile Replace Successful."