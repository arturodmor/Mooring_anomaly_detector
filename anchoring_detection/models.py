from anchoring_detection.preprocess import Preprocess

import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn import metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from sklearn.inspection import DecisionBoundaryDisplay

import logging

logger = logging.Logger(__name__)


class Models(Preprocess):

    "Class to train and evaluate models"

    def __init__(self, cm = None, df_metrics = None):
        super().__init__()
        self.cm = cm
        self.df_metrics = df_metrics

    
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


    def return_metrics(self,Y = None, Y_pred = None):

        """To return training metrics

        Args:
            Y(Object): Train or test label set from the dataset
            Y_pred(Object): Predictions

        Returns:
            cm(Object): COnfusión matrix
            df_metrics(Dataframe): Dataframe with considered metrics
        """

        try:
            # Metrics
            accuracy = metrics.accuracy_score(Y,Y_pred)
            precision = metrics.precision_score(Y,Y_pred)
            recall = metrics.recall_score(Y,Y_pred)
            f1 = metrics.f1_score(Y,Y_pred)
            self.cm = metrics.confusion_matrix(Y,Y_pred)

            data = {
                'accuracy': [accuracy],
                'precision': [precision],
                'recall': [recall],
                'f1': [f1]
            }

            self.df_metrics = pd.DataFrame(data)

            return self.cm, self.df_metrics
        
        except Exception as e:
            logger.error('[ERROR] Params are None. Remember to define them')




