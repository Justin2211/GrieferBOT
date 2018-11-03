import os, time

class LogHandler(object):
    def __init__(self):
        pass

    def createOwnLogName(self):
        pass
    
    def createNewLogFolder(self, path):
        os.makedirs("Logs")

    def setOwnLog(self, ownlog):
        self.ownLog = ownlog

    def getOwnLog(self):
        return self.ownLog

    def setLogfile(self, file):
        self.logfile = file

    def getLogfileFromEnv(self):
        file = os.getenv("APPDATA")+"/.minecraft/logs/latest.log"
        self.setLogfile(file)
        return file

    def getLogfile(self):
        return self.logfile

    def writeLineToOwnLog(self, line):
        a = open(self.getOwnLog(), 'a+')
        a.write(line)
        a.close()

    def output(self, line):
        print(out)
        self.writeLineToOwnLog(line)
