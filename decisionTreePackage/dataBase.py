from collections import OrderedDict
from math import log
import fileinput

class Database:

            #Creates a Database, using the given file as its initial data
            def __init__(self, fileName):
                        self.readFile(fileName)

            #Parses and sets the values of the database
            def readFile(self, fileName):
                        self.caseData = []
                        self.attrValues = []
                        rawAttrValues = []
                        rawFile = open(fileName, 'r')
                        self.labelData = rawFile.readline().replace('\n','').split(":")
                        for i in range(len(self.labelData)):
                                    rawAttrValues.append([])
                        for line in rawFile:
                                    temp = line.replace('\n','').split(":")
                                    if (temp != ['']):
                                                self.caseData.append(temp)
                                                for i in range(len(temp)):
                                                            rawAttrValues[i].append(temp[i])
                        for attrList in rawAttrValues:
                                    self.attrValues.append(sorted(list(OrderedDict.fromkeys(attrList))))
                        rawFile.close()

            #Finds and returns the cases that contain the requested attribute 
            def getCasesWithAttrValue(self, caseNums, attrNum, attrVal):
                        subsetCaseNums = []
                        for case in caseNums:
                                    if (self.caseData[case][attrNum] == attrVal):
                                                subsetCaseNums.append(case)
                        return subsetCaseNums

            #Returns the current entropy for the passed cases
            def getEntropy(self, cases):
                        H = 0.0
                        resultCol = len(self.attrValues) - 1
                        for attr in self.attrValues[resultCol]:
                                    subset = self.getCasesWithAttrValue(cases, resultCol, attr)
                                    if (len(subset) == 0):
                                                continue
                                    percent = float(len(subset)) / float(len(cases))
                                    H += percent * log(1.0/percent, 2.0)
                        return H

            def getTrainingCase(self, caseToReturn):
                        return self.caseData[caseToReturn]

            def getNumTrainingCases(self):
                        return len(self.caseData)

            def getAttributeValues(self, attrNum):
                        return self.attrValues[attrNum]

            def getNumAttributes(self):
                        return len(self.attrValues)

            def getLabelValues(self, labelNum):
                        return self.labelData[labelNum]

            def getNumLabels(self):
                        return len(self.labelData)

            #Prints the database to the console
            def printDatabase(self):
                        print("ATTR LIST:")
                        print(self.attrValues)
                        print("LABLES:")
                        print(self.labelData)
                        print("DATA:")
                        for line in self.caseData:
                                    print (line)

            def __repr__(self):
                        return "Database()"

            def __str__(self):
                        toPrint = "";
                        toPrint = toPrint + "ATTR LIST: \n"
                        toPrint = toPrint + self.attrValues + "\n"
                        toPrint = toPrint + "LABLES: \n"
                        toPrint = toPrint + self.labelData + "\n"
                        toPrint = toPrint + "DATA: \n"
                        for line in self.caseData:
                                    toPrint = toPrint + line + "\n"
                        return toPrint