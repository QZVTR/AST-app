#from munkres import Munkres

class HungarianAlgo:
    def __init__(self, costMatrix):
        self.costMatrix = costMatrix

    def solve(self):
        costMatrix = self.costMatrix
        nRows = len(costMatrix)
        nCols = len(costMatrix[0])

        # Step 1: Subtract the minimum value of each row from its elements
        for i in range(nRows):
            minVal = min(costMatrix[i])
            for j in range(nCols):
                costMatrix[i][j] -= minVal

        # Step 2: Subtract the minimum value of each column from its elements
        for j in range(nCols):
            minVal = min(costMatrix[i][j] for i in range(nRows))
            for i in range(nRows):
                costMatrix[i][j] -= minVal

        # Step 3: Cover all zeros with minimum number of lines
        rowCovered = [False] * nRows
        colCovered = [False] * nCols
        coveredZeros = []

        while True:
            # Find an uncovered zero
            row, col = self.findUncoveredZeros(costMatrix, rowCovered, colCovered)
            if row is None:
                break
            
            coveredZeros.append((row, col))
            rowCovered[row] = True
            colCovered[col] = True

            # Find a non-covered zero in the same row
            for c in range(nCols):
                if costMatrix[row][c] == 0 and not rowCovered[row]:
                    colCovered[c] = True
                    break

            # Find a zero in the same column as a starred zero
            for r, c in coveredZeros:
                if c == col and r != row:
                    rowCovered[r] = True
                    break

        # Step 4: Get the optimal assignment
        assignments = [(row, col) for row, col in coveredZeros if costMatrix[row][col] == 0]
        return assignments

    def findUncoveredZeros(self, costMatrix, rowCovered, colCovered):
        nRows = len(costMatrix)
        nCols = len(costMatrix[0])
        
        for i in range(nRows):
            for j in range(nCols):
                if costMatrix[i][j] == 0 and not rowCovered[i] and not colCovered[j]:
                    return i, j
        return None, None
    
    
    
"""
# Example usage:
costMatrix = [[10000000, 10000000, 10000000], 
              [9999958, 10000000, 10000000], 
              [10000000, 9999988, 10000000], 
              [10000000, 10000000, 9999978]]

costMatrixMunkres =[[10000000, 10000000, 10000000],
                    [9999958, 10000000, 10000000],
                    [10000000, 9999988, 10000000],
                    [10000000, 10000000, 9999978]]

hungarianSolver = HungarianAlgo(costMatrix)
assignments = hungarianSolver.solve()
print("Assignments:", assignments)
#print("Total Cost:", totalCost)
munkresSovler = Munkres()
comp = munkresSovler.compute(costMatrixMunkres)
print("Assignments:", comp)
"""