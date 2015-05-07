from decisionTreePackage.decTreeNode import Node
from decisionTreePackage.database import Database
from collections import OrderedDict
from decisionTreePackage.cdf import CDF

class TreeTools:

            #Builds a Tree. If the given data is a leaf, returns a true/false leaf node. Otherwise, it
            #picks the best decision from the avaliable options, creates a node for it, and populates its children 
            #via recursively calling itself with the remaining data. 
            def buildTree(self, dbase, cases, attrIndicies):
                        isTrue = dbase.getCasesWithAttrValue(cases, dbase.getNumAttributes() - 1, "True")
                        isFalse = dbase.getCasesWithAttrValue(cases, dbase.getNumAttributes() - 1, "False")
                        if(isTrue == cases):
                                    return Node(cases, -1, dbase, "True")
                        elif(isFalse == cases):
                                    return Node(cases, -1, dbase, "False")
                        bestAttr = self.findBestAttr(cases, attrIndicies, dbase)
                        attrValue = dbase.getAttributeValues(bestAttr)
                        attrLabel = dbase.getLabelValues(bestAttr)
                        newRoot = Node(cases, bestAttr, dbase, attrLabel)
                        childAttr = list(attrIndicies)
                        childAttr.remove(bestAttr)
                        temp = []
                        for attr in attrValue:
                                    childCases = dbase.getCasesWithAttrValue(cases, bestAttr, attr)
                                    
                                    for x in childCases:
                                                temp.append(x) 
                                    child = self.buildTree(dbase, childCases, childAttr)
                                    newRoot.addChild(attr, child)
                        return newRoot

            #Finds the best Attribute to work with from the provided options
            def findBestAttr(self, cases, attrIndicies, dbase):
                        best = -1
                        bestEntropy = 0.0
                        for i in range(len(attrIndicies)):
                                    attrSingleIndex = attrIndicies[i]
                                    tempEntropy = 0.0
                                    attrList = dbase.getAttributeValues(attrSingleIndex)
                                    for attr in attrList:
                                                subset = dbase.getCasesWithAttrValue(cases, attrSingleIndex, attr)
                                                tempEntropy += dbase.getEntropy(subset)
                                    if (best < 0 or tempEntropy < bestEntropy):
                                                best = i
                                                bestEntropy = tempEntropy
                        return attrIndicies[best]

            #Prints the tree via recursive calls. Prints to the command line. 
            def printTree(self, nodeToPrint, toPrint, lv):
                        toPrint = ("        " * lv) + toPrint + "--->" + str(nodeToPrint)
                        print (toPrint)
                        for i in range(len(nodeToPrint.children)):
                                    child = nodeToPrint.children[i]
                                    childLabel = nodeToPrint.childrenLabels[i]
                                    self.printTree(child, childLabel, lv + 1)

            #Creates the graphviz dot file via recursion. This is the initial call that will set up and finish
            #the documentt, as well as call the proper recursive function
            def dotOutput (self, nodeToPrint, wFile):
                        self.labelCount = 0
                        wFile.write("digraph G \n{\n")
                        wFile.write('            L0 [shape=parallelogram, color=darkslateblue, fontcolor=white, style=filled, label="' + nodeToPrint.label + '"];\n')
                        for i in range(len(nodeToPrint.children)):
                                    self.dotOutputRec(nodeToPrint.children[i], wFile, "L0", nodeToPrint.childrenLabels[i])
                        wFile.write("}")

            #Creates a graphviz node for the given tree node, and recursively calls itself on 
            #all of the node's children
            def dotOutputRec(self, nodeToPrint, wFile, parentLabel, transitionLabel):
                        self.labelCount += 1
                        curlabelCount = self.labelCount
                        curLabel = "L" + str(curlabelCount)
                        wFile.write("            " + parentLabel + " -> " + curLabel + " [label=\"" + transitionLabel + '"];\n')
                        if (nodeToPrint.label == "False"):
                                    wFile.write("            " + curLabel + " [style=filled, shape=box, color=red, fontcolor=black, label=False]\n")
                        elif (nodeToPrint.label == "True"):
                                    wFile.write("            " + curLabel + " [style=filled, shape=box, color=green, fontcolor=black, label=True]\n")
                        else:
                                    wFile.write('            ' + curLabel + ' [shape=parallelogram, color=darkslateblue, fontcolor=white, style=filled, label="' + nodeToPrint.label + '"];\n')
                                    for i in range(len(nodeToPrint.children)):
                                                self.dotOutputRec(nodeToPrint.children[i], wFile, curLabel, nodeToPrint.childrenLabels[i])
                        
            # Applies Chi Squared pruning on the tree, which will help remove nodes that are nonimportant.
            # For more information, please visit the following link...
            # http://www2.lv.psu.edu/jxm57/irp/chisquar.html
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

            #The pruning function. Decides if the node will become a true or false leaf node, and
            #removes all of the nodes children
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

