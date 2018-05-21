BikeShare <- maml.mapInputPort(1)
require(dplyr)

## Build a dataframe with the quantile by month and 
## hour - workTime. Parameter Quantile determines the trim point. 
  Quantile <- 0.10
  quants <- (
    BikeShare %>%
      group_by(workTime, monthCount) %>%
      summarise(Quant = quantile(cnt,
                                 probs = Quantile, 
                                 na.rm = TRUE)) 
  )

maml.mapOutputPort('quants')
