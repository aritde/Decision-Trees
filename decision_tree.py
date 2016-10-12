import random
import math

# Sample datasets
dataFile=open("C:/Transferred/b565/iris.data",'r')
testFile=open("C:/Transferred/b565/test.data",'r')
#dataFile=open("C:/Transferred/b565/ecoli.data",'r')
#dataFile=open("C:/Transferred/b565/wine.data",'r')

test_data=[]
for line in testFile:
   arrList=[]
   arr=line.replace("\n","").split(",")
   for val in arr:
     try:
       arrList.append(float(val))
     except ValueError:
         arrList.append(val)
   test_data.append(arrList)
random.shuffle(test_data)

my_data=[]
for line in dataFile:
   arrList=[]
   arr=line.replace("\n","").split(",")
   for val in arr:
     try:
       arrList.append(float(val))
     except ValueError:
         arrList.append(val)
   my_data.append(arrList)
random.shuffle(my_data)
class node:
     def __init__(self,col=-1,value=None,results=None,left=None,right=None):
        self.col=col
        self.value=value
        self.results=results
        self.left=left
        self.right=right
def division_into_different_sets(dataset,dividing_attribute,threshold):
    success_set=[]
    non_success_set=[]
    if isinstance(threshold,int) or isinstance(threshold,float):
        for each_row in dataset:
            if each_row[dividing_attribute]>=threshold:
                success_set.append(each_row)
            else:
                non_success_set.append(each_row)
    else:
        for each_row in dataset:
            if  each_row[dividing_attribute]==threshold:
                success_set.append(each_row)
            else:
                non_success_set.append(each_row)
    """for i in success_set:
        print i"""
    return (success_set,non_success_set)
def each_category(dataset):
    type_dict = {}
    for each_row in dataset:
        collen = len (each_row)
        types = each_row[collen - 1]
        if types not in type_dict:
            type_dict[types]=0
        type_dict[types] = type_dict[types] + 1
    """for value in type_dict: # can be removed
        print {value : type_dict[value]}  can be removed
    """
    return type_dict
#each_category(dataset)
def gini_value (dataset):
    intermediate_value = 0.0
    unique_classes = each_category(dataset)
    number_of_unique_classes = len(unique_classes)
    len_dataset = len(dataset)
    for each_type in unique_classes.keys():
        prob_value = float (unique_classes[each_type])/len_dataset
        intermediate_value = intermediate_value + (prob_value*prob_value)
    final_value = 1 - intermediate_value
    return final_value
def entropy_value (dataset):
    calculated_entropy = 0.0
    type_dict = each_category(dataset)
    type_dict_length = len(type_dict)
    dataset_length = len (dataset)
    for each_type in type_dict.keys():
        intermediate_value = 1.0
        prob_value = float(type_dict[each_type])/dataset_length
        intermediate_value = (-1.0) * prob_value * math.log(prob_value,2)
        calculated_entropy = calculated_entropy + intermediate_value
    #print calculated_entropy
    return calculated_entropy

def create_bin_tree (dataset,measure=entropy_value):
    if measure == entropy_value:
        if len(dataset) == 0:
            return node()
        current_entropy_score = measure(dataset)
        best_info_gain =0.0
        best_attribute_for_splitting = None
        best_sets = None
        collen = len(dataset[0])-1
        unique_coulmn_values = {}
        for each_column in range (0, collen):
            unique_coulmn_values = set([row[each_column] for row in dataset])
            for key in unique_coulmn_values:
                success_set,unsuccessful_set = division_into_different_sets(dataset,each_column,key)
                prob_value = float(len(success_set))/len(dataset)
                info_gain = current_entropy_score - prob_value*entropy_value(success_set) - (1-prob_value)*entropy_value(unsuccessful_set)
                """
                intermediate_value = (-1)*((prob_value*entropy_value(success_set)) + (1-prob_value)*entropy_value(unsuccessful_set))
                info_gain = current_entropy_score - intermediate_value
                """
                if info_gain > best_info_gain and len(success_set)>0 and len(unsuccessful_set) > 0:
                    best_info_gain = info_gain
                    best_attribute_for_splitting = (each_column , key)
                    best_sets=(success_set,unsuccessful_set)
        if best_info_gain > 0:
            trueBranch = create_bin_tree(best_sets[0])
            falseBranch = create_bin_tree(best_sets[1])
            return node(col=best_attribute_for_splitting[0],value=best_attribute_for_splitting[1],left=trueBranch,right=falseBranch)
        else:
            return node(results=each_category(dataset))
    elif measure == gini_value:
        if len(dataset) == 0:
            return node()
        current_gini_score = measure(dataset)
        best_info_gain =0.0
        best_attribute_for_splitting = None
        best_sets = None
        collen = len(dataset[0])-1
        unique_coulmn_values = {}
        for each_column in range (0, collen):
            unique_coulmn_values = set([row[each_column] for row in dataset])
            for key in unique_coulmn_values:
                success_set,unsuccessful_set = division_into_different_sets(dataset,each_column,key)
                prob_value = float(len(success_set))/len(dataset)
                info_gain = current_gini_score - prob_value*gini_value(success_set) - (1-prob_value)*gini_value(unsuccessful_set)
                """
                intermediate_value = (-1)*((prob_value*entropy_value(success_set)) + (1-prob_value)*entropy_value(unsuccessful_set))
                info_gain = current_entropy_score - intermediate_value
                """
                if info_gain > best_info_gain and len(success_set)>0 and len(unsuccessful_set) > 0:
                    best_info_gain = info_gain
                    best_attribute_for_splitting = (each_column , key)
                    best_sets=(success_set,unsuccessful_set)
        if best_info_gain > 0:
            trueBranch = create_bin_tree(best_sets[0])
            falseBranch = create_bin_tree(best_sets[1])
            return node(col=best_attribute_for_splitting[0],value=best_attribute_for_splitting[1],left=trueBranch,right=falseBranch)
        else:
            return node(results=each_category(dataset))
# The user has to pass "measure = entropy_value" in order to calculate entropy instead of gini_value
trained_tree = create_bin_tree(my_data,measure=gini_value)

def labelling_new_data (test_list,trained_tree):
    new_child = None
    if trained_tree.results!=None:
        return trained_tree.results
    else:
        split_value=test_list[trained_tree.col]
        if (isinstance(split_value,int)):
            if split_value<trained_tree.value:
                new_child = trained_tree.right
            else:
                new_child = trained_tree.left
        elif(isinstance(split_value,float)):
            if split_value<trained_tree.value:
                new_child = trained_tree.right
            else:
                new_child = trained_tree.left
        else:
            if split_value != trained_tree.value:
                new_child = trained_tree.right
            else:
                new_child == trained_tree.left
    return labelling_new_data(test_list,new_child)

def testing (test_data):
    result_outcome_set = []
    for each_record in test_data:
        result_returned = labelling_new_data(each_record,trained_tree)
        result_outcome_set.append(result_returned)
    return result_outcome_set
#print "New" + str(a)
print "Results"
result_st = testing(test_data)
for record in result_st:
        print record.keys()

def cross_validation():
    count = 0
    data_value = []
    result_st = testing(test_data)
    record = {}
    #for record in result_st:
        #print record.keys()
    while ((record in result_st) and  (data_value in test_data )):
        print record.keys()
        if(record.keys() == data_value[-1]):
            count = count + 1
        else:
            continue
    print count
    success_count = (count/len(test_data)) *100.0
    print "Success rate = " + str(success_count)
cross_validation()
#for data in test_data:
#    print data[-1]S