# DecisionTreePython
A simple python decision tree library with optional Graphviz output. Includes an example program and data file. 

## Input File Format
* The first line of input files must be labels. 
* Each line will be treated as a new test case.
* Each attribute in a test case must be separated by a ':'
* Every test case needs to have a value for all the attributes
* Spelling / formatting for the attributes must be consistent (false and False will be treated differently)

## Use
To create your own program using this library, please put the *decisionTreePackage* folder into your project folder. Next, place the following in your import.

'''
# Importing the Decision Tree Package
from decisionTreePackage.dataBase import DataBase
from decisionTreePackage.decTreeNode import Node
from decisionTreePackage.treeTools import TreeTools
'''

The main part of the library is broken up into three different parts; the Database, the Nodes, and the TreeTools. 

### Database
The Database will read in correctly formatted data, and create decision trees based on the values (See “Input File Format” for how to format data tables). 

### Nodes
These are the nodes for the decision tree. This class has variables for what database its based off of, what training case its based off of, its attribute number, a label for the node, what its entropy is, its children if there are any, and their labels. Nodes can call 'addChild(childLabel, childNode)' to add a child to the node. There are also repr and str functions for debugging and printing.

### TreeTools
A number of methods built to help build and maintain decision trees. 

#### buildTree
'buildTree(database, cases, attributeIndices)'
Builds a tree from the given databases. Checks if the current case is all true or false. If so, it sets the node as a leaf and returns. Otherwise, it will pick what the best available attribute is from the available list, gets the values for that attribute, gets the label information, creates a node for the current decision, and populates its children recursively before returning the new node. 

#### findBestAttr
'findBestAttr(cases, attributeIndicies, database)'
Finds the best attribute to work from. This is an internal function, and should most likely not be called outside of the buildTree function

#### printTrees
'printTree(nodeToPrint, toPrint, level)'
Prints the tree from the current node. toPrint is the value that is leading to this current node. Normally, you will use this on the root node to print the whole tree, but can be used on individual nodes to show subtrees. The average call on the root will look like the following
'''
# Print the tree
tTools = TreeTools()
tTools.printTree(root, "root", 0)
'''
where root is the root node of a tree

#### dotOutput
'dotOutput(nodeToPrint, fileToWriteTo)'
This creates a graphviz “.dot” file, which can be used with the graphviz software to display a visual representation of the decision tree. This is the method you call initially to start the creation of the file. 

You can learn more about the graphviz program here:
www.graphviz.org

#### dotOutputRec
'dotOutputRec(nodeToPrint, fileToWriteTo, parrentLabel, transitionLabel)'
This is the recursive function for the graphviz file creator. It works node per node, creating an appropriate node in the graphviz format, writes the node into the file, and then recursively calls this function on all the nodes children. This shouldn't be called directly, but instead though the 'dotOutput' function. 

#### chiSquaredTest
'chiSquaredTest(nodeToTest)'
This method will apply the Chi-Square test on the provided node, which will decide whether or not a node is significant enough to remain on the tree or not. If it isn't, this function calls a pruning function that will change the insignificant node into a leaf node of the appropriate type. 

For more information about Chi-Squared, I suggest the following link for the basics:
http://www2.lv.psu.edu/jxm57/irp/chisquar.html

#### Prune
'prune(nodeToPrune)'
Takes in a node, and decides if it should become a true or false leaf node. It will also clear off its children, and their labels from the node. 

## Example
See the main.py file for an example program showing how this library can be used. The provided 'Restaurants.txt' file is already formatted and ready to be used with this example. 