import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib

###############################
# Read Data #
############################## 
frame = pd.read_csv('data.csv')

###############################
# Clean Data #
############################## 

### To Numeric 
numCols = ['Current Loan Amount', 'Credit Score', 'Annual Income', 'Years of Credit History'
           , 'Months since last delinquent', 'Number of Open Accounts', 'Number of Credit Problems'
           , 'Current Credit Balance', 'Bankruptcies', 'Tax Liens']
makeNumCols = ['Monthly Debt', 'Maximum Open Credit']
both = numCols + makeNumCols
for col in both:
    frame[col] = pd.to_numeric(frame[col], errors='coerce')
    frame[col] = frame[col].fillna(frame[col].mode())

### Handle strings / dummy variables 
stringColumns = ['Home Ownership', 'Term','Purpose','Years in current job']
frame['Home Ownership'] = frame['Home Ownership'].replace('havemortgage', 'home mortgage')
convert = {'10+ years' : 10, '1 year': 1, '< 1 year': 1, '9 years': 9, '3 years': 3, '4 years': 4,
       'n/a': 0, '5 years': 5, '7 years': 7, '2 years': 2, '6 years': 6, '8 years': 8}
frame = frame.replace({'Years in current job': convert})
for col in ['Home Ownership', 'Term','Purpose']:
    frame[col] = frame[col].str.lower()
    dummy_df = pd.get_dummies(frame[col])
    frame = pd.concat([frame, dummy_df], axis=1)

### Handle Outliers 
frame = frame[frame['Annual Income'] < 2000000]
frame = frame[frame['Current Loan Amount'] < 99999990]
frame = frame[frame['Credit Score'] < 1000]

### train_test_split
test_set = frame[frame.columns.difference(['Loan Status', 'Customer ID', 'Loan ID', 'Home Ownership', 'Term','Purpose'])]
X_train, X_test, y_train, y_test = train_test_split(test_set ,frame['Loan Status'], test_size=0.9)

### Initialize and fit model 
gbc = GradientBoostingClassifier(max_depth=3)
gbc.fit(X_train, y_train)
gbc_score = gbc.score(X_test, y_test)
print('gbc_score '+ str(gbc_score))

### Pickle model
joblib.dump(gbc, 'GradBooClas.pkl')