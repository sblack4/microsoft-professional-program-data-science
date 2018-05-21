import pandas as pd

# TODO: Load up the 'tutorial.csv' dataset
#
# .. your code here ..
census = pd.read_csv('datasets/tutorial.csv')


# TODO: Print the results of the .describe() method
#
# .. your code here ..
print(census.describe())


# TODO: Figure out which indexing method you need to
# use in order to index your dataframe with: [2:4,'col3']
# And print the results
#
# .. your code here ..

print(census.loc[2:4, 'col3'])
