import os
import time
from datasketch.minhash import MinHash
import concurrent.futures
import ast

from app.settings import BASE_DIR
from functools import reduce

# file paths
filePath = None

# specyhashes file path
specyhashesFilePath = None

# lsh similarity file path
lshSimilarityFilePath = None

splitValue = 200000
minHashPermmutations = 10

fileNameArray = []


dnaMinHashes = []


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(set(list2))))
    union = len(set(list1).union(set(list2)))
    if(union == 0):
        return 0.0
    else:
        return float(intersection / union)


def minHashing(splitedString):
    shringleLength = 5
    startIndex = 0
    m1 = MinHash(num_perm=minHashPermmutations)

    for x in range(0, int(round(len(splitedString) / shringleLength))):
        m1.update(splitedString[startIndex:(
            startIndex + shringleLength)].encode('utf8'))
        startIndex = startIndex + shringleLength

    return m1.hashvalues


def LSH(filename):

    print("task started " + filename)

    taskStartTime = time.time()

    file1 = open(filePath + filename, "r")
    dnaSet1 = file1.read()
    flag = True
    startPointer = 0
    dnaLength = len(dnaSet1)
    # print(dnaLength)
    # print("dna length ",dnaLength)
    oneSpecyMinHash = []
    while (flag):

        if (startPointer + splitValue <= dnaLength):

            splitedString = dnaSet1[startPointer:startPointer + splitValue]
            minHashValue = minHashing(splitedString)
            oneSpecyMinHash += list(minHashValue)
            startPointer = startPointer + splitValue

        else:

            splitedString = dnaSet1[startPointer::]
            minHashValue = minHashing(splitedString)
            oneSpecyMinHash += list(minHashValue)
            flag = False

    onespecietoprint = []

    onespecietoprint.append([filename, oneSpecyMinHash])
    try:
        f = open(specyhashesFilePath, 'a+')
    except Exception as ex:
        print(ex)
    f.writelines("%s\n" % item for item in onespecietoprint)
    f.close()
    print("time for " + filename + " minhashing", time.time() - taskStartTime)

    return oneSpecyMinHash


def main(process_id, file_dict):
    result_matrix = ""

    totStartTime = time.time()
    fileIndex = 1

    global filePath
    global specyhashesFilePath
    global lshSimilarityFilePath
    global dnaMinHashes
    global fileNameArray

    fileNameArray = []

    filePath = BASE_DIR + "/storage/" + str(process_id) + "/DNA_SEQUNCES/"
    specyhashesFilePath = BASE_DIR + "/storage/" + \
        str(process_id) + '/' + 'specyhashes.txt'
    lshSimilarityFilePath = BASE_DIR + "/storage/" + \
        str(process_id) + '/' + 'LSH_similarity.txt'

    for filename in os.listdir(filePath):
        fileNameArray.append(filename)
        fileIndex += 1

    print(fileNameArray)
    a = []
    dnaMinHashes = []
    for i in fileNameArray:
        a.append(LSH(i))
    for filename, minhashArray in zip(fileNameArray, a):

        dnaMinHashes.append([filename, minhashArray])

    print("total time = ", time.time()-totStartTime)
    fo = open(specyhashesFilePath, 'r')
    f1 = fo.readlines()

    comparingStartTime = time.time()

    for i in range(0, len(f1)):
        for j in range(i, len(f1)):
            f_item_i = ast.literal_eval(f1[i])
            f_item_j = ast.literal_eval(f1[j])
            print("jaccard similarity between " +
                  f_item_i[0] + " and " + f_item_j[0] + " is : ", jaccard_similarity(f_item_i[1], f_item_j[1]))
            f = open(lshSimilarityFilePath, 'a+')

            first_file = file_dict[f_item_i[0][:-4]]
            second_file = file_dict[f_item_j[0][:-4]]

            new_line = "%s\n" % (first_file + "," + second_file + "," + str(
                jaccard_similarity(f_item_i[1], f_item_j[1])))

            result_matrix = result_matrix + new_line
            f.writelines(new_line)
            f.close()

    print("time for comparing = ", time.time()-comparingStartTime)
    a = []
    return result_matrix
