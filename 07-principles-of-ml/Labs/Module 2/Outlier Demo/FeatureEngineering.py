def azureml_main(df):
    import numpy as np
 
    ## Create a new column to indicate if the day is a working day
    work_day = df['workingday'].as_matrix()
    holiday = df['holiday'].as_matrix()                       
    df['isWorking'] = np.where(np.logical_and(work_day == 1, holiday == 0), 1, 0)
    
    ## Compute a new column with the count of months 
    df['monthCount'] = 12 * df.yr + df.mnth

    ## Add a variable with unique values for time of day for working 
    ## and non-working days
    isWorking = df['isWorking'].as_matrix()
    df['workHr'] = np.where(isWorking, 
                                        df.hr, 
                                        df.hr + 24.0)
    
    ## Drop unneded columns
    df = df.drop(['workingday', 'holiday', 'hr'], axis = 1)
    
    return df 
    