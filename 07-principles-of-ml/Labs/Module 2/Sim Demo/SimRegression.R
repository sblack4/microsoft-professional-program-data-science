sim.reg.data <- function(x1, y1, x2, y2, n, sd){
  w <- rnorm(n, mean = 0, sd = sd)
  data.frame(
              x = seq(from = x1, to = x2, length.out = n),
              y = (seq(from = x1, to = x2, length.out = n) + w)
            )
}


sim.reg.outlier <- function(x1, y1, x2, y2, n, sd, ox, oy){
  w <- rnorm(n, mean = 0, sd = sd)
  df <- data.frame(
            x = c(seq(from = x1, to = x2, length.out = n), ox),
            y = c((seq(from = x1, to = x2, length.out = n) + w), oy)
          )
  df[order(df$x),]
}


plot.reg <- function(df){
  require(ggplot2)
  ggplot(df, aes(x, y)) + 
    geom_point(size = 2) +
    ggtitle('X vs. Y')
}


plot.reg <- function(df){
  require(ggplot2)
  require(gridExtra)
  mod <- lm(y ~ x, data = df)
  df$score <- predict(mod)
  df$resids <- df$y - df$score
  
  p1 <- ggplot(df, aes(x, y)) + 
          geom_point(size = 2) +
          geom_line(aes(x, score, color = 'Red')) + 
          ggtitle('X vs. Y with regression')
 
  p2 <- ggplot(df, aes(resids)) +
           geom_histogram() +
           ggtitle('Distribution of residuals')
  
  grid.arrange(p1, p2, nrow = 2)
  
  print(paste('Intercept =', as.character(mod$coefficients[1])))
  print(paste('Slope =', as.character(mod$coefficients[2])))
  
  SSE <- sqrt(sum(df$resids * df$resids))
  SSR <- sqrt(sum(df$y * df$y))
  n = nrow(df)
  adjR2  <- 1.0 - (SSE/SSR) * ((n - 1)/(n - 2))
  print(paste('Adjusted R^2 =', as.character(adjR2)))
}


demo.reg <- function(){
  sd <- c(1, 5, 10)
  for(i in 1:3){
    regData <-  sim.reg.data(0, 0, 10, 10, 50, sd[i])
    plot.reg(regData)
  }
}


demo.outlier <- function(){
  ox <- c(0, 0, 5)
  oy <- c(10, -10, 10)
  for(i in 1:3){
    regData <-  sim.reg.outlier(0, 0, 10, 10, 50, 1, ox[i], oy[i])
    plot.reg(regData)
  }
}


