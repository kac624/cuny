This project aims to investigate the relationship between the competitiveness of electoral districts and the partisan leanings of candidates elected in those districts. The predominating narrative on partisan gerrymandering posits that redistricting efforts led by one-sided state legislatures leads to one-sided, uncompetitive congressional races, in which one party is heavily favored in most districts. In turn this lack of competition contributes to polarization, as the "real" races take place during primary elections, in which candidates are incentivized to take more extreme positions to appeal to their parties' political bases. This narrative is compelling, but I have found very limited empirical evidence to support it. Therein lies the goal of the analysis I put forth below: is there empirical support linking a lack of competitiveness with more polarizing candidates?  

Because these phenomena are not directly observable — referred to as "latent" variables — I consider six different proxy variables that attempt to quantify competitiveness and partisanship. To attempt to measure competitiveness, I consider three variables: the results of a 2022 study measuring voter policy preferences (referred to below as the "Ideology" measure; see [1]), the Cook Partisan Voting Index (referred to as "Cook PVI"; see [2]), and the average, district-level "efficiency gap" for all congressional elections since 2010 (see [3]). As a proxy of how far left or right candidates lean, I consider another three variables: the NOMINATE measure of ideological leanings in Congressional voting, popularized by Poole and Rosenthal (referred to as "Nominate"; see [4]), GovTrack's measure of partisan cooperation in Congress (referred to as "Govtrack"; see [5]) and a "homemade" measure of partisan rhetoric based on predictive modeling performed on a corpus candidate tweets. The construction of this final measure based on candidate tweets is the focus of the first four notebooks. The fifth notebook focuses on compiling competitiveness measure, and the final notebook implements final statistical analyses in an attempt to answer the original research question.  

Below is a walkthrough of the six primary notebooks.  

1.	Ballotpedia Scrape: I begin by scraping the Ballotpedia website to gather twitter handles for over a thousand House candidates.  
2.	Consolidate Candidates: I then query the Federal Election Committee (FEC) API to compile an official list of registered candidates in the 2022 midterm elections for the US House of Representatives. This dataset serves as the foundation upon which all other data is mapped. I then map Twitter handles to candidates, using data from Ballotpedia (see notebook 1), the @unitedstates project, and Politwoops.   
3.	Twitter Scrape: I next use the consolidates list of candidates and Twitter handles to scrape and compile over 2 million tweets. I also clean the candidates dataset to remove erroenous / outdated / duplicative Twitter handles.  
4.	Partisanship Scores: This notebook focuses on constructing and compiling three different measures of candidates’ partisanship. I leverage TF-IDF to engineer features for use in a number of probabilistic classification models (logistic regression, Naïve Bayes, XGBoost, SVM) that predict candidates’ party affiliation. I take the average of the probabilities assigned to each candidate by these models as a “partisanship score,” indicating how far left- or right-leaning each candidate is, in terms of their online rhetoric. I finally map these scores, along with two other measures of candidates’ ideological leanings (see [4] and [5] below), to the candidates dataset.  
5.	Competitiveness Scores: This notebook focuses on constructing and compiling three different measures of districts’ partisanship (inversely related to the districts competitiveness). I leverage the methodology described in [3] and historical elections data from the MIT Election Lab to calculate the efficiency gap for all 430+ congressional voting districts. I also gather district-level survey results on ideology and the Cook Partisan Voting Index (PVI) scores for 2022, and map both to the candidates dataset.  
6.	Partisanship vs Competitiveness: The final notebook (serving as the DATA606 final), starts with the final compiled candidates dataset, complete with candidates’ partisanship scores, along with competitiveness scores for the districts in which these candidates ran. Because of the latent nature of these variables, it is difficult to assign a high degree of confidence to any one test. I therefore found it useful to performing testing on all nine combinations of the above six variables, comparing results and assessing the persistence of any relationship holistically. I first conduct null hypothesis test to compare the mean partisanship score of candidates from districts with a high degree of competitiveness versus those from districts with a low degree of competitiveness. Results appear mixed, but tend to indicate only a weak relationship, if any, with three of the nine pairs of variables showing a statistically significant relationship. To follow up on this finding, I fit a series of linear regression models. Of the nine models, only three had statistically significant predictors, corresponding to the same three significant pairs from the first round of tests. Moreover, those three models offered only limited explanation of the variance in the dependent variable, as evidenced by low R-squared (all under 15%). While I would expect the relationship between variables to positive (i.e. more partisan districts should have more partisan candidates), the mixed signs of beta coefficients further highlights the lack of persistence in the relationship.

In conclusion, this analysis provides limited evidence of a persistent relationship between districts’ competitiveness and the partisan leanings of their candidates. 

Citations  
[1] Warshaw, Christopher, and Chris Tausanovitch. "Subnational ideology and presidential vote estimates (v2022)." Harvard Dataverse, 2022. https://doi.org/10.7910/DVN/BQKU4M.  
[2] The Cook Political Report. "The 2022 Cook Partisan Voting Index (Cook PVI) | Cook Political Report.“ 2022. https://www.cookpolitical.com/cook-pvi/2022-partisan-voting-index.  
[3] Stephanopoulos, Nicholas, and Eric McGhee. "Partisan Gerrymandering and the Efficiency Gap." University of Chicago Law Review 82 (2014): 831–900.
[4] Lewis, Jeffrey B., Keith Poole, Howard Rosenthal, Adam Boche, Aaron Rudkin, and Luke Sonnet. "Voteview: Congressional Roll-Call Votes Database." 2023. https://voteview.com/.  
[5] GovTrack.us. "Ideology Analysis of Members of Congress." 2013. https://www.govtrack.us/about/analysis.