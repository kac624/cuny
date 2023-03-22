# Q#7

( (15 * 80) + (20 * 90) ) / (20 + 15)

# Q#9 - 1.5 x IQR greater
median = 16.5
q1 = 15
q3 = 18
iqr = q3 - q1
q3 + 1.5 * iqr
q1 - 1.5 * iqr

# Q#11
(5/9) * (5/9) + (4/9) * (4/9)

# Q#13
dbinom(1, 3, prob = 0.767) + 
  dbinom(2, 3, prob = 0.767) + 
  dbinom(3, 3, prob = 0.767)
pbinom(0,3,0.767,lower.tail=FALSE)

# Q#15
(6/10) * (6/10) + (4/10) * (4/10)

# Q#19
library(ggplot2)
dist <- rnorm(1000, mean = 1500, sd = 500)
df <- data.frame(mean = 0)
for (i in 1:1000) {
  samp <- sample(x = dist, size = 100)
  df[i, 'mean'] <- mean(samp)
}
ggplot(df, aes(mean)) +
  geom_histogram()
