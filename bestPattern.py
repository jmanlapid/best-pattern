import traceback
import sys
from sys import maxint

if len(sys.argv) != 3:
    sys.exit("Command line args must be bestRegex.py <input file> <output file>")

def buildTree (glob_tree, pattern, index):
    if index > len(pattern) - 1:
        return
    token = pattern[index]
    if token not in glob_tree:
        glob_tree[token] = {}
    return buildTree (glob_tree[token], pattern, index + 1)

def matchPattern (glob_tree, path, pattern, index):
    token = path[index]
    if index == len(path) - 1:
        if token in glob_tree and len(glob_tree[token]) == 0:
            tempPattern1 = pattern+token+"\n"
            getBestPattern(tempPattern1)
        if "*" in glob_tree and len(glob_tree["*"]) == 0:
            tempPattern2 = pattern+"*\n"
            getBestPattern(tempPattern2)
    else:
        if "*" in glob_tree:
            matchPattern (glob_tree["*"], path, pattern+"*"+",", index + 1)
        if token in glob_tree:
            matchPattern (glob_tree[token], path, pattern+token+",", index + 1)

def getBestPattern(tempPattern):
    global bestPattern
    global numWildCards
    tempPattern_wc = tempPattern.count("*")
    bestPattern_wc = bestPattern.count("*")
    if not bestPattern:
        bestPattern = tempPattern
        numWildCards = tempPattern_wc
    elif tempPattern_wc < bestPattern_wc:
        bestPattern = tempPattern
        numWildCards = tempPattern_wc
    elif tempPattern_wc == bestPattern_wc:
        bestPattern = disputeTie(tempPattern, bestPattern, len(tempPattern))

def disputeTie(str1, str2, lastIndex):
    str1_index = str1.rindex("*", 0, lastIndex)
    str2_index = str2.rindex("*", 0, lastIndex)
    if str1_index > str2_index:
        return str1
    elif str2_index > str1_index:
        return str2
    else:
        return disputeTie(str1, str2, lastIndex - 1)

try:
    glob_tree = {}
    f_read = open(sys.argv[1], "r")
    f_write = open(sys.argv[2], "w")
    numPatterns = int(f_read.readline())
    for t in range(0, numPatterns):
        pattern = f_read.readline().replace("\n", "").split(",")
        buildTree(glob_tree, pattern, 0)

    numPaths = int(f_read.readline())
    for t in range(0, numPaths):
        bestPattern = ""
        numWildCards = maxint
        path = f_read.readline().replace("\n", "")
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        path = path.split("/")
        matchPattern (glob_tree, path, "", 0)
        if bestPattern:
            f_write.write(bestPattern)
        else:
            f_write.write("NO MATCH\n")
    f_read.close()
    f_write.close()
except IOError:
    sys.exit("Error opening file \"" + sys.argv[1] + "\" for parsing")
except:
    sys.exit(traceback.format_exc())
