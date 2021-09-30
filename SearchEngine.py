'''
This program implements AVL trees, priority queues and heaps in order to make
a simple search engine.
includes the AVLTree, WebPageIndex, WebpagePriorityQueue and ProcessQuery class
Name: Haadia Mufti
Student ID: 20079759
'''
import os
# the node class is implemented to suport the AVL tree class
class Node:

    #every node of a tree should have a pointer for the left child, right child
    # height, key and value 
    def __init__(self, key, value):
        self.key= key
        self.value = value
        self.leftChild = None
        self.rightChild = None
        self.height= 1

    # return a list of nodes visited until the target value is found
    def searchPath(self, key):

        # if the key is found then the list is returned 
        if self.key == key:
            return []

        # if the key value is less than the key in the tree then we tranverse
        # through the left tree
        elif self.key > key:
            if self.leftChild != None:
                return [self.leftChild.key] + self.leftChild.searchPath(key)
            else:
                print("not in tree path")
                return []
            
        # if the key value is more than the key in the tree then we tranverse
        # through the right tree
        elif self.key < key :
            if self.rightChild != None:
                return [self.rightChild.key]+self.rightChild.searchPath(key)
            else:
                print("not in the tree path")
                return []

    # the function return the value for the key input
    # if value cannot be found, none is returned
    def get(self, key):

        # if the value is found then the value is returned
        if self.key == key:
            return self.value

        # tranverse through the left tree untill there are no more children 
        elif self.key > key:
            if self.leftChild != None:
                return self.leftChild.get(key)
            else:
                return None

        # tranverse through the right tree untill there are no more children 
        elif self.key < key:
            if self.rightChild != None:
                return self.rightChild.get(key)
            else:
                return None
            
 # the AVLTreeMap class perform the functionality for AVL trees 
class AVLTreeMap:

    # every AVL tree will have a pointer for the root
    def __init__(self, key, value):

        self.root = Node(key, value)

    # search add the nodes visited to a lsit untill the target key is found
    def searchPath(self, key):

        # tranverse through the left subtres and add to the lsit
        # untill no chidren 
        if self.root != None :
            
            searchList = [ self.root.key] + self.root.searchPath(key)
            keysVisted = ''
            for element in searchList:
                keysVisted += str(element) + ","
            return (print (keysVisted[:-1]))
        else:
            print("not in tree path")
            return []

    # get function gets the valeu for the key we input
    def get(self, key):

        # if the root is empty then we can't ffind the value
        if self.root != None:
            return self.root.get(key)
        else:
            return None

    # put function insert a value in the tree, checks if the tree is still balanced
    # after the insertion 
    def put(self, key, value, root):

        # add the key and value to the respective tree only when the node is empty
        if root== None:
            return Node(key,value)

        # if the key is less than the key in the tree, go through the left tree
        elif key < root.key:
            root.leftChild=self.put(key,value,root.leftChild)

        # if the key is less than the key in the tree, go through the left tree
        elif key > root.key:
            root.rightChild= self.put(key, value,root.rightChild)

        # if the key is the same then update the value of the key
        elif key == root.key :
            root.value = value

        
        # update the height of the tree after adding the node
        root.height = 1 + max(self.getHeight(root.leftChild), self.getHeight(root.rightChild))

        #get the balance of the tree to see the tree has to be rebalanced 
        currectBalance = self.getBalance(root)

        # Left Left Case
        # if the left side of the tree has more subtrees then we perform a
        # right rotation to balance the tree
        if currectBalance > 1 and key < root.leftChild.key:
            return self.rightRotate(root)

        # Right Right Case
        # if the right side of the tree has more subtrees then we perform a
        # left rotation to balance the tree
        if currectBalance < -1 and key > root.rightChild.key:
            return self.leftRotate(root)

        # Left Right Case
        # if the left side and right child of the tree has more subtrees then
        # we perform a left and right rotation to rebalance the tree
        if currectBalance > 1 and key > root.leftChild.key:
            root.leftChild = self.leftRotate(root.leftChild)
            return self.rightRotate(root)

        # Right Left Case
        # if the right side and left child of the tree has more subtrees then
        # we perform a right an left rotation to rebalance the tree
        if currectBalance < -1 and key < root.rightChild.key:
            root.rightChild = self.rightRotate(root.rightChild)
            return self.leftRotate(root)

        return root

    # leftRotate rotates the tree when the right tree has more nodes
    def leftRotate(self, z):

        # placeholders so we don't lose the values for the rotation
        A = z.rightChild
        beta = A.leftChild

        # the tree/children are rotated 
        A.leftChild = z
        z.rightChild = beta

        # the heights of the trees are recalculated after the rotation
        z.height = 1+ max(self.getHeight(z.leftChild), self.getHeight(z.rightChild))
        A.height = 1+ max(self.getHeight(A.leftChild), self.getHeight(A.rightChild))

        return A

    # rightRoates rotates the tree when the left tree has more nodes
    def rightRotate(self, z):

        # placeholders so that the values of the nodes aren't lost
        B = z.leftChild
        alpha = B.rightChild

        # the tree/children are rotated
        B.rightChild = z
        z.leftChild = alpha

        # the height of the tree's are recalculated after the rotation
        z.height = 1+ max(self.getHeight(z.leftChild), self.getHeight(z.rightChild))
        B.height = 1+ max(self.getHeight(B.leftChild), self.getHeight(B.rightChild))

        return B


    # return the neight of the particular tree/subtree
    def getHeight(self,node):

        if node != None:
            return node.height
        else:
            return 0

    # returns the balance of the particular tree/subtree
    def getBalance(self, root):

        if self == None: 
            return 0

        return (self.getHeight(root.leftChild) - self.getHeight(root.rightChild))
'''       
index representaton of the webpage
converts the webpage into an AVLMap
key refers to the each word appearing on the webpage and the value is a list
of positions of this word in the file
'''
class WebPageIndex:

    # class constructor take a filename as an input
    def __init__(self, filename):

        self.file = filename

    # makes the contents in the filename into a list after removing all
    # punctuations 
    def getList(self, filename):

        # reads content of the file 
        fileLocation = "testdata/"+filename
        textFile = open(fileLocation,'r+', encoding="utf-8")
        doc = textFile.read().split(' ')
        newList = []
        punctuation = "!@#$%^&*(){}[]_+<>?:.,;"
        for element in doc:
            for letter in element:
                if letter in punctuation:
                    element = element.replace(letter, "")
            element= element.lower()
            newList.append(element) #adds the stripped element to the list
        return newList

    # function takes all the element of the list and converts it into an AVL tree
    # the key of the AVL tree is the word in the file and the value is a list of
    # the positions the particular index appears
    def toAVLTree( self):
        docList = self.getList(self.file)
        treeDictionary = {}
        positon = 0
        # add the position as a list in the value of the dictionary
        for word in docList:
            if word in treeDictionary:
                 treeDictionary[word].append(positon)
            else:
                treeDictionary[word]= [positon]
                
            positon +=1

        # all the values in the dictionary are then used to make an AVL tree
        tree = None
        for key in treeDictionary:
            if tree == None:
                tree= AVLTreeMap(key, treeDictionary[key])
            else:
                tree.root = tree.put(key, treeDictionary[key], tree.root)

        return tree
             
    # this function returns the number of times a word appears in a the file
    # this is done by just taking the length of the list in the value postion
    # as the list contains the indices in which the word appears
    def getCount(self, word):
        tree = self.toAVLTree()
        treeValue = tree.get(word)
        if treeValue == None:
            return 0
        return len(treeValue)


# a priority queue is implemented using a maxheap as maxheap can give the max value
# in O(1) time.
class WebpagePriorityQueue:

    # class constructor take in a query and a web file 
    def __init__(self, query, webPageIndex):
        self.query = query
        self.webPageIndex = webPageIndex
        self.heap = [[0,0]]
        self.maxHeap = self.createHeap()

    # this function calculates the priority of the query in the file
    # the priority is calculated based on the nummber of times the word is repeated
    def calculatePriority(self, webPageIndex):
        # remove all punctuations from the query 
        queryList = []
        punctuation = "!@#$%^&*()_+<>?:.,;"
        for element in self.query:
            for letter in element:
                if letter in punctuation:
                    element = element.replace(letter, "")
            element= element.lower()
            queryList.append(element)
        queryList = ''.join(queryList)
        queryList= queryList.split()

        # priority sum has the total of the number of times the word is repeated in
        # the file
        prioritySum = 0
        for element in queryList:
            prioritySum += webPageIndex.getCount(element)

        return prioritySum

    # returns the highest priority value without removing it
    def peek(self):
        return self.heap[1][1]

    # returns the highest priority value and also removes it from the list
    def poll(self):
        highPriority = self.heap[1][1]
        del(self.heap[1])
        return highPriority

    # reheap takes a new query and reheaps the heap as the priority of a query
    # on each web page is different 
    def reheap(self, newQuery):

        if newQuery == self.query:
            return 
        self.heap = [[0,0]]
        self.query = newQuery
        self.maxHeap = self.createHeap()
        return self.maxHeap

    # creates an array based heap
    def createHeap(self):

        for word in self.webPageIndex:

            priority = self.calculatePriority(word)
            self.heap.append([priority, word])
            self.reOrderHeap(len(self.heap)-1)

        return self.heap

    # re orders the maxheap when a new value is added
    def reOrderHeap(self, index):

        parentIndex = index //2

        if index <= 1:
            return
        # swaps values of the parent and child if the parent is lesser than the child
        elif self.heap[index][0] > self.heap[parentIndex][0]:
            self.heap[index], self.heap[parentIndex] = self.heap[parentIndex], self.heap[index]
            self.reOrderHeap(parentIndex)

# this class implements a simple web search engine. The first part is to build a list of
# WebPageIndex instances from a folder containing a set of web pages (txt files).
# The second part is to enter a loop to process a series of user queries (also from a txt file)
class ProcessQueries:

    # contructure takes no input. Just calls function
    def __init__(self):
        self.processQueries()

    # this function opens each txxt file in the testdata folder and converts each file into
    # a WebPageIndex instance and adds them to a list. Thiis creates a list of AVL trees
    def webIndexList(self):
        webIndicesList = []
        textFile = os.listdir('testdata')
        for file in textFile:
            if file != ".DS_Store":
                webIndexTree = WebPageIndex(file) 
                webIndicesList.append(webIndexTree)
                
        return webIndicesList

    # this function puts all the queries in the query file in a list
    def queryList(self):
        # puts all the queries in a list
        queryFile = open("queries.txt", "r")
        queryList = queryFile.read().split('\n')
        return queryList

    # this function takes each query and searches the query in each of the webpage index instances
    # it then gives a list of files in which the word appears in order of priority
    def processQueries(self):
        queryList = self.queryList()
        webIndicesList = self.webIndexList()
        lenQueries = len(queryList)

        # every query is taken ffrom the list to search related files
        for query in queryList:
            print("Searching for files with", query,"in it..")
            print('Search Results:')
            print()
            queryPriorityQueue = WebpagePriorityQueue(query, webIndicesList)
            maxHeap = queryPriorityQueue.maxHeap

            # if there are no queries in the list and the max priority is not 0 then print
            # the the file names
            if lenQueries == 0:
                while len(maxHeap) > 1:
                    if maxHeap[1][0] !=0:
                        print(queryPriorityQueue.poll().file)
                    else: 
                         queryPriorityQueue.poll()
            else:

                # otherwise print the values of the highest priority untill you have searched
                # for all the queries in the list
                while len(maxHeap) > 1 and lenQueries > 0:

                    if maxHeap[1][0] != 0:
                         print(queryPriorityQueue.poll().file)

                    else:
                        queryPriorityQueue.poll()
                    lenQueries -=1
            print()


ProcessQueries()










         
 



    
