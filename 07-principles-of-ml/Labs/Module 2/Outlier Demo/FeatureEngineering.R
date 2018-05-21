BikeShare <- maml.mapInputPort(1)

  ## Create a new feature to indicate workday
  BikeShare$isWorking <- ifelse(BikeShare$workingday & 
                                !BikeShare$holiday, 1, 0)  
  BikeShare$workingday <- NULL
  BikeShare$holiday <- NULL

  ## Add a feature with unique values for time of day for working and non-working days.
  BikeShare$workTime <- ifelse(BikeShare$isWorking, 
                             BikeShare$hr, 
                             BikeShare$hr + 24) 

  ## Add a column of the count of months from the origin
  BikeShare$month.count <- BikeShare$mnth + 12 * BikeShare$yr

maml.mapOutputPort('BikeShare')
