# Paycheck Protection Program Analysis

BACKGROUND:  
In 2020 the Paycheck Protection Program provided nearly $800 billion in loans to small businesses in order to retain payrolls. In the process, some applications were removed by the Small Business Administration with no specified explanation. This analysis looks into the characteristics of applications taken out and how they compare to the retained ones which may highlight the probable reasons why they were removed. 

METHODS:  
This analysis used the PPP removed applicants dataset provided by the U.S. Small Business Administration to explore the significant influential factors. For the first step of the analysis, the missing values were carefully addressed by observing the correlation between variables and filling them up with the suitable values. 

RESULTS:  
Some of the findings indicated that for the data remaining in the PPP dataset, over 99% the loan status is either “Exemption 4” or “Paid Full”. On the other hand, the loan status for data that were removed from the PPP dataset is 90.3% on “Actively Un-disbursed”, and 9.7% of “Exemption 4”.

CONCLUSION:  
Through the logistic regression model, it also displays that when using the variable, loan_status, as the only independent variable, the accuracy of prediction can achieve 96%. Hence, both the data visualization and model concluded that the loan_status is a significant predictor to predict whether there is a need to remove or keep the data or not.
