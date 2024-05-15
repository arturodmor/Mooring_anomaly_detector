from anchoring_detection.preprocess import Preprocess

import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import GridSearchCV

import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from sklearn.inspection import DecisionBoundaryDisplay


class Models(Preprocess):

    "Class to train and evaluate models"

    def __init__(self, dataframes_surge=None, dataframes_sway=None, df_surge = None, df_sway = None, n_states=10, n_dirs=5):
        super().__init__(movements=['Surge', 'Sway'], main_path=rf'D:\arturo_sim\simulaciones\acoplado', dataframes_surge=dataframes_surge, dataframes_sway=dataframes_sway)
        self.df_surge = df_surge
        self.df_sway = df_sway
        self.n_states = n_states
        self.n_dirs =n_dirs

    
    def transform_dataset(self,dataset):

        """ To divide and normalize dataset

        Returns:
            All Surge and Sway m0 instance, normalized and divided in train and test set
        """

        X = dataset[['m0_Surge','m0_Sway']]
        Y = dataset['Dragging']
        
        # Divide dataset in train and test data
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Normalize features
        min_max_scaler = MinMaxScaler()
        X_train_min_max = min_max_scaler.fit_transform(X_train)
        X_test_min_max = min_max_scaler.transform(X_test)

        return X_train_min_max, X_test_min_max, Y_train, Y_test
    

    def evaluate_models(self,model='svm'):

        """ To evaluate models before and after hyperparams setup

        Returns:
            Metrics and cross validation results. Dataframe with Hyperparams results
        """

        self.transform_dataset()

        if model == "svm":
            clf = svm.SVC()

            param_grid = [
                {'C':[1, 10, 100, 1000],'kernel':['linear']},
                {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
                {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['sigmoid']}
                ]
            
            metric_columns = ['param_C', 'param_gamma', 'param_kernel', 'mean_train_accuracy', 'mean_train_precision', 'mean_train_recall', 'mean_train_f1']

        elif model =="logistic":
            clf = LogisticRegression()

            param_grid = [
                {'C':[1, 10, 50, 100],'penalty':['l1','l2'],'solver':['liblinear']}
                ]
            
            metric_columns = ['param_C', 'param_penalty', 'param_solver', 'mean_train_accuracy', 'mean_train_precision', 'mean_train_recall', 'mean_train_f1']

        
        clf.fit(X_train_min_max,Y_train)

        #Cross Validation
        y_validate_scores = cross_val_score(clf, X_train_min_max, Y_train, cv=5,scoring='accuracy')
        y_validate_pred = cross_val_predict(clf, X_train_min_max, Y_train, cv=5)

        #Metrics
        accuracy = metrics.accuracy_score(Y_train,y_validate_pred)
        precision = metrics.precision_score(Y_train,y_validate_pred)
        recall = metrics.recall_score(Y_train,y_validate_pred)
        f1 = metrics.f1_score(Y_train,y_validate_pred)

        cm = metrics.confusion_matrix(Y_train,y_validate_pred)

        print(y_validate_scores, y_validate_pred, accuracy, precision, recall, f1, cm)
    
        #Hyperparams selection
        grid_search = GridSearchCV(clf, param_grid,  cv=5, scoring= ['accuracy','precision','recall','f1'],refit='accuracy', return_train_score=True)
        grid_search.fit(X_train_min_max,Y_train)

        hyperparams = pd.DataFrame(grid_search.cv_results_)
        hyperparams = hyperparams[metric_columns]

        return hyperparams


    def train_models(self,model='svm'):

        """ To train models and do prediction with test set

        Returns:
            Comparison between training and test set metrics
        """

        if model == "svm":
            clf = svm.SVC(C=1, kernel='linear')

        elif model =="logistic":
            clf = LogisticRegression(C=1, penalty='l2',solver='liblinear')

        #Train and predict
        clf.fit(X_train_min_max,Y_train)
        Y_pred_test = clf.predict(X_test_min_max)

        #Train metrics
        accuracy_train = metrics.accuracy_score(Y_train,y_validate_pred)
        precision_train = metrics.precision_score(Y_train,y_validate_pred)
        recall_train = metrics.recall_score(Y_train,y_validate_pred)
        f1_train = metrics.f1_score(Y_train,y_validate_pred)







