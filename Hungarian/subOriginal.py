import ast
from _ast import *
from scipy.optimize import linear_sum_assignment
import numpy as np
from munkres import Munkres
from main import HungarianAlgo

class SignificantSubTreesComp:
    def __init__(self, tree1: AST, tree2: AST):
        # Constructor method to initialize the class
        # Opens and reads the contents of two Python files into strings
        # Parses the strings into abstract syntax trees (ASTs)
        with open(tree1, "r") as source:
            self.tree1Str = source.read()
        with open(tree2, "r") as source:
            self.tree2Str = source.read()

        self.tree1 = ast.parse(self.tree1Str)
        self.tree2 = ast.parse(self.tree2Str)

    def isSignificant(self, root):
        # Method to determine if a given AST node is significant
        # Returns True if the node is significant, False otherwise
        if isinstance(root, Import):
            return True
        elif isinstance(root, While):
            return True
        elif isinstance(root, For):
            return True
        elif isinstance(root, If):
            return True
        elif isinstance(root, FunctionDef):
            return True
        elif isinstance(root, ClassDef):
            return True
        elif isinstance(root, comprehension):
            return True
        elif isinstance(root, Return):
            return True
        else:
            return False

    def getNumNodes(self, tree):
        # Method to calculate and return the total number of nodes in an AST
        return len(list(ast.walk(tree)))

    def getSigSubTrees(self, tree):
        # Method to extract significant subtrees from an AST
        # Returns a list of significant subtrees
        return [node for node in ast.walk(tree) if self.isSignificant(node)]

    def applyWeightsToTree(self, weight, subTree):
        # Method to apply weights to a subtree based on its type
        # Returns the weighted value
        newWeight = weight

        if isinstance(subTree, While):
            newWeight *= 1
        elif isinstance(subTree, Import):
            newWeight *= 0.3
        elif isinstance(subTree, FunctionDef):
            newWeight *= 1.2
        elif isinstance(subTree, If):
            newWeight *= 0.5
        elif isinstance(subTree, ClassDef):
            newWeight *= 1
        elif isinstance(subTree, For):
            newWeight *= 1
        elif isinstance(subTree, comprehension):
            newWeight *= 1
        elif isinstance(subTree, Return):
            newWeight *= 1
        elif isinstance(subTree, Module):
            newWeight *= 1
        return newWeight

    def applyWeightsToSubtreesMultiple(self, weight, ast_1, ast_2):
        # Method to apply weights to multiple subtrees and return their average
        if weight == 0:
            return 0
        else:
            return (
                self.applyWeightsToTree(weight, ast_1)
                + self.applyWeightsToTree(weight, ast_2)
            ) / 2

    def compareSubTrees(self, reorderDepth):
        # Method to compare significant subtrees between two ASTs and return their similarity
        subTree1 = self.getSigSubTrees(self.tree1)
        subTree2 = self.getSigSubTrees(self.tree2)

        similarity, bestMatches = self.compareSigSubTrees(
            subTree1, subTree2, reorderDepth
        )
        return similarity, bestMatches

    def compareSigSubTrees(self, sigSubTrees1, sigSubTrees2, reorderDepth):
        # Method to compare significant subtrees between two lists of subtrees and return their similarity
        comparisonMatrix = []
        costMatrix = []
        bestMatchValue = 0
        bestMatchWeight = 0
        childrenA = sigSubTrees1.copy()
        childrenB = sigSubTrees2.copy()

        # Check if the number of significant subtrees in both lists is less than or equal to 1
        if len(childrenA) <= 1 or len(childrenB) <= 1:
            for childA in childrenA:
                for childB in childrenB:
                    bestMatchValue += self.compareASTs(childA, childB, reorderDepth)
        else:
            for childA in childrenA:
                row = []
                costRow = []
                for childB in childrenB:
                    similarity = self.compareASTs(childA, childB, reorderDepth)
                    row.append(similarity)
                    costRow.append(10000000 - similarity)

                comparisonMatrix.append(row)
                costMatrix.append(costRow)

        print(f'cost matrix compare {costMatrix}')
        # Use the Munkres algorithm to compute the best matching pairs
        m = Munkres()
        indices = m.compute(costMatrix)
        #print(f'indices compare {indices}')

        for row, col in indices:
            bestMatchWeight += self.applyWeightsToSubtreesMultiple(
                comparisonMatrix[row][col], sigSubTrees1[row], sigSubTrees2[col]
            )

        # Calculate the total weight for significant subtrees in both trees
        totalWeight = 0
        for subTree in sigSubTrees1:
            numNodes = self.getNumNodes(subTree)
            subTreeWeight = self.applyWeightsToTree(numNodes, subTree)
            totalWeight += subTreeWeight
        for subTree in sigSubTrees2:
            numNodes = self.getNumNodes(subTree)
            subTreeWeight = self.applyWeightsToTree(numNodes, subTree)
            totalWeight += subTreeWeight

        allSubtreesWeight = totalWeight

        # Calculate the similarity between the two lists of significant subtrees
        similarity = 2 * bestMatchWeight / allSubtreesWeight
        return round(similarity, 2), bestMatchValue

    def compareASTs(self, AST_a, AST_b, reorderDepth):
        # Method to compare two AST nodes and return their similarity
        childrenA = list(ast.iter_child_nodes(AST_a))
        childrenB = list(ast.iter_child_nodes(AST_b))

        if type(AST_a) != type(AST_b):
            return 0
        elif len(childrenA) != len(childrenB):
            return 0

        if (
            type(AST_a) == type(AST_b)
            and len(list(childrenA)) == 0
            and len(list(childrenB)) == 0
        ):
            return 1

        if reorderDepth == 0:
            matchIndex = 0
            for pair in zip(childrenA, childrenB):
                nodeA, nodeB = pair
                matchIndex += self.compareASTs(nodeA, nodeB, reorderDepth)
            return matchIndex + 1

        elif reorderDepth > 0:
            matchIndex = self.reorderChildren(AST_a, AST_b, reorderDepth - 1)
            return matchIndex + 1

        return 0

    def reorderChildren(self, AST_a, AST_b, reorderDepth):
        # Method to reorder children nodes of ASTs and return their similarity
        comparisonMatrix = []
        bestMatchVal = 0
        childrenA = list(ast.iter_child_nodes(AST_a))
        childrenB = list(ast.iter_child_nodes(AST_b))
        costMatrix = [
            [0] * len(childrenB) for _ in range(len(childrenA))
        ]  # Initialize costMatrix

        if len(childrenA) <= 1 or len(childrenB) <= 1:
            for childA in childrenA:
                for childB in childrenB:
                    bestMatchVal += self.compareASTs(childA, childB, reorderDepth)
        else:
            for childA in childrenA:
                row = []
                for childB in childrenB:
                    similarity = self.compareASTs(childA, childB, reorderDepth)
                    row.append(similarity)

                comparisonMatrix.append(row)

            #print(f'cost matrix reorder {costMatrix}')
            m = Munkres()
            indices = m.compute(costMatrix)
            #print(f'indices reorder {indices}')

            for row, col in indices:
                bestMatchVal += comparisonMatrix[row][col]

        return bestMatchVal
    


script1 = 'titanic_k.py'
script2 = 'titanic_k.py'

sol = SignificantSubTreesComp(script1, script2)
res = sol.compareSubTrees(reorderDepth=10000)
print(res)