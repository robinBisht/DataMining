
# Importing the required packages
import numpy as np
import pandas as pd
import itertools
import warnings
warnings.filterwarnings(action='ignore')

# Reading and cleaning the data
titanic = pd.read_csv("Q2-tennis.csv")
target = titanic["Play"]
features = titanic.loc[:, ["Outlook","Temp","Humidity","Windy"]]

# Main class
class Node:
    def __init__(self, features, target):
        self.left = None 
        self.right = None
        self.features = features
        self.target = target 
        self.feature_types = self.select_dtype()
        
    # Identiy feature types
    def select_dtype(self):
        feature_types = []
        for item in self.features.columns:
            if self.features[item].dtype != "O":
                feature_types.append((item, "numerical")) 
            else:
                if self.features[item].nunique() <= 2:
                    feature_types.append((item, "binary"))
                else:
                    feature_types.append((item, "multiclass"))
        return feature_types
    
    # Calculate gini impurity for each feature at a node
    # Need to provide a default value as a fallback 
    @staticmethod
    def gini_impurity_total(a=0, b=0, c=0, d=0):
        total_elements = a + b + c + d
        gini_1 = 1 - np.square(a/(a+b)) - np.square(b/(a+b))
        # print("{},{},{},{}".format(a,b,c,d))
        gini_2 = 1 - np.square(c/(c+d)) - np.square(d/(c+d))
        total_gini = ((a+b)/total_elements) * gini_1 + ((c+d)/total_elements) * gini_2
        return total_gini 
    
    @staticmethod
    def gini_impurity(a=0, b=0):
        return 1 - np.square(a/(a+b)) - np.square(b/(a+b))
    
    # Calculate gini for all feature combinations in categorical features
    def calculate_gini(self, feature):
        gini_node = []
        combinations = []
        for i in range(1, self.features[feature].nunique()):
            combinations = combinations + list(itertools.combinations(self.features[feature].unique(), i))
       
        for item in combinations:
            t1 = self.target[self.features[feature].isin(item)] 
            t2 = self.target[~self.features[feature].isin(item)]
            tone = t1.value_counts().tolist()
            ttwo = t2.value_counts().tolist()
            tne = [False,False]
            if len(tone) < 2:
                for ind,ite in t1.items():
                    if ite == 'yes':
                        tne[0] = True
                    elif ite == 'no':
                        tne[1] == True
                if not tne[0]:
                    tone.insert(0,0)
                elif not tne[1]:
                    tone.append(0)
            tne = [False,False]
            if len(ttwo) < 2:
                for ind,ite in t2.items():
                    if ite == 'yes':
                        tne[0] = True
                    elif ite == 'no':
                        tne[1] == True
                if not tne[0]:
                    ttwo.insert(0,0)
                elif not tne[1]:
                    ttwo.append(0)
            args = tone+ttwo
            gini_node.append(Node.gini_impurity_total(*args))
        return gini_node, combinations # Return all the values 
# Get the best gini values for each feature  
    def evaluate_node(self):
        gini_values = []
        for feature in self.features.columns:
            # print(feature)
            calculated_gini, combinations = self.calculate_gini(feature)
            best_combination = combinations[np.argmin(calculated_gini)]
            gini_values.append((feature, best_combination, np.min(calculated_gini)))
        # print("gini_values_evaluate_node: {}".format(gini_values))
        return gini_values
                
    # Inserting a new node based on the decision criteria
    def insert_node(self):
        gini_values = self.evaluate_node()
        values = [item[2] for item in gini_values]
        node_gini =  Node.gini_impurity(*self.target.value_counts().tolist())
        
         # Terminate the branch if current gini is better or no features to split
        if node_gini < np.min(values): 
            print("terminating the branch")
            self.left = None
            self.right = None 
        else:
            best_feature = gini_values[np.argmin(values)][0]
            best_combination = gini_values[np.argmin(values)][1]
            print(f"Creating a new branch using {best_feature} and {best_combination}")
            left_features = self.features[self.features[best_feature].isin(best_combination)]
            left_features.drop([best_feature], axis=1, inplace=True)
            left_target = self.target[self.features[best_feature].isin(best_combination)]
            if list(left_features.columns) == []:
                self.left = None 
                self.right = None
            else:
                self.left = Node(left_features, left_target)
                # print("test")
                self.left.insert_node()

            right_features = self.features[~self.features[best_feature].isin(best_combination)]
            right_target = self.target[~self.features[best_feature].isin(best_combination)]
            right_features.drop([best_feature], axis=1, inplace=True)
            if list(right_features.columns) == []:
                self.left = None 
                self.right = None
            else:
                self.right = Node(right_features, right_target)
                self.right.insert_node()

# Creating the root node with the full dataset 
root = Node(features, target)

# Building the tree 
root.insert_node()