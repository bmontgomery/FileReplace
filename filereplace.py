import sys
import os.path
import re

def printHelp(extended):
	print "Usage: filereplace.py [TEMPLATE_FILE] [VALUE_FILE] [OUTPUT_FILE]"
	print ""
	print "  TEMPLATE_FILE    Required. This file contains the text in which this script"
	print "                   will replace variable references with their values from"
	print "                   the VALUE_FILE. This file is not edited."
	print ""
	print "  VALUE_FILE       Required. This file contains the variable definitions."
	print "                   Each variable reference in TEMPLATE_FILE will be replaced"
	print "                   with the variable definition in this file. This file is"
	print "                   not edited."
	print ""
	print "  OUTPUT_FILE      Required. This is the file to which the resulting text is"
	print "                   written after all variable replacements have been"
	print "                   performed."
	print ""
	
	if extended:
		print "Notes:"
		print ""
		print "  ---------------------------------------------------------------------------"
		print "  The Template File"
		print ""
		print "  This script will examine the template file for variable references."
		print "  Variable references are formatted like this: \"@VARIABLE_NAME@\" (without"
		print "  the quotes). Variable names can contain letters and underscores (_) and"
		print "  should only be defined once in a value file."
		print ""
		print "  Example:"
		print ""
		print "    <add key=\"DbConnStr\" value=\"server=@DB_SERVER@;database=@DB_NAME@\" />"
		print ""
		print "  If you wish to use an @ symbol in the template file without referencing a"
		print "  a variable, escape it like this: \\@."
		print ""
		print "  ---------------------------------------------------------------------------"
		print "  The Value File"
		print ""
		print "  The value file contains the variable definitions. One variable definition"
		print "  is permitted per line. The variable name must not include the @ symbols."
		print "  The variable name is followed by a single equals (=) sign, then the value"
		print "  with which the script will replace all variable references in"
		print "  TEMPLATE_FILE."
		print ""
		print "  Example:"
		print ""
		print "    DB_SERVER=.\SQLEXPRESS"
		print "    DB_Name=TeamDynamix"

# see if the user is asking for help
if len(sys.argv) == 2 and sys.argv[1].lower() == "help":
	printHelp(True)
	sys.exit()
	
# validate arguments	
if len(sys.argv) != 4:
	printHelp(False)
	sys.exit("Error: incorrect number of arguments.")

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
				varName = splitLine[0]
				if varName not in variables:
					variables[varName] = splitLine[2].rstrip("\n")
				else:
					print "Warning: Variable \"" + varName + "\" defined twice. Original value will be used."
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

print "\nFile generated successfully."