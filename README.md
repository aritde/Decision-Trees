# Decision-Trees

Implementing classification trees and evaluating their accuracy. This program

a) Learns a classification tree given a data set. All features are assumed to be numerical. Gini or information gain,as specified
by user,  are used to decide on the best attribute to split in every step. Stops growing the tree when all examples in a node 
belong to the same class or the remaining examples contain identical features.

b) Implements cross-validation to evaluate the accuracy of the algorithm on 10 different data sets from the UCI Machine Learning 
Repository. Categorical features are converted to numerical by encoding them using sparse binary representation. 
