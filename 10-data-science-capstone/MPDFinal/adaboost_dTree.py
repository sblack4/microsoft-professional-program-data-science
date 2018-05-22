import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib

import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
from sklearn import preprocessing, linear_model

###############################
# Read Data #
############################## 
frame = pd.read_csv('data.csv')


###############################
# Clean Data #
############################## 

## strings to lowercase and merge values
stringColumns = ['Home Ownership', 'Term','Purpose','Years in current job']
for col in stringColumns:
    frame[col] = frame[col].str.lower()
frame['Home Ownership'] = frame['Home Ownership'].replace('havemortgage', 'home mortgage')
frame['Years in current job'] = frame['Years in current job'].replace('n/a', '10+ years')

## numbers all the things
numCols = ['Current Loan Amount', 'Credit Score', 'Annual Income', 'Years of Credit History'
           , 'Months since last delinquent', 'Number of Open Accounts', 'Number of Credit Problems'
           , 'Current Credit Balance', 'Bankruptcies', 'Tax Liens']
makeNumCols = ['Monthly Debt', 'Maximum Open Credit']
both = numCols + makeNumCols
frame['Current Loan Amount'] = frame['Current Loan Amount'].replace(99999999.0, 'Nan')
for col in both:
    frame[col] = pd.to_numeric(frame[col], errors='coerce')
    frame[col] = frame[col].fillna(frame[col].mode())
    frame[col] = frame[col].fillna(frame[col].mean())

## 
# all_cols = ['Loan ID', 'Customer ID', 'Loan Status', 'Current Loan Amount', 'Term',
#        'Credit Score', 'Years in current job', 'Home Ownership',
#        'Annual Income', 'Purpose', 'Monthly Debt', 'Years of Credit History',
#        'Months since last delinquent', 'Number of Open Accounts',
#        'Number of Credit Problems', 'Current Credit Balance',
#        'Maximum Open Credit', 'Bankruptcies', 'Tax Liens']
num_colsN_loanStuff = ['Current Loan Amount', 'Credit Score', 'Annual Income', 'Years of Credit History'
           , 'Months since last delinquent', 'Number of Open Accounts', 'Number of Credit Problems'
           , 'Current Credit Balance', 'Bankruptcies', 'Tax Liens'
            , 'Monthly Debt', 'Maximum Open Credit', 'Loan Status', 'Loan ID']
string_cols = ['Term', 'Years in current job', 'Home Ownership', 'Purpose']
new_df = frame[num_colsN_loanStuff]
for col in string_cols:
    dummy_df = pd.get_dummies(frame[col])
    new_df = pd.concat([new_df, dummy_df], axis=1)
new_df = new_df.set_index('Loan ID')
 
###############################
# Split into Test/Train Sets #
##############################

test_set = new_df[new_df.columns.difference(['Loan Status'])]
X_train, X_test, y_train, y_test = train_test_split(test_set ,new_df['Loan Status'], test_size=0.7)

 
# #############################
# # Save Test/Train Data Set #
# ############################
# # test.to_csv('/home/drcrook/data/EE_Regression_Test.csv')
# # train.to_csv('/home/drcrook/data/EE_Regression_Train.csv')
 
# #########################
# # Preprocess Functions #
# ########################
# #Get Min/Max Params
# def MinMaxParams(df):
#     return df.min(), df.max()
 
# #Min/Max Normalization
# def MM_Normalize(df, min_vals, max_vals):
#     return (df - min_vals) / (max_vals - min_vals)
 
# #Inverse Min/Max Normalization
# def Inverse_MM_Normalize(df, min_vals, max_vals):
#     return ((max_vals - min_vals) * df) + min_vals
 
# ###############################################
# # Get Params and save them, will need in AML #
# ##############################################
# params = MinMaxParams(train)
 
# ###############################
# # Pre-Process Data for Model #
# ##############################
# #Normalize Data
# train_n = MM_Normalize(train, params[0], params[1])
# test_n = MM_Normalize(test, params[0], params[1])
 
# #Extract y's as own set & drop from inputs
# train_y = train_n['Heating Load']
# train_n.drop('Heating Load', axis = 1, inplace=True)
 
# #we want true test_y's, we don't want to judge against inversed normalization.
# #we want to test against the original answers, so snag that, and drop labels
# #from normalized data set.
# test_y = test['Heating Load']
# test_n.drop('Heating Load', axis = 1, inplace=True)
 
# #Convert to numpy matrices, as this is what SKLearn wants.
# train_n = train_n.as_matrix()
# test_n = test_n.as_matrix()
 
############################
# Now for Machine Learning #
############################
# model = linear_model.LinearRegression()
# model.fit(train_n, train_y)

# # Create and fit an AdaBoosted decision tree
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), algorithm="SAMME", n_estimators=200)
bdt.fit(X_train, y_train)
bdt_score = bdt.score(X_test, y_test)
print('bdt score' + str(bdt_score))

# #GradientBoostingClassifier
gbc = GradientBoostingClassifier(max_depth=3)
gbc.fit(X_train, y_train)
gbc_score = gbc.score(X_test, y_test)
print('gbc_score '+ str(gbc_score))



#############
# Inference #
############
# predictions_n = model.predict(test_n)
# predictions = Inverse_MM_Normalize(predictions_n, 
#                                    params[0]['Heating Load'], 
#                                    params[1]['Heating Load'])
 
######################
# Calculate Metrics #
#####################
# from sklearn.metrics import mean_squared_error
# RMSE = mean_squared_error(predictions, test_y)**0.5
# RMSE
 
 
#############################################
# Persist Model for AML Operationalization #
############################################
# joblib.dump(model, '/home/drcrook/data/EE_Model/model.pkl')

#joblib.dump(gbc, 'model.pkl')
#joblib.dump(bdt, 'model.pkl')
 
# #test model
# model2 = joblib.load('/home/drcrook/data/EE_Model/model.pkl')
# p = Inverse_MM_Normalize(model2.predict(test_n), 
#                          params[0]['Heating Load'],
#                          params[1]['Heating Load'])
# #ensure same RMSE
# RMSE = mean_squared_error(p, test_y)**0.5
# RMSE  