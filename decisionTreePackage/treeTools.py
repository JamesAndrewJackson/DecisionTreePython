from decisionTreePackage.decTreeNode import Node
from decisionTreePackage.dataBase import DataBase
from collections import OrderedDict
from decisionTreePackage.cdf import CDF

class TreeTools:
	def buildTree(self, dbase, cases, attrIndicies):
		isTrue = dbase.getCasesWithAttrValue(cases, dbase.getNumAttributes() - 1, "True")
		isFalse = dbase.getCasesWithAttrValue(cases, dbase.getNumAttributes() - 1, "False")
		if(isTrue == cases):
			#print ("All TRUE")
			#print (cases)
			#input('Press <ENTER> to continue')
			return Node(cases, -1, dbase, "True")
		elif(isFalse == cases):
			#print ("All False")
			#print (cases)
			#input('Press <ENTER> to continue')
			return Node(cases, -1, dbase, "False")
		bestAttr = self.findBestAttr(cases, attrIndicies, dbase)
		attrValue = dbase.getAttributeValues(bestAttr)
		attrLabel = dbase.getLabelValues(bestAttr)
		newRoot = Node(cases, bestAttr, dbase, attrLabel)
		childAttr = list(attrIndicies)
		childAttr.remove(bestAttr)
		'''print("ATTRINDICIES")
		print(attrIndicies)
		print("CHILDATTR")
		print(childAttr)
		print("BEST")
		print(bestAttr)
		print("ATTRLABEL")
		print(attrLabel)
		print("ATTRVALUE")
		print(attrValue)'''
		temp = []
		for attr in attrValue:
			childCases = dbase.getCasesWithAttrValue(cases, bestAttr, attr)
			
			for x in childCases:
				temp.append(x) 
			#print("***Child Data***")
			#print(newRoot)
			#print(attr)
			#print(childCases)
			#print(bestAttr)
			#input('Press <ENTER> to continue')
			child = self.buildTree(dbase, childCases, childAttr)
			newRoot.addChild(attr, child)
		#if (set(temp) != set(cases)):
			#print ("SHITS GONE WRONG")
			#print(OrderedDict.fromkeys(temp))
			#print(OrderedDict.fromkeys(cases))
			#input("Press <ENTER> to continue")
		return newRoot

	def findBestAttr(self, cases, attrIndicies, dbase):
		#print ("FINDBESTATTR")
		best = -1
		bestEntropy = 0.0
		for i in range(len(attrIndicies)):
			attrSingleIndex = attrIndicies[i]
			tempEntropy = 0.0
			attrList = dbase.getAttributeValues(attrSingleIndex)
			'''print ("CUR LABEL")
			print (dbase.labelData[attrSingleIndex])
			print ("CUR ATTRLIST: ")
			print (attrList)'''
			for attr in attrList:
				'''print ("CUR ATTR: ")
				print (attr)'''
				subset = dbase.getCasesWithAttrValue(cases, attrSingleIndex, attr)
				tempEntropy += dbase.getEntropy(subset)
			if (best < 0 or tempEntropy < bestEntropy):
				best = i
				bestEntropy = tempEntropy
		#print ("END FINDBESTATTER")
		return attrIndicies[best]

	def printTree(self, nodeToPrint, toPrint, lv):
		#print(nodeToPrint)
		toPrint = ("        " * lv) + toPrint + "--->" + str(nodeToPrint)
		print (toPrint)
		'''print(len(nodeToPrint.children))
		print( print([str(item) for item in nodeToPrint.children]))
		input('Press <ENTER> to continue')'''
		for i in range(len(nodeToPrint.children)):
			#print( nodeToPrint.children[i])
			#input('Press <ENTER> to continue')
			child = nodeToPrint.children[i]
			childLabel = nodeToPrint.childrenLabels[i]
			self.printTree(child, childLabel, lv + 1)

	def dotOutput (self, nodeToPrint, wFile):
		self.labelCount = 0
		wFile.write("digraph G \n{\n")
		wFile.write('	L0 [shape=parallelogram, color=darkslateblue, fontcolor=white, style=filled, label="' + nodeToPrint.label + '"];\n')
		for i in range(len(nodeToPrint.children)):
			self.dotOutputRec(nodeToPrint.children[i], wFile, "L0", nodeToPrint.childrenLabels[i])
		wFile.write("}")

	def dotOutputRec(self, nodeToPrint, wFile, parentLabel, transitionLabel):
		self.labelCount += 1
		curlabelCount = self.labelCount
		curLabel = "L" + str(curlabelCount)
		wFile.write("	" + parentLabel + " -> " + curLabel + " [label=\"" + transitionLabel + '"];\n')
		if (nodeToPrint.label == "False"):
			wFile.write("	" + curLabel + " [style=filled, shape=box, color=red, fontcolor=black, label=False]\n")
		elif (nodeToPrint.label == "True"):
			wFile.write("	" + curLabel + " [style=filled, shape=box, color=green, fontcolor=black, label=True]\n")
		else:
			wFile.write('	' + curLabel + ' [shape=parallelogram, color=darkslateblue, fontcolor=white, style=filled, label="' + nodeToPrint.label + '"];\n')
			for i in range(len(nodeToPrint.children)):
				self.dotOutputRec(nodeToPrint.children[i], wFile, curLabel, nodeToPrint.childrenLabels[i])
		
	def chiSquaredTest(self, node):
		original = []
		if (len(node.children) == 0):
			return
		for child in node.children:
			self.chiSquaredTest(child)
			numTrue = node.dBase.getCasesWithAttrValue(child.cases, node.dBase.getNumAttributes() - 1, "True")
			numFalse = node.dBase.getCasesWithAttrValue(child.cases, node.dBase.getNumAttributes() - 1, "False")
			original.append([len(numTrue), len(numFalse)])
		for row in original:
			x = 0
			for value in row:
				x += value
			row.append(x)
		trueTotal = 0
		falseTotal = 0
		total = 0
		for row in original:
			trueTotal += row[0]
			falseTotal += row[1]
			total += row[2]
		total += trueTotal + falseTotal
		original.append([trueTotal, falseTotal, total])

		expected = []
		for rowIndex in range(len(original)-1):
			expected.append([])
			for colIndex in range(len(original[0])-1):
				rowTotal = original[rowIndex][len(original[rowIndex])-1]
				colTotal = original[len(original)-1][colIndex]
				expected[rowIndex].append((rowTotal * colTotal) / total)

		chiSquared = 0
		for rowIndex in range(len(original)-1):
			for colIndex in range(len(original[0])-1):
				v = original[rowIndex][colIndex]
				e = expected[rowIndex][colIndex]
				chiSquared += (v - e)**2 / e

		if (CDF.cdfResult((len(original) - 2)) > chiSquared):
			self.prune(node)

	def prune(self, node):
		totalTrue = 0
		totalFalse = 0
		for child in node.children:
			totalTrue += len(node.dBase.getCasesWithAttrValue(child.cases, node.dBase.getNumAttributes() - 1, "True"))
			totalFalse += len(node.dBase.getCasesWithAttrValue(child.cases, node.dBase.getNumAttributes() - 1, "False"))
		trueFalseRatio = totalTrue / totalFalse
		if (trueFalseRatio < 1):
			node.label = "False"
		else:
			node.label = "True"
		node.children = []
		node.childrenLabels = []

