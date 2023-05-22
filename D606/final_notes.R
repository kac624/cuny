####### Q1
# ci = mu +/- z * s / sqrt(n)
# z = 2.576
z = -qnorm((1 - 0.99) / 2)
z = qnorm(0.99 + ((1 - 0.99) / 2))
s = 0.534
z * s


###### Q3
# 13 of 52 trucks and 11 of 88 cars failed the emissions test
# SE = sqrt [ SE_{1} + SE_{2} ] 
# SE = sqrt [ (p(1-p)_{1} / n_{1}) + (p(1-p)_{2} / n_{2}) ]
p1 = 13 / 52
se1 = p1*(1-p1) / 52
p2 = 11 / 88
se2 = p2*(1-p2) / 88
SE = sqrt(se1 + se2)
round(SE,3)

###### Q6
# ci = mu +/- z * s / sqrt(n)
z = 1
s = 1
n = 100
MOE1 = z * s / sqrt(n)
MOE1
MOE2 = z * s / sqrt(n*16)
MOE2
MOE1 / MOE2
n * 16
