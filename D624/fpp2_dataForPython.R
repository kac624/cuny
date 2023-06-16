library(fpp2)

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


data(plastics)
plastics_df <- data.frame(time = time(plastics), series = plastics)
write.csv(plastics_df, 'data/plastics.csv', row.names = F)


data(pigs)
pigs_df <- data.frame(time = time(pigs), series = pigs)
write.csv(pigs_df, 'data/pigs.csv', row.names = F)


data(ibmclose)
ibm_df <- data.frame(time = time(ibmclose), series = ibmclose)
write.csv(ibm_df, 'data/ibm.csv', row.names = F)


set.seed(42)
e <- rnorm(100)
write.csv(e, 'data/rnorm.csv', row.names = F)


data(austa)
austa_df <- data.frame(time = time(austa), series = austa)
write.csv(austa_df, 'data/austa.csv', row.names = F)


library(mlbench)

data(Glass)
write.csv(Glass, 'data/glass.csv', row.names = F)

data(Soybean)
write.csv(Soybean, 'data/soybean.csv', row.names = F)
