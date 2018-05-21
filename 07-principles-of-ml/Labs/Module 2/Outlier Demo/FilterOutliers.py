def azureml_main(df, quantile):
    import pandas as pd
    
    ## Save the original names of the DataFrame.
    in_names = list(df)
    
    df = pd.merge(df, quantile,
                     left_on = ['monthCount', 'workHr'], 
                     right_on = ['monthCount', 'workHr'],
                     how = 'inner')   

    ## Filter rows where the count of bikes is less than the lower quantile.                                         
    df = df.ix[df['cnt'] > df['quantile']]      
    
    ## Remove the unneeded column and restore the original column names. 
    df.drop('quantile', axis = 1, inplace = True)
    df.columns = in_names  

    ## Sort the data frame based on the dayCount
    df.sort(['days', 'workHr'],  axis = 0, inplace = True)     
    
    return df
