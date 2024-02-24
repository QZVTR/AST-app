import numpy as np
from main import HungarianAlgo
import ast
from _ast import *

class SigSubTreeComparison:
    def __init__(self, tree1: AST, tree2: AST):
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
        
    def compareSigSubTrees(self, subTreesA, subTreesB, depth):
        comparisonMatrix = []
        costMatrix = []
        bestMatchValue = 0
        bestMatchWeight = 0
        childrenA = subTreesA[:]
        childrenB = subTreesB[:]

        if len(childrenA) <= 1 or len(childrenB) <= 1:
            for childA in childrenA:
                for childB in childrenB:
                    bestMatchValue += self.compareASTs(childA, childB, depth)
        else:
            for childA in childrenA:
                row = []
                costRow = []
                for childB in childrenB:
                    similarity = self.compareASTs(childA, childB, depth)
                    row.append(similarity)
                    costRow.append(10000000 - similarity)
                
                comparisonMatrix.append(row)
                costMatrix.append(costRow)
            print(f'cost matrix compare {costMatrix}')
            m = HungarianAlgo(costMatrix)
            indices = m.solve()
            

            for row, col in indices:
                bestMatchWeight += self.applyWeightsToSubtreesMultiple(
                    comparisonMatrix[row][col], subTreesA[row], subTreesB[col]
                )

            # Calculate the total weight for significant subtrees in both trees
            totalWeight = 0
            for subTree in subTreesA:
                numNodes = self.getNumNodes(subTree)
                subTreeWeight = self.applyWeightsToTree(numNodes, subTree)
                totalWeight += subTreeWeight
            for subTree in subTreesB:
                numNodes = self.getNumNodes(subTree)
                subTreeWeight = self.applyWeightsToTree(numNodes, subTree)
                totalWeight += subTreeWeight

            allSubtreesWeight = totalWeight

            # Calculate the similarity between the two lists of significant subtrees
            similarity = 2 * bestMatchWeight / allSubtreesWeight
            return round(1-similarity, 2), bestMatchValue
                
            

    def compareASTs(self, ASTa, ASTb, depth):
        childrenA = list(ast.iter_child_nodes(ASTa))
        childrenB = list(ast.iter_child_nodes(ASTb))
        
        if type(ASTa) == type(ASTb) and len(childrenA) == 0 and len(childrenB) == 0:
            return 1
        elif type(ASTa) != type(ASTb) or len(childrenA) != len(childrenB):
            return 0
        
        if depth == 0:
            index = 0
            for pair in zip(childrenA, childrenB):
                nodeA, nodeB = pair
                index += self.compareASTs(nodeA, nodeB, depth)
            return index
        elif depth > 0:
            index = self.reorderCompare(ASTa, ASTb, depth - 1)
            return index

    def reorderCompare(self, AST_a, AST_b, reorderDepth):
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
            m = HungarianAlgo(costMatrix)
            indices = m.solve()
            #print(f'indices reorder {indices}')

            for row, col in indices:
                bestMatchVal += comparisonMatrix[row][col]

        return bestMatchVal

        


script1 = 'titanic_k.py'
script2 = 'titanic_k.py'

sol = SigSubTreeComparison(script1, script2)
res = sol.compareSubTrees(reorderDepth=10000)
print(res)
