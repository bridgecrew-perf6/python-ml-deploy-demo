# The model training codes are the same as those from https://towardsdatascience.com/credit-card-fraud-detection-using-machine-learning-python-5b098d4a8edc
# The creditcard.csv file can be downloaded from https://www.kaggle.com/mlg-ulb/creditcardfraud

# Import libraries and packages
import joblib
import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
from termcolor import colored as cl # text customization
from xgboost import XGBClassifier


def train_model():
    # Import Dataset
    data=pd.read_csv("creditcard.csv")

    # Check transaction distribution
    Total_transactions = len(data)
    normal = len(data[data.Class == 0])
    fraudulent = len(data[data.Class == 1])
    fraud_percentage = round(fraudulent/normal*100, 2)
    print(cl('Total number of Trnsactions are {}'.format(Total_transactions), attrs = ['bold']))
    print(cl('Number of Normal Transactions are {}'.format(normal), attrs = ['bold']))
    print(cl('Number of fraudulent Transactions are {}'.format(fraudulent), attrs = ['bold']))
    print(cl('Percentage of fraud Transactions is {}'.format(fraud_percentage), attrs = ['bold']))

    # Check for null values
    data.info()

    # Scale Variable
    sc = StandardScaler()
    amount = data['Amount'].values
    data['Amount'] = sc.fit_transform(amount.reshape(-1, 1))

    # Drop Time variable
    data.drop(['Time'], axis=1, inplace=True)

    # Drop Duplicates
    data.drop_duplicates(inplace=True)

    # Train & Test Split
    x = data.drop('Class', axis = 1).values
    y = data['Class'].values
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 1)

    # Model Building
    # XGBoost
    xgb = XGBClassifier(max_depth = 4)
    xgb.fit(X_train, y_train)
    preds = xgb.predict(X_test)

    print('Accuracy score of the XGBoost model is {}'.format(accuracy_score(y_test, preds)))
    print('F1 score of the XGBoost model is {}'.format(f1_score(y_test, preds)))

    # Save Model
    joblib.dump(xgb, 'credit-card-fraud-model.model')