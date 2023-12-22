# System includes
import datetime
import math
import os
import sys
import traceback
import StringIO

_isLoggingEnabled = True
_defaultLogFile = None 
_loggingDepth = 0
_loggingIndent = 0
_logToFile = False

def EnableLogToFile():
	global _logToFile
	_logToFile = True

def DisableLogToFile():
	global _logToFile
	_logToFile = False

def LogToFileEnabled():
	global _logToFile
	return _logToFile


def GetLogName(name=""):
	d = datetime.datetime.now().timetuple()
	return '%02d%02d%02d_%02d%02d%02d_%s_log.txt' % (math.fmod(d[0],100),d[1],d[2],d[3],d[4],d[5], name)


def EnableLogging():
	global _isLoggingEnabled
	_isLoggingEnabled = False


def DisableLogging():
	global _isLoggingEnabled
	_isLoggingEnabled = True


def LoggingEnabled():
	global _isLoggingEnabled
	return _isLoggingEnabled


def IncreaseIndent():
	global _loggingIndent
	_loggingIndent = _loggingIndent + 1


def DecreaseIndent():
	global _loggingIndent
	_loggingIndent = _loggingIndent - 1


def StartLogging():
	global _loggingDepth
	if _loggingDepth == 0:
		if _logToFile == True:
			logFile = GetDefaultLog()
			_LogStringToFile(logFile, "Log Started")
	_loggingDepth = _loggingDepth + 1


def EndLogging():
	global _loggingDepth
	if _loggingDepth == 1:
		if _logToFile == True:
			logFile = GetDefaultLog()
			_LogStringToFile(logFile, "Log Ended")
			EndLog(logFile)
	_loggingDepth = _loggingDepth - 1
	if _loggingDepth < 0:
		_loggingDepth = 0


def SetDefaultLog(logFile):
	global _defaultLogFile
	if LoggingEnabled():
		_defaultLogFile = logFile


def GetDefaultLog():
	global _defaultLogFile
	if _defaultLogFile == None:
		_defaultLogFile = CreateLog("log.txt")
	return _defaultLogFile

logPath = None

def GetLogPath():
	global logPath
	return logPath

def CreateLog(logName, folderPath = ""):
	global logPath
	if folderPath == "":
		folderPath = "."
	folderPath = os.path.expanduser(folderPath)
	logPath = os.path.join(folderPath, logName)
	try:
		EnsureFolderExists(folderPath)
		logFile = open(logPath, "w")
		return logFile
	except:	
		sys.stderr.write("*** Error: Could not create log file at %s.  Disabling logging." % logPath)
		return open("/dev/null", "w")		
	
def EnsureFolderExists(folderPath):
	if not os.path.exists(folderPath):
		try:
			os.makedirs(folderPath)
			print "Created folder %s." % folderPath
		except:
			print "Error creating folder %s" % folderPath
			raise

def EndLog(logFile):
	logFile.close()


def LogString(str, formattingList=[], fIncludeTime = True):
	if _logToFile == True:
		_LogStringToFile(GetDefaultLog(), str)
	_LogStringToTerminal(str, formattingList, fIncludeTime)


def LogAction(action, projectSpec):
	if action[0].islower():
		action = action[0].upper() + action[1:]
	if type(projectSpec) != list:
		projectSpec = [projectSpec]
	for projectSpecT in projectSpec:
		_LogEventCore("->", action, projectSpecT, "...", _loggingIndent, ["bold"])


def LogFailure(action, projectSpec, reason=""):
	suffix = ""
	if len(reason) > 0:
		suffix = " - " + reason
	_LogEventCore("*  Failure", action, projectSpec, suffix, _loggingIndent, ["bold", "red"])


def LogSuccess(action, projectSpec, reason=""):	
	suffix = ""
	if len(reason) > 0:
		suffix = " - " + reason
	_LogEventCore("+  Success", action, projectSpec, suffix, _loggingIndent, [])


def LogUserCancelled(action, projectSpec, reason=""):
	suffix = ""
	if len(reason) > 0:
		suffix = " - " + reason
	_LogEventCore("*  USER CANCELLED:", action, projectSpec, suffix, _loggingIndent, ["bold", "red"])


def _GetIndentString():
	# Get the indent string.
	return "    " * _loggingIndent


def LogText(str, formattingList=[]):
	# Log the string with indenting
	LogString(_GetIndentString() + str, formattingList)


def LogError(str):
	# Log the error string with indenting, in red, without a timestamp.
	LogString(_GetIndentString() + str, ["red"], False)

def LogWarning(str):
	# Log the warning string with indenting, in yellow, without a timestamp.
	LogString(_GetIndentString() + str, ["yellow"], False)

def LogProgress(str):
	# Progress only goes to the terminal and it ends with a carriage-return
	# instead of a linefeed so subsequent output will overwrite it.
	#
	# Log the string with indenting, in blue
	_LogStringToTerminal(_GetIndentString() + str, ["blue"], True, False)


def LogTraceback():
	trace = StringIO.StringIO()
	traceback.print_exc(file=trace)
	
	for line in trace.getvalue().split("\n"):
		LogText(line)
	trace.close()
	

def _LogEventCore(prefix, action, projectSpec, suffix, indent, formattingList):
	# Add the prefix and action.
	str = _GetIndentString() + prefix + " " + action
	# Add the project spec
	for i in range(len(projectSpec)):
		str = str + " " + projectSpec[i]
	# Add the suffix
	str = str + suffix
	# Log the string
	LogString(str, formattingList)


def _LogStringToFile(logFile, out, fIncludeTime = True, fIncludeNewLine = True):
	if LoggingEnabled():
		if fIncludeTime:
			out = _GetDateString() + " " + out
		if fIncludeNewLine:
			out = out + "\n"

		# If the attribute_value is a string and it contains non-ASCII characters, 
		# first decode it as UTF-8 to prevent unicode() from decoding as ASCII
		# and throwing UnicodeDecodeError
		if isinstance(out, str):
			out = out.decode("utf-8")
		
		# Then, re-encode as ASCII replacing UTF-8 characters with a marker like '?'
		# Note, "out" might start out as unicode
		# TODO - bug 242069 - dougfor - add support for UTF-8 logging
		if isinstance(out, unicode):
			out = out.encode("ascii", "replace")

		logFile.write(out)
		logFile.flush()


def _LogStringToTerminal(out, formattingList = [], fIncludeTime = True, fNewline = True):
	dateStr = ""
	
	if fIncludeTime:
		dateStr = _GetDateString()
	
	# If the attribute_value is a string and it contains non-ASCII characters, 
	# first decode it as UTF-8 to prevent unicode() from decoding as ASCII
	# and throwing UnicodeDecodeError
	if isinstance(out, str):
		out = out.decode("utf-8")

	#Modified to use FormatStringToTerminal method
	sys.stdout.write(_GenerateFormattedString(FormatStringToTerminal(out,dateStr), formattingList))
	if fNewline:
		sys.stdout.write('\n')
	else:
		sys.stdout.write('\r')
		sys.stdout.flush()

def FormatStringToTerminal(str, dateStr=""):
	# Added to support the new logger
	filler = ""
	dateLen = len(dateStr)
	totalWidth = len(str) + dateLen
	termWidth = _TerminalWidth()
	# If the line is wider than the terminal, elide text from the middle of the string
	# (If we're not including the timestamp, don't truncate the line, as it contains
	# important information, such as an error message from the compiler.)
	if not (dateStr == "") and totalWidth > termWidth:
		strLen = len(str)
		middle = strLen / 2
		elideWidth = (strLen - (termWidth - dateLen - 1) + 1) / 2
		str = str[0:middle - elideWidth - 2] + "..." + str[middle + elideWidth + 1:strLen]
		totalWidth = len(str) + dateLen
	if totalWidth < termWidth:
		filler = " " * (termWidth - totalWidth)
		
	return str + filler + dateStr

def _GetDateString():
	d = datetime.datetime.now().timetuple()
	return '[%04d/%02d/%02d:%02d:%02d:%02d]' % (d[0],d[1],d[2],d[3],d[4],d[5])


_formattingMap = {   \
	'bold':    '01', \
		'dim':     '02', \
		'italic':  '04', \
		'blink':   '05', \
		'inverse': '07', \
		'seclet':  '08', \
		'black':   '30', \
		'red':     '31', \
		'green':   '32', \
		'yellow':  '33', \
		'blue':    '34', \
		'purple':  '35', \
		'cyan':    '36', \
		'white':   '37', \
		'blackBG': '40', \
		'redBG':   '41', \
		'greenBG': '42', \
		'yellowBG':'43', \
		'blueBG':  '44', \
		'purpleBG':'45', \
		'cyanBG':  '46', \
		'whiteBG': '47'  \
		}


def _GenerateFormattedString(str, formattingList):
	# set up the formatting tags on the front
	strT = '\x1b['
	for format in formattingList:
		strT = strT + _formattingMap[format] + ';'
	strT = strT[:-1] + 'm'
	# add the string to print
	strT = strT + str
	# add the close formatting tag on the back
	strT = strT + '\x1b[00m'
	# return the generated string
	return strT


fCursesInitialized = True
try:
	import curses
	curses.setupterm()
except:
	fCursesInitialized = False

def _TerminalWidth():
	numColumns = 80
	if fCursesInitialized:
		try:
			numColumns = curses.tigetnum('cols')
		except:
			# default to a large width for non-terminals
			numColumns = 1024
	return numColumns
