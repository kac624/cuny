data(gold)
data(woolyrnq)
data(gas)

gold_df <- data.frame(time = time(gold), series = gold)
woolyrnq_df <- data.frame(time = time(woolyrnq), series = woolyrnq)
gas_df <- data.frame(time = time(gas), series = gas)

write.csv(gold_df, 'data/gold.csv', row.names = F)
write.csv(woolyrnq_df, 'data/woolyrnq.csv', row.names = F)
write.csv(gas_df, 'data/gas.csv', row.names = F)

frequency(gold)
frequency(woolyrnq)
frequency(gas)

retaildata <- readxl::read_excel('data/retail.xlsx', skip=1)
myts <- ts(retaildata[,"A3349873A"],
           frequency=12, start=c(1982,4))
autoplot(myts)
ggseasonplot(myts)
ggsubseriesplot(myts)
gglagplot(myts)
ggAcf(myts)