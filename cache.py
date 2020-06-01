""" 
    CSE112: Computer Organisation
    End Semester Assignment: Cache

    Made By: Ananya Lohani
    Roll Number: 2019018
    Section: A
    Group: 9

    Documentation for the code is given in README.md file.
    Further documentation for the functions are in the
    docstrings of the functions and inline comments.
    For any further doubts, please email me: ananya19018@iiitd.ac.in
"""

import math         #for using math.log()
import random       #for using random.sample()

def generateMainMemory(bits, blockSize):

    """ A function that divides the locations in main memory into blocks
        using totalSize(S) and blockSize(B) as provided by the user and
        generates addresses of bits specified in the program.
    """
    size = 2**bits
    noOfBlocks = int(size/blockSize)
    wordNumber = 0
    blocks = [["" for i in range(blockSize)] for j in range(noOfBlocks)]
    for i in range(noOfBlocks):
        for j in range(blockSize):
            binNum = convertToBinary(wordNumber)
            binNum = completeBits(binNum, bits)
            blocks[i][j] = binNum
            wordNumber = wordNumber + 1
    return blocks

# Following are some helper functions to make conversions easier.
def convertToBinary(num):

    """ Takes an integer as argument and returns a string in binary. """

    binStr = bin(num)
    binStr = binStr.replace("0b", "")
    return binStr

def completeBits(binStr, bits):

    """ Completes the given binary string to generate an adddress according
        to the bits specified by the program.
        eg. a 16-bit system will generate an address of 16 bits and so on.
    """

    while(len(binStr) != bits):
        binStr = "0" + binStr
    return binStr

def printArray(arr, arrType):

    """ Pretty prints the arrays according to its type. """

    for i in range(len(arr)):
        print(arrType, i, ":", end=" ")
        for j in range(len(arr[0])):
            print(arr[i][j], end=" ")
        print()
    print()

def printCache(cache, cacheLines, blocks, blockSize, blockData):

    """ Pretty prints the cache. """

    for i in range(cacheLines):
        flag = 0
        blockNo = int(cache[i][0][6:])
        print("Cache Line " + str(i) + ":")
        print("Block "+ str(blockNo))
        for j in range(blockSize):
            blockAdd = blocks[blockNo][j]
            data = blockData[blockNo][j]
            if(data != None):
                flag = 1
                print("Address: "+ str(blockAdd) + " Data: " + str(data))
        if(flag == 0): print("Block empty")
        print()

def returnIndexArray(address, bits, blockSize, cacheLines):

    """ Returns the Index part of the address as an integer. """

    blockOffset = int(math.log(blockSize, 2))
    index = int(math.log(cacheLines, 2))
    startIndex = bits - blockOffset - index
    endIndex = bits - blockOffset
    return int(address[startIndex:endIndex], 2)

def returnTagArray(address, bits, blockSize, cacheLines):

    """ Returns the Tag part of the address as integer. """

    startIndex = 0
    blockOffset = int(math.log(blockSize, 2))
    if(cacheLines != 0): index = int(math.log(cacheLines, 2))
    else: index = 0
    endIndex = bits - blockOffset - index
    return int(address[startIndex:endIndex], 2)

# Following functions carry out the required operations of Direct Mapping. 
def directMapping(blocks, cacheLines, blockSize, totalSize, bits):

    """ Returns a Cache structure which directly maps the blocks to the cache lines.
        cacheStruct is an array to keep track of which blocks *can* occupy the respective
        cache line. 
        cache is an array that keeps track of which block is currently occupying the 
        respective cache line.
    """ 

    noOfBlocks = int(2**bits/blockSize)
    cacheStruct = [[] for i in range(cacheLines)]
    ind = 0
    for i in range(noOfBlocks):
        for j in range(blockSize):
            ind = returnIndexArray(blocks[i][j], bits, blockSize, cacheLines)
        cacheStruct[ind].append("Block "+str(i))
    cache = [["Block " + str(i)] for i in range(cacheLines)]
    return (cache, cacheStruct)

def directMapRead(address, blocks, blockData, cache, cacheStruct, blockSize, cacheLines, bits):

    """ Reads from a directly mapped cache. If memory address not found in the cache, it broadcasts
        "Read Miss" and reads the block from the main memory and loads it into the appropriate cache, 
        following a random replacement scheme.
    """

    addInd = returnIndexArray(address, bits, blockSize, cacheLines)
    blockNo = int(cache[addInd][0][6:])
    addTag = returnTagArray(address, bits, blockSize, cacheLines)
    for i in range(blockSize):
        blockTag = returnTagArray(blocks[blockNo][i], bits, blockSize, cacheLines)
        if(addTag == blockTag and address == blocks[blockNo][i]):
            print("Read hit!")
            return blockData[blockNo][i]

    print("Read miss!")
    for i in range(len(cacheStruct[addInd])):
        newBlock = int(cacheStruct[addInd][i][6:])
        if(newBlock == blockNo): continue
        for j in range(blockSize):
            blockTag = returnTagArray(blocks[newBlock][j], bits, blockSize, cacheLines)
            if(addTag == blockTag and address == blocks[newBlock][i]):
                cache[addInd][0] = "Block " + str(newBlock)
                print("Block", str(newBlock), "loaded into Cache Line", str(addInd), ", replacing Block", str(blockNo))
                return blockData[newBlock][j]

def directMapWrite(address, data, blocks, blockData, cache, cacheStruct, blockSize, cacheLines, bits):

    """ Writes to a directly mapped cache. If memory address not found in the cache, it broadcasts
        "Write Miss" and reads the block from the main memory and loads it into the appropriate cache, 
        following a random replacement scheme. Then it writes to the respective memory address in the 
        block.
    """

    addInd = returnIndexArray(address, bits, blockSize, cacheLines)
    blockNo = int(cache[addInd][0][6:])
    addTag = returnTagArray(address, bits, blockSize, cacheLines)
    for i in range(blockSize):
        blockTag = returnTagArray(blocks[blockNo][i], bits, blockSize, cacheLines)
        if(addTag == blockTag and address == blocks[blockNo][i]):
            print("Write hit!")
            blockData[blockNo][i] = data
            print("Data", str(data), "written to address", str(address), "in Block", str(blockNo))
            return

    print("Write miss!")
    for i in range(len(cacheStruct[addInd])):
        newBlock = int(cacheStruct[addInd][i][6:])
        if(newBlock == blockNo): continue
        for j in range(blockSize):
            blockTag = returnTagArray(blocks[newBlock][j], bits, blockSize, cacheLines)
            if(addTag == blockTag and address == blocks[newBlock][j]):
                cache[addInd][0] = "Block " + str(newBlock)
                print("Block", str(newBlock), "loaded into Cache Line", str(addInd), ", replacing Block", str(blockNo))
                blockData[newBlock][j] = data
                print("Data", str(data), "written to address", str(address), "in Block", str(newBlock))
                return

# Following functions carry out the required operations of Fully Associative Mapping. 
def fullyAssociativeMapping(cacheLines, blockSize, bits): 

    """ Returns a cache with each cache line containing a random block from main memory. """

    noOfBlocks = int(2**bits/blockSize)
    l = random.sample(range(noOfBlocks), cacheLines)

    cache = [[""] for i in range(cacheLines)]
    for i in range(cacheLines):
        cache[i][0] = "Block " + str(l[i])
    return cache

def FA_Read(address, blocks, blockData, cache, cacheLines, blockSize, totalSize, bits):

    """ Reads from a fully associative cache. If memory address not found in cache, it broadcasts 
        "Read Miss" and reads the block from main memory, and loads it into the cache, following
        a random replacement scheme.
    """

    addTag = returnTagArray(address, bits, blockSize, 0)
    for i in range(cacheLines):
        blockNo = int(cache[i][0][6:])
        for j in range(blockSize):
            blockTag = returnTagArray(blocks[blockNo][j], bits, blockSize, 0)
            if(blockTag == addTag and address == blocks[blockNo][j]):
                print("Read Hit!")
                return blockData[blockNo][j]

    print("Read Miss!")
    noOfBlocks = int(2**bits/blockSize)
    l = int(random.sample(range(cacheLines),1)[0])
    for i in range(noOfBlocks):
        for j in range(blockSize):
            if(blocks[i][j] == address):
                oldBlock = cache[l][0][6:]
                cache[l][0] = "Block " + str(i)
                print("Block", str(i), "loaded into Cache Line", str(l), ", replacing Block", str(oldBlock))
                return blockData[i][j]

def FA_Write(address, data, blocks, blockData, cache, cacheLines,blockSize, totalSize, bits):

    """ Writes to a fully associative cache. If memory address not found in cache, it broadcasts 
        "Write Miss" and reads the block from main memory, and loads it into the cache, following
        a random replacement scheme. Then it writes to the respective memory address in the block.
    """

    addTag = returnTagArray(address, bits, blockSize, 0)
    for i in range(cacheLines):
        blockNo = int(cache[i][0][6:])
        for j in range(blockSize):
            blockTag = returnTagArray(blocks[blockNo][j], bits, blockSize, 0)
            if(blockTag == addTag and address == blocks[blockNo][j]):
                print("Write Hit!")
                blockData[blockNo][j] = data
                print("Data", str(data), "written to address", str(address), "in Block", str(blockNo))
                return

    print("Write Miss!")
    noOfBlocks = int(2**bits/blockSize)
    l = int(random.sample(range(cacheLines),1)[0])
    for i in range(noOfBlocks):
        for j in range(blockSize):
            if(blocks[i][j] == address):
                oldBlock = cache[l][0][6:]
                cache[l][0] = "Block " + str(i)
                print("Block", str(i), "loaded into Cache Line", str(l), ", replacing Block", str(oldBlock))
                blockData[i][j] = data
                print("Data", str(data), "written to address", str(address), "in Block", str(i))
                return

# Following functions carry out the required operations of N-way Set Associative Mapping.
def setAssociativeMapping(blocks, cacheLines, blockSize, totalSize, ways, bits):

    """ Returns an N-way set associative cache, with eachs set containing N cache lines.
        blockSet is an array that keeps track of which blocks *can* occupy the respective set.
        lineSet is an array that keeps track of which cache lines are currently occupying the 
        respective set.
        cache is an array that keeps track of which block is currently occupying the respective 
        cache line.
    """

    noOfBlocks = int(2**bits/blockSize)
    noOfSets = int(cacheLines/ways)
    setStructBlocks = [[] for i in range(noOfSets)]
    for i in range(noOfBlocks):
        for j in range(blockSize):
            ind = returnIndexArray(blocks[i][j], bits, blockSize, noOfSets)
        setStructBlocks[ind].append("Block "+str(i))
    setStructLines = [[] for i in range(noOfSets)]
    line = 0
    for i in range(noOfSets):
        for j in range(ways):
            setStructLines[i].append("Cache "+str(line))
            line = line + 1
    cache = [[""] for i in range(cacheLines)]
    for i in range(noOfSets):
        l = random.sample(setStructBlocks[i],ways)
        for j in range(ways):
            ind = int(setStructLines[i][j][6:])
            cache[ind][0] = l[j]
    return (cache, setStructLines, setStructBlocks)

def SA_Read(address, blocks, blockData, cache, blockSet, lineSet, blockSize, cacheLines, ways, bits):

    """ Reads from an N-way set associative cache. If memory address not found in cache, it broadcasts
        "Read Miss" and reads the block containing the address from main memory. It loads the block into 
        a randomly selected cache of the appropriate set, thus following the random replacement scheme.
    """

    noOfSets = int(cacheLines/ways)
    addInd = returnIndexArray(address, bits, blockSize, noOfSets)
    addTag = returnTagArray(address, bits, blockSize, noOfSets)
    setNo = lineSet[addInd]
    blockNo = 0
    for i in range(ways):
        cacheNo = int(setNo[i][6:])
        blockNo = int(cache[cacheNo][0][6:])
        for j in range(blockSize):
            blockTag = returnTagArray(blocks[blockNo][j], bits, blockSize, noOfSets)
            if(addTag == blockTag and address == blocks[blockNo][j]):
                print("Read Hit!")
                return blockData[blockNo][j]

    print("Read Miss!")
    setNo = blockSet[addInd]
    for i in range(len(blockSet[0])):
        newBlock = int(setNo[i][6:])
        if(newBlock == blockNo): continue
        for j in range(blockSize):
            blockTag = returnTagArray(blocks[newBlock][j], bits, blockSize, noOfSets)
            if(addTag == blockTag and address == blocks[newBlock][j]):
                x = random.sample(lineSet[addInd],1)
                cacheNo = int(str(x[0])[6:])
                cache[cacheNo][0] = "Block " + str(newBlock)
                print("Block", str(newBlock), "loaded into Cache Line", str(cacheNo), "from Set", str(addInd), ", replacing Block", str(blockNo))
                return blockData[newBlock][j]

def SA_Write(address, data, blocks, blockData, cache, blockSet, lineSet, blockSize, cacheLines, ways, bits):

    """ Writes to an N-way set associative cache. If memory address not found in cache, it broadcasts
        "Write Miss" and reads the block containing the address from main memory. It loads the block into 
        a randomly selected cache of the appropriate set, thus following the random replacement scheme.
        Then it writes to the respective memory address in the block.
    """

    noOfSets = int(cacheLines/ways)
    addInd = returnIndexArray(address, bits, blockSize, noOfSets)
    addTag = returnTagArray(address, bits, blockSize, noOfSets)
    setNo = lineSet[addInd]
    blockNo = 0
    for i in range(ways):
        cacheNo = int(setNo[i][6:])
        blockNo = int(cache[cacheNo][0][6:])
        for j in range(blockSize):
            blockTag = returnTagArray(blocks[blockNo][j], bits, blockSize, noOfSets)
            if(addTag == blockTag and address == blocks[blockNo][j]):
                print("Write Hit!")
                blockData[blockNo][j] = data
                print("Data", str(data), "written to address", str(address), "in Block", str(blockNo))
                return

    print("Write Miss!")
    setNo = blockSet[addInd]
    for i in range(len(blockSet[0])):
        newBlock = int(setNo[i][6:])
        if(newBlock == blockNo): continue
        for j in range(blockSize):
            blockTag = returnTagArray(blocks[newBlock][j], bits, blockSize, noOfSets)
            if(addTag == blockTag and address == blocks[newBlock][j]):
                x = random.sample(lineSet[addInd],1)
                cacheNo = int(str(x[0])[6:])
                cache[cacheNo][0] = "Block " + str(newBlock)
                print("Block", str(newBlock), "loaded into Cache Line", str(cacheNo), "from Set", str(addInd), ", replacing Block", str(blockNo))
                blockData[newBlock][j] = data
                print("Data", str(data), "written to address", str(address), "in Block", str(newBlock))
                return


def begin():

    """ A function that initialises the program. """

    S = int(input("Enter total size of cache(S): "))
    cL = int(input("Enter number of lines in cache(CL): "))
    B = int(input("Enter the size of a block(B): "))
    print()

    #Specifies the word size, eg. 32-bit, 16-bit, etc.
    bits = 16  

    if(math.log(S, 2) > bits):
        print("Invalid size of cache")
    
    print("Types of mapping of cache: ")
    print("1. Direct Mapping")
    print("2. Fully Associative Mapping")
    print("3. N-way Set Associative Mapping")
    print()

    blocks = []     # Array that stores the addresses of the main memory in blocks
    cache = []      # Array that stores the cache structure
    cacheStruct = []        

    noOfBlocks = int(2**bits/B)
    blockData = [[None for i in range(B)] for j in range(noOfBlocks)]

    blocks = generateMainMemory(bits, B)

    choice = int(input("Choose type of mapping(1, 2 or 3): "))
    print()
    #printArray(blocks, "Block")
    if(choice == 1):
        (cache, cacheStruct) = directMapping(blocks, cL, B, S, bits)
        c = 'Y'
        while(c == 'Y' or c == 'y'):
            print("Operations: ")
            print("1. Read")
            print("2. Write")
            print("3. View Cache")
            print()

            ch = int(input("Choose operation(1, 2 or 3): "))
            print()

            if(ch == 1):
                add = input("Enter address from which data has to be read(in binary): ")
                if(int(add, 2) != 0 and math.log(int(add, 2)) > bits):
                    print("Invalid Address")
                    print()
                else:
                    add = completeBits(add, bits)
                    data = directMapRead(add, blocks, blockData, cache, cacheStruct, B, cL, bits)
                    print("Data at address", add, "is", str(data))
                    print()
            elif(ch == 2):
                add = input("Enter address to which data has to be written(in binary): ")
                if(int(add, 2) != 0 and math.log(int(add, 2)) > bits):
                    print("Invalid Address")
                    print()
                else:
                    add = completeBits(add, bits)
                    data = input("Enter data to be written: ")
                    print()
                    directMapWrite(add, data, blocks, blockData, cache, cacheStruct, B, cL, bits)
            elif(ch == 3):
                printCache(cache, cL, blocks, B, blockData)
            else:
                print("Invalid Choice!")
                print()
            c = input("Do you want to continue(Y/N)?")
            print()

    elif(choice == 2):
        cache = fullyAssociativeMapping(cL, B, bits)
        c = 'Y'
        while(c == 'Y' or c == 'y'):
            print("Operations: ")
            print("1. Read")
            print("2. Write")
            print("3. View Cache")
            print()

            ch = int(input("Choose operation(1, 2 or 3): "))
            print()

            if(ch == 1):
                add = input("Enter address from which data has to be read(in binary): ")
                print()
                if(int(add, 2) != 0 and math.log(int(add, 2)) > bits):
                    print("Invalid Address")
                    print()
                else:
                    add = completeBits(add, bits)
                    data = FA_Read(add, blocks, blockData, cache, cL, B, S, bits)
                    print("Data at address", add, "is", str(data))
                    print()
            elif(ch == 2):
                add = input("Enter address to which data has to be written(in binary): ")
                print()
                if(int(add, 2) != 0 and math.log(int(add, 2)) > bits):
                    print("Invalid Address")
                    print()
                else:
                    add = completeBits(add, bits)
                    data = input("Enter data to be written: ")
                    print()
                    FA_Write(add, data, blocks, blockData, cache, cL, B, S, bits)
            elif(ch == 3):
                printCache(cache, cL, blocks, B, blockData)
            else:
                print("Invalid Choice!")
                print()
            c = input("Do you want to continue(Y/N)?")
            print()

    elif(choice == 3):
        N = int(input("Enter number of ways(N) for N-way Set Associative Mapping: "))
        print()
        (cache, lineSet, blockSet) = setAssociativeMapping(blocks, cL, B, S, N, bits)
        c = 'Y'
        while(c == 'Y' or c == 'y'):
            print("Operations: ")
            print("1. Read")
            print("2. Write")
            print("3. View Cache")
            print("4. View Sets")
            print()

            ch = int(input("Choose operation(1, 2, 3 or 4): "))
            print()

            if(ch == 1):
                add = input("Enter address from which data has to be read(in binary): ")
                print()
                if(int(add, 2) != 0 and math.log(int(add, 2)) > bits):
                    print("Invalid Address")
                    print()
                else:
                    add = completeBits(add, bits)
                    data = SA_Read(add, blocks, blockData, cache, blockSet, lineSet, B, cL, N, bits)
                    print("Data at address", add, "is", str(data))
                    print()
            elif(ch == 2):
                add = input("Enter address to which data has to be written(in binary): ")
                print()
                if(int(add, 2) != 0 and math.log(int(add, 2)) > bits):
                    print("Invalid Address")
                    print()
                else:
                    add = completeBits(add, bits)
                    data = input("Enter data to be written: ")
                    print()
                    SA_Write(add, data, blocks, blockData, cache, blockSet, lineSet, B, cL, N, bits)
            elif(ch == 3):
                printCache(cache, cL, blocks, B, blockData)
            elif(ch == 4):
                printArray(lineSet, "Set")
            else:
                print("Invalid Choice!")
                print()
            c = input("Do you want to continue(Y/N)?")
            print()
    
    else:
        print("Invalid Choice, Exiting...")

# To start program execution
begin()