# Main Python Imports
import tkinter
import tkinter.filedialog
import getpass
import os

# Importing the Decision Tree Package
from decisionTreePackage.dataBase import DataBase
from decisionTreePackage.decTreeNode import Node
from decisionTreePackage.treeTools import TreeTools

# ---Basic run example---

# tkinter setup
gui = tkinter.Tk()
user = getpass.getuser()

# Getting the file to read
mFileName = tkinter.filedialog.askopenfilename(initialdir='C:/Users/%s' % user, title="Pick file to build tree from")
gui.destroy()

# Creating the database from file
mDataBase = DataBase(mFileName)
###mDataBase.printDataBase()

# Create the tree
tTools = TreeTools()
caseRangeInit = list(range(mDataBase.getNumTrainingCases()))
attrRangeInit = list(range(mDataBase.getNumAttributes() - 1))
root = tTools.buildTree(mDataBase, caseRangeInit, attrRangeInit)

# Print the tree
tTools.printTree(root, "root", 0)

# Find if the user wants to print a DOT result file
input("Press <ENTER> to continue")
print("Create .gv file of tree? Y/N")
answer = input().upper()
if (answer == "Y" or answer == "YES"):
            writeFile = open(mFileName.split('.')[0] + "RESULTS.gv", 'w')
            tTools.dotOutput (root, writeFile)
            writeFile.close() 
            print(mFileName.split('.')[0] + "RESULTS.gv")

# Find if the user wants to chisquare test
print("Prune tree? Y/N")
answer = input().upper()
if (answer == "Y" or answer == "YES"):
            tTools.chiSquaredTest(root)
            tTools.printTree(root, "root", 0)
            input("Press <ENTER> to continue")
            print("Create .gv file of tree? Y/N")
            answer = input().upper()
            if (answer == "Y" or answer == "YES"):
                        writeFile = open(mFileName.split('.')[0] + "RESULTS_PRUNE.gv", 'w')
                        tTools.dotOutput (root, writeFile)
                        writeFile.close()

## Politely end the program
print("Thank you for using this Decision Tree program!")
input("Press <ENTER> to exit the program")

# ---End example ---