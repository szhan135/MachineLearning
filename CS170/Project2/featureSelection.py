#Siyi Zhan
#SID: 8862053955
#FeatureSelection Algorithm

import copy
import math
import numpy as np


#The nearest neighbor classifier (keep the training instances in memory and
#when a new data point is given for classification, compute its distance to the training points and return
#the class label of the nearest training point)
def nearest_neighbor(arr, pointLeft, numOfInstance, subFeature):
    initialLabel = 0
    minDistance = math.inf

    for i in range(numOfInstance):
        if i != pointLeft:
            distance = 0 #initial the distance, updating in the for loop, compare with the minDistance later
            for j in range(len(subFeature)):
                distance += pow(arr[i][subFeature[j]] - arr[pointLeft][subFeature[j]], 2)
            if distance < minDistance:
                initialLabel = arr[i][0]  # returns class label
                minDistance = distance

    return initialLabel # return output: class label of nearest neighbor

#Helper function to return the accuracy
def cal_accuracy(arr, numOfInstance, subFeature):
    match = 0 
    #count of correct/accuracy
    for i in range(numOfInstance):
        instance_NN_classifier = i  #initialize the classifier
        targetLabel = arr[instance_NN_classifier][0]
        nnLabel = nearest_neighbor(arr, instance_NN_classifier, numOfInstance, subFeature)

        if nnLabel == targetLabel:  
            match += 1

    return (match / numOfInstance) * 100.0  #return the accuracy of %

# Helper Function to Normalize
#scan the file by colomun, and squish it to gather it to be one row
def Normalization(np_array, numOfInstance, numOffeature):
    arr = np.mean(np_array, axis=0)
    mean = np.delete(arr, 0)
    arr = np.std(np_array, axis=0)
    standard = np.delete(arr, 0)
    #get the mean and the standard for the instances

    for i in range(0, numOfInstance):
        for j in range(1, numOffeature + 1):
            np_array[i][j] = ((np_array[i][j] - mean[j - 1]) / standard[j - 1])
    return np_array
    #return the modifed instances array


def forward_selection(arr, numOfInstance, numOffeature):
    currentState = []
    goalState = []
    goalStateAccuracy = 0
    
    for i in range(numOffeature):  
        currentAccuracy = 0 
        featureSets = None
        bool_if_add = False
        
        for j in range(1, numOffeature + 1): 
            
            if j not in currentState:
                currentState.append(j)
                accuracy = cal_accuracy(arr, numOfInstance, currentState)
                print("Using feature(s) " + str(currentState) + " accuracy is " + str(accuracy) + "%")
                
                if accuracy > goalStateAccuracy:  
                    bool_if_add = True
                    goalStateAccuracy = accuracy
                
                if accuracy > currentAccuracy:  
                    currentAccuracy = accuracy
                    featureSets = j
                currentState.pop(len(currentState) - 1) 

        currentState.append(featureSets)
      
        if bool_if_add: 
            goalState = copy.deepcopy(currentState)  
            print("Feature set " + str(currentState) + " was best, accuracy is " + str(goalStateAccuracy) + "%")
        else:  
            print("The set is not more accurate than before")
            print("Feature set " + str(currentState) + " was best, accuracy is " + str(currentAccuracy) + "%")
            break  

    print("Therefore, Forward Selection returns the best feature set is " + str(goalState) + " which has an accuracy of " + str(
        goalStateAccuracy) + "%")
# return the trace of the foward_algorithm, best subset of features,  and accuracy


def backward_selection(arr, numOfInstance, numOffeature):
    
    currentState = list(range(1, numOffeature + 1))
    goalState = list(range(1, numOffeature + 1))
    goalStateAccuracy = 0.0

    for i in range(numOffeature):  
        currentAccuracy = 0  
        featureDelete = None
        bool_if_delete = False
        for j in range(1, numOffeature + 1):  
            
            if j in currentState:
                temp = [x for x in currentState if x != j]  
                accuracy = cal_accuracy(arr, numOfInstance, temp)
                print("Using feature(s) " + str(temp) + " accuracy is " + str(accuracy) + "%")
                if accuracy > goalStateAccuracy:  
                    bool_if_delete = True
                    
                    goalStateAccuracy = accuracy
                if accuracy > currentAccuracy:  
                    currentAccuracy = accuracy
                    featureDelete = j
              
        currentState.remove(featureDelete)
       
        if bool_if_delete:  
            goalState = copy.deepcopy(currentState)  
            print("Feature set " + str(currentState) + " was best, accuracy is " + str(goalStateAccuracy) + "%")
        else:  
            print("The set is not more accurate than before")
            print("Feature set " + str(currentState) + " was best, accuracy is " + str(currentAccuracy) + "%")

    print("Therefore, Backward Selection returns the best feature set is " + str(goalState) + " which has an accuracy of " + str(
        goalStateAccuracy) + "%")


def process():
    print("Welcome to Siyi Zhan(862053955)'s Feature Selection Solver.")
    file_name = input("Choose one file to test: ")
    #open the test file and return a failure message if invalid input
    try:
        file = open(file_name, "r")
    except IOError:
        raise IOError("No Such File") from None 
    #use sum function to learn the number of instances in the chosen file 
    numOfInstance = sum(1 for line in file)
    file.seek(0, 0)
    numOffeature = len(file.readline().split()) - 1 #-1 to exclude the class label 
    #use readline function to read, split all the keys in the file, len function return a number of features: how many keys do we have
    file.seek(0, 0)
    
    arr = [[0 for i in range(numOffeature + 1)] for j in range(numOfInstance)]  # +1  to include the class label
    #i is row, j represents for column(instance)
    # this array contains a features inside the instances!
    for i in range(numOfInstance):
        arr[i] = file.readline().split()
    np_array = np.array(arr, dtype=float)

    file.close()

    print("Analyze the test file: This file has " + str(numOffeature) +
          " features, and " +
          str(numOfInstance) + " instances.")

    dataNormalized = Normalization(np_array, numOfInstance, numOffeature)
    dataNormalized = dataNormalized.tolist()#normalized the data
    print("Normalized the Data..")

    print("Choose the algorithm you want to run.")
    print("Type 1 for Forward Selection")
    print("Tyoe 2 for Backward Selection")
    user_input = int(input())
    while user_input < 1 or user_input > 2:
        print("Invalid choice. Try again")
        user_input = int(input())

    featureGenerated = list(range(1, numOffeature + 1))

    accuracyGenerated = cal_accuracy(dataNormalized, numOfInstance, featureGenerated)
    print(
        "Iterating nearest neighbor algorithm with test files' " + str(
            numOfInstance) + " features" +
        ", which has an default accuracy of " + str(accuracyGenerated) + "%")
    print("Start Running the chosen Algroithm")
#Have the default accuarcy analysis first and then choose the other two algorithms to compare
    if user_input == 1:
        forward_selection(dataNormalized, numOfInstance, numOffeature)
    elif user_input == 2:
        backward_selection(dataNormalized, numOfInstance, numOffeature)


if __name__ == '__main__':
    process()