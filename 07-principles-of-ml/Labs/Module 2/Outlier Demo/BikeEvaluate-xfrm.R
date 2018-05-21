df <- maml.mapInputPort(1)

order.frame <- function(df){
  df[order(df$days, df$workTime),]
}
df <- order.frame(df)
print('Ordered the data frame')


## Time series plots showing actual and predicted values; columns 3 and 4.
times <- c(6, 8, 10, 12, 14, 16, 18, 20)

ts.bikes <- function(t, df){
  require(ggplot2)
  temp <- df[df$workTime == t, ]
  ggplot() +
    geom_line(data = temp, 
              aes(x = days, y = cnt)) +
    geom_line(data = temp, 
              aes(x = days, y = predicted), color = "red") +
    ylab("Number of bikes rented") +
    labs(title = paste("Bike demand at ",
                       as.character(t), ":00", spe ="")) +
    theme(text = element_text(size=16))
}

lapply(times, ts.bikes, df)
print('applied the ts.bikes')

## Compute the residuals
resids <- function(df){
  library(dplyr)
  df <-  mutate(df, resids = predicted - cnt)
}


box.resids <- function(df){
  ## Plot the residuals by hour
  require(ggplot2)
  df <- resids(df)
  df$fact.hr <- as.factor(df$workTime)   
  print(str(df))
  ggplot(df, aes(x = fact.hr, y = resids)) + 
    geom_boxplot( ) + 
    ggtitle("Residual of actual versus predicted bike demand by hour")
}
box.resids(df)
print('made the boxplots')

hist.resids <- function(t, df){
  ## Plot the residuals by hour
  require(ggplot2)
  df <- resids(df[df$workTime == t, ])   
  print(str(df))
  ggplot(df, aes(resids)) + 
    geom_histogram( ) + 
    ggtitle(paste("Histogram of residuals for hour =", as.character(t)))
}

lapply(times, hist.resids, df)