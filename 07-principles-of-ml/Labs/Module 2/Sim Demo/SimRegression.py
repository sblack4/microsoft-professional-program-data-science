def sim_reg_data(xmin, xmax, ymin, ymax, n, sd):
    import pandas as pd
    import numpy.random as nr
    
    w = nr.normal(loc = 0, scale = sd, size = n)

    xstep = float(xmax - xmin)/float(n - 1)
    ystep = float(ymax - ymin)/float(n - 1)
    
    x = []
    xcur = xmin
    y = []
    ycur = ymin 
    for i in range(n):
        x.append(xcur)
        xcur += xstep
        y.append(ycur + w[i])
        ycur += ystep
    
    out = pd.DataFrame([x, y]).transpose()
    out.columns = ['x', 'y']    
    return out       


def sim_reg_outlier(xmin, xmax, ymin, ymax, n, sd, olX, olY):
    import pandas as pd
    import numpy.random as nr
    
    w = nr.normal(loc = 0, scale = sd, size = n)

    xstep = float(xmax - xmin)/float(n - 1)
    ystep = float(ymax - ymin)/float(n - 1)
    
    x = []
    xcur = xmin
    y = []
    ycur = ymin 
    for i in range(n):
        x.append(xcur)
        xcur += xstep
        y.append(ycur + w[i])
        ycur += ystep
    
    x.append(olX)
    y.append(olY)
    
    out = pd.DataFrame([x, y]).transpose()
    out.columns = ['x', 'y']    
    return out     


        
def plot_2D(df):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(8, 6))
    fig.clf()
    ax = fig.gca()
    df.plot(kind = 'scatter', x = 'x', y = 'y', ax = ax, alpha = 0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('X vs. Y')
    return 'Done'
 

        
def plot_reg(df):
    import matplotlib.pyplot as plt
    from sklearn import linear_model
    import math

    ## Prepare data for model
    nrow = df.shape[0]
    X = df.x.as_matrix().reshape((nrow,1))
    Y = df.y.as_matrix()
    ## Compute the linear model
    clf = linear_model.LinearRegression()
    lm = clf.fit(X, Y)
    ## Compute the y values
    df['lm_Y'] = lm.predict(X)   
    df.sort_values(by='x', ascending=True, inplace = True)

    fig, ax = plt.subplots(1, 2, figsize = (12,6))
    df.plot(kind = 'scatter', x = 'x', y = 'y', ax = ax[0], alpha = 0.5)
    df.plot(kind = 'line', x = 'x', y = 'lm_Y', style = ['r'], ax = ax[0])  
    ax[0].set_xlabel('X')
    ax[0].set_ylabel('Y')
    ax[0].set_title('X vs. Y')
    
    
    df['resids'] = (df.lm_Y - df.y)    
    ax[1].hist(df['resids'], bins = 30, alpha = 0.7) 
    ax[1].set_xlabel('Residual')
    ax[1].set_ylabel('Count')
    ax[1].set_title('Histogram of Residuals')  
    
    SSE = math.sqrt(sum(df.resids * df.resids))
    SSR = math.sqrt(sum(df.y * df.y))
    R2_adj = 1.0 - (SSE/SSR) * ((nrow - 1)/(nrow - 2))
    print('Intercept = ' + str(lm.intercept_))
    print('Slope = ' + str(lm.coef_[0]))
    print('Adjusted R^2 = ', str(R2_adj))
    return '  '


def sim_reg():
    import SimRegression as sr
    sds = [1, 5, 10]
    for sd in sds:
      reg_data = sr.sim_reg_data(1, 10, 1, 10, 50, sd)
      sr.plot_reg(reg_data)
    return 'Done'    
 
def sim_outlier():
    import SimRegression as sr
    ox = [0, 0, 5]
    oy = [10, -10, 10]
    for x, y in zip(ox, oy):
        reg_data = sr.sim_reg_outlier(1, 10, 1, 10, 50, 1, x, y)
        sr.plot_reg(reg_data)
    return 'Done'    
        
    