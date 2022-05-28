# -*- coding: utf-8 -*-
"""PPP Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lgfe-FJ1ygLohk_PMaH9vzxzeaY0aNy8
"""

# Import packages
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib 
import matplotlib.pyplot as plt
import sklearn
from sklearn import preprocessing

"""# All loans to Georgia businesses that remain in the PPP database (ppp_applicants_ga_full.csv)"""

# Import data
filepath = "ppp_applicants_ga_full.csv"
data = pd.read_csv(filepath)
df = pd.DataFrame(data)

# Data preprocessing
na = df.isna().any()
NA_columns = df.columns[na].tolist()
NA_columns

# Summary of the data (numerical variables)
df.describe(include=[np.number])

# Summary of the data (categorical variables)
df.describe(include=[object])

# Correct the data type: numerical to categorical
df.naics_code = df.naics_code.apply(str)
df.loan_number = df.loan_number.apply(str)
df.sba_office_code = df.sba_office_code.apply(str)
df.servicing_lender_location_id = df.servicing_lender_location_id.apply(str)
df.originating_lender_location_id = df.originating_lender_location_id.apply(str)

# Address the NA values
df.undisbursed_amount = df.undisbursed_amount.fillna(0)
df[df.project_county_name.isna()] # find the observations records of the NA value
df.project_county_name.fillna("LEE", limit = 1, inplace = True) # observation 39150: project_county_name = LEE
df.project_county_name.fillna("FULTON", limit = 1, inplace = True) # observation 88268: project_county_name = FULTON
df.project_county_name.fillna("COBB", limit = 1, inplace = True) # observation 177572: project_county_name = COBB
df.project_county_name.fillna("COLQUITT", limit = 1, inplace = True) # observation 239504: project_county_name = COLQUITT
df.project_county_name.fillna("GWINNETT", limit = 1, inplace = True) # observation 279180: project_county_name = GWINNETT
df.project_county_name.fillna("COBB", limit = 1, inplace = True) # observation 396988: project_county_name = COBB

# Drop name
df = df.drop(columns="name", axis=1)

# Drop forgiveness_amount
df = df.drop(columns="forgiveness_amount", axis=1)

# Drop forgiveness_data
df = df.drop(columns="forgiveness_date", axis=1)

"""# Loans to Georgia businesses that were removed from the PPP database (ppp-removed-ga.xlsx)"""

# Import data
filepath1 = "ppp-removed-ga.xlsx"
data1 = pd.read_excel(filepath1)
df1 = pd.DataFrame(data1)

# Data Prepocessing
na1 = df1.isna().any() 
NA_columns1 = df1.columns[na1].tolist()
NA_columns1

# Summary of loan_status_date
df1.loan_status_date.describe()

# Summary of the data (numerical variables)
df1.describe(include=[np.number])

# Summary of the data (categorical variables)
df1.describe(include=[object])

# Correct the data type: numerical to categorical
df1.naics_code = df1.naics_code.apply(str)
df1.loan_number = df1.loan_number.apply(str)
df1.sba_office_code = df1.sba_office_code.apply(str)
df1.servicing_lender_location_id = df1.servicing_lender_location_id.apply(str)
df1.originating_lender_location_id = df1.originating_lender_location_id.apply(str)
df1.forgiveness_date = df1.forgiveness_date.apply(str)

# Address the NA values
df1.undisbursed_amount = df1.undisbursed_amount.fillna(0)
df1 = df1.drop(columns="name" ,axis=1)
df1 = df1.drop(columns="forgiveness_amount" ,axis=1)
df1 = df1.drop(columns="forgiveness_date" ,axis=1)

# Create the variable "Removed"
df["removed"] = 0
df1["removed"] = 1

# Save datasets to new excel files
df.to_csv('new_ppp_applicants_ga_full.csv')
df1.to_excel('new_ppp-removed-ga.xlsx')

# import the saved data set
filepath_new_all = "new_combined_data.csv"
data_new_all = pd.read_csv(filepath_new_all)
df_new_all = pd.DataFrame(data_new_all)

# Address missing values
df_new_all.naics_code = df_new_all.naics_code.fillna("None")
df_new_all.business_type = df_new_all.business_type.fillna("None")
df_new_all.loan_status_date = df_new_all.loan_status_date.fillna("Other")

# Define Cohen's d function
def cohen(sample_1, sample_2):
  return (mean(sample_1) - mean(sample_2)) / (sqrt((stdev(sample_1) ** 2 + stdev(sample_2) ** 2) / 2))

# Prepare variables to calculate Cohen's d
df_fl = df_new_all.loc[df_new_all["removed"] == 0]
df_rm = df_new_all.loc[df_new_all["removed"] == 1]
df_fl["amount_per_job"] = df_fl.amount / df_fl.jobs_retained
df_rm["amount_per_job"] = df_rm.amount / df_rm.jobs_retained
lmi_num_fl = pd.Series(np.searchsorted(['N', 'Y'], df_fl.lmi_indicator), df_fl.index)
lmi_num_rm = pd.Series(np.searchsorted(['N', 'Y'], df_rm.lmi_indicator), df_rm.index)
RU_num_fl = pd.Series(np.searchsorted(['R', 'U'], df_fl.rural_urban_indicator), df_fl.index)
RU_num_rm = pd.Series(np.searchsorted(['R', 'U'], df_rm.rural_urban_indicator), df_rm.index)
hub_num_fl = pd.Series(np.searchsorted(['N', 'Y'], df_fl.hubzone_indicator), df_fl.index)
hub_num_rm = pd.Series(np.searchsorted(['N', 'Y'], df_rm.hubzone_indicator), df_rm.index)
job_noSP_fl = df_fl[df_fl.business_type != "Sole Proprietorship"]
job_noSP_fl = job_noSP_fl[job_noSP_fl.business_type != "Self-Employed Individuals"]
job_noSP_rm = df_rm[df_rm.business_type != "Sole Proprietorship"]
job_noSP_rm = job_noSP_rm[job_noSP_rm.business_type != "Self-Employed Individuals"]

# Calculate Cohen's d
print("The effect sample size for LMI indicator is",cohen(lmi_num_fl, lmi_num_rm))
print("The effect sample size for Rural Urban indicator is", cohen(RU_num_fl, RU_num_rm))
print("The effect sample size for Hubzone indicator is", cohen(hub_num_fl, hub_num_rm))
print("The effect sample size for amount is", cohen(df_fl.amount, df_rm.amount))
print("The effect sample size for amount per jobs retained is", cohen(df_fl.amount_per_job[df_fl.jobs_retained != 0], df_rm.amount_per_job[df_rm.jobs_retained != 0]))
print("The effect sample size for term", cohen(df_fl.term, df_rm.term))
print("The effect sample size for jobs retained", cohen(df_fl.jobs_retained, df_rm.jobs_retained))
print("The effect sample size for approval amount difference", cohen(df_fl.current_approval_amount - df_fl.initial_approval_amount, df_rm.current_approval_amount - df_rm.initial_approval_amount))
print("The effect sample size for jobs retained without sole proprietorship and self-employed individuals", cohen(job_noSP_fl.jobs_retained, job_noSP_rm.jobs_retained))

# Correlation Analysis
df_new_all_corr = df_new_all
df_new_all_corr.drop(["sba_office_code", "term", "sba_guaranty_percentage", "servicing_lender_location_id", "originating_lender_location_id", "Unnamed: 0", "naics_code", "loan_number", "removed"], axis = 1, inplace = True)
corr = df_new_all_corr.corr()
mask = np.triu(np.ones_like(corr, dtype = bool))
cmap = sn.diverging_palette(230, 20, as_cmap = True)
plt.show(sn.heatmap(corr, mask = mask, cmap = cmap, vmax = 1, vmin= -1, center = 0, annot = True, 
            square = True, linewidths = .3, cbar_kws = {"shrink": .5}, fmt='.2f'))

# Drop variables, and test 19 different models
df = df_new_all.drop(columns=["Unnamed: 0", "Unnamed: 0.1", "address", "city", "zip", "date_approved", "congressional_district", "loan_number", "servicing_lender_location_id", "servicing_lender_address", "servicing_lender_city", "servicing_lender_zip", "project_city", "project_county_name", "project_zip", "originating_lender_city", "loan_status_date", "originating_lender_location_id"] ,axis=1)
df1 = df_new_all.drop(columns="naics_code", axis=1) 
df2 = df1.drop(columns="processing_method", axis=1) 
df3 = df2.drop(columns="lender", axis=1) 
df5 = df3.drop(columns="rural_urban_indicator", axis=1) 
df6 = df5.drop(columns="lmi_indicator", axis=1) 
df7 = df6.drop(columns="servicing_lender_state", axis=1)  
df8 = df7.drop(columns="project_state", axis=1) 
df9 = df8.drop(columns="sba_office_code", axis=1) 
df10 = df9.drop(columns="servicing_lender_name", axis=1) 
df11 = df10.drop(columns="originating_lender_state", axis=1) 
df12 = df11.drop(columns="hubzone_indicator", axis=1) 
df13 = df13.drop(columns="current_approval_amount", axis=1) 
df14 = df15.drop(columns="initial_approval_amount", axis=1) 
df15 = df16.drop(columns="sba_guaranty_percentage", axis=1) 
df16 = df17.drop(columns="jobs_retained", axis=1) 
df17 = df19.drop(columns="amount", axis=1) 
df18 = df20.drop(columns="loan_status", axis=1)

# Get dummies
dm = pd.get_dummies(df21, drop_first=True)

"""# data patitioning"""

# Set the target variable
target = dm.removed

# Set the independent variables
indep_data = dm.drop(columns="removed", axis=1)

# Split the data and target into training and validation sets
from sklearn.model_selection import train_test_split
data_train, data_valid, target_train, target_valid = train_test_split(indep_data, target, test_size=0.3, random_state=50)

# Logistic regression model
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(data_train,target_train)

# Prediction
logreg.predict(data_valid)
print("Independent variables in model = %s" % data_train.columns.tolist())

# Accuracy
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
print("Accuracy for training = %.2f" % accuracy_score(target_train, logreg.predict(data_train)))
print("Accuracy for validation = %.2f" % accuracy_score(target_valid, logreg.predict(data_valid)))

# Confusion model
print(confusion_matrix(target_train, logreg.predict(data_train)))
print(confusion_matrix(target_valid, logreg.predict(data_valid)))

# ROC curve
print(roc_auc_score(target_train, logreg.predict(data_train)))
print(roc_auc_score(target_valid, logreg.predict(data_valid)))