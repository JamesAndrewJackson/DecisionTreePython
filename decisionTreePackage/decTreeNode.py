
class Node:

	def __init__(self, trainingCaseIndicies, attrNum, dbase, label):
		self.dBase = dbase
		self.cases = trainingCaseIndicies
		self.attrNum = attrNum
		self.label = label
		self.entropy = self.dBase.getEntropy(self.cases)
		self.children = []
		self.childrenLabels = []

	def addChild(self, label, child):
		#print("I am adding \'" + child.label + "\' to parent '" + self.label + "' on connection '" + label + "'")
		#input('Press <ENTER> to continue')
		self.children.append(child)
		self.childrenLabels.append(label)

	def __repr__(self):
		return "Node()"

	def __str__(self):
		return "Node: " + self.label