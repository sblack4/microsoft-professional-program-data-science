BikeShare <- maml.mapInputPort(1)
quants <- maml.mapInputPort(2)
  require(dplyr)

## Join the quantiles to the dataframe
  BikeShare <- left_join(BikeShare, quants)

## Filter for the rows we want and remove the no longer needed column
  BikeShare <- BikeShare %>% 
      filter(cnt > Quant) 
  BikeShare[, "Quant"] <- NULL

## Output the transformed data frame.
maml.mapOutputPort('BikeShare')

