dates <- seq(as.Date("2010/1/1"), by = "month", length.out = 10)
y1 <- seq(from = 100, by = 10, length.out = 10)
y2 <- exp(1:10)
# y2 <- seq(from = 150, by = 15, length.out = 10)

plot(dates, y1, type="l",col="red")
lines(dates, y2, col="green")

###

df <- data.frame(dates, y1, y2)
plot(df)

###

par(mar = c(5, 4, 4, 4) + 0.3)
plot(dates, y1, type="l",col="red")
par(new = TRUE)
plot(dates, y2, type = "l", axes = FALSE, bty = "n", xlab = "", ylab = "")
axis(side=4, at = pretty(range(y2)))
mtext("z", side=4, line=3)
