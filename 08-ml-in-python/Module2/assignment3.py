import pandas as pd

# TODO: Load up the dataset
# Ensuring you set the appropriate header column names
#
# .. your code here ..
hds = ['motor', 'screw', 'pgain', 'vgain', 'class']
df = pd.read_csv('datasets/servo.data', names=hds)
print(df.head(5))
# TODO: Create a slice that contains all entries
# having a vgain equal to 5. Then print the 
# length of (# of samples in) that slice:
#
# .. your code here ..
vslice = df[df['vgain']==5]
print(vslice.describe())
# TODO: Create a slice that contains all entries
# having a motor equal to E and screw equal
# to E. Then print the length of (# of
# samples in) that slice:
#
# .. your code here ..
mslice = df[(df['motor']=='E') & (df['screw']=='E')]
print(mslice.describe())


# TODO: Create a slice that contains all entries
# having a pgain equal to 4. Use one of the
# various methods of finding the mean vgain
# value for the samples in that slice. Once
# you've found it, print it:
#
# .. your code here ..
pslice = df[df['pgain']==4]
print(pslice.describe())


# TODO: (Bonus) See what happens when you run
# the .dtypes method on your dataframe!
print(df.dtypes)


