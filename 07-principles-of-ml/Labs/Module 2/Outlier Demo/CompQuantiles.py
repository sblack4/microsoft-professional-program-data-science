def azureml_main(df):
    import pandas as pd
    ## Compute the lower quantile of the number of biked grouped by
    ## Date and time values. 
    out = df.groupby(['monthCount', 'workHr']).cnt.quantile(q = 0.2)
    out = pd.DataFrame(out)
    out.reset_index(inplace=True) 
    out.columns = ['monthCount', 'workHr', 'quantile']
    return out
    
