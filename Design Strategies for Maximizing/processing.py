#!/usr/bin/env python
# coding: utf-8


"""
This code was developed to help researchers to process data.
------
Author: Jinseok Kim (Ph.D.),
        Research Assistant Professor at Survey Research Center, Institute for Social Research,
        and School of Information, University of Michigan - Ann Arbor
Date: 12/08/2021

Packages required to be installed: numpy, pandas, and sklearn
"""

import numpy as np
import pandas as pd
from sklearn import preprocessing


def ignore_future_warnings():

    """ 
    Silent future warnings while running packages
    """

    ''' import warnings filter '''
    from warnings import simplefilter

    ''' ignore all future warnings '''
    simplefilter(action = 'ignore', category = FutureWarning)
    
''' run the defined function '''
ignore_future_warnings()


def convert_values(input_df, column_name = None, method = None):
    
    """
    This converts values into another values as defined by a method
    Parameters
    ------
    input_df: a pandas dataframe object
    column_name_list: a column name to convert values
    method: a name string of a value converter
            Five methods are available
            'label_binarizer', 'normalizer', 'standard_scaler', 'min_max_scaler', 'power_transformer'
            For details on each method and parameters, follow the link under each method shown below.
            To add other methods, see a link below.
            https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing
    
    Returns
    ------
    a pandas dataframe in which values in a column are converted according to a method
        Note: this function replaces values in original column (i.e., inplace=True)
    """
    
    ''' invoke a converting method and initialize it using default settings '''
    if   method == 'label_binarizer':
        converter = preprocessing.LabelBinarizer()
        # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelBinarizer.html#sklearn.preprocessing.LabelBinarizer
        
    elif method == 'normalizer':
        converter = preprocessing.Normalizer()
        # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html#sklearn.preprocessing.Normalizer
       
    elif method == 'standard_scaler':
        converter = preprocessing.StandardScaler()
        # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html#sklearn.preprocessing.StandardScaler
    
    elif method == 'min_max_scaler':
        converter = preprocessing.MinMaxScaler()
        # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler
        
    elif method == 'power_transformer':
        converter = preprocessing.PowerTransformer()
        # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PowerTransformer.html#sklearn.preprocessing.PowerTransformer
    
    ''' convert values by a converting method '''
    input_df[column_name] = converter.fit_transform(np.array(input_df[column_name]).reshape(-1, 1))
    
        
    return input_df


def encode_column(input_df, column_name_list, method=None, ordered_categories=None):
    
    """
    This appends encoded columns to input datdaframe and delete before-encoded columns.
    ------
    :param input_df: a pandas dataframe object
    :param column_name_list: a list ([])of column names to encode
    ------
    :return: a pandas dataframe in which a list of columns is one-hot-encoded
             into N (no. of categories in the columns to encode) columns and
             before-encoded columns are deleted
    """
    
    def _encode_column_ohe(input_df, column_name_list):
    
        """
        This encodes categorical vlaues in a column into an array of columns (a.k.a. one-hot-encoding).
        Parameters
        ------
        input_df: a pandas dataframe object
        column_name_list: a list ([]) of column names to encode

        Returns
        ------
        a pandas dataframe in which a column is one-hot-encoded
                 into N (no. of categories in the column to encode) columns
        an array of categories used in encoding
        """

        ''' initialized an encoder '''

        encoder = preprocessing.OneHotEncoder(sparse=False)
            # For details, https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html

        ''' transform column(s) into an array of encoded values ''' 
        encoded_column = encoder.fit_transform(input_df[column_name_list])
            # if OneHotEncoder(sparse=True), .toarray() needs to be added

        ''' get feature names for encoded array '''
        encoded_column_names = encoder.get_feature_names_out()
            # feature names are alphabetically ordered by scikit learn
            # added for future use (e.g., printing encoded columns)

        ''' create a pandas dataframe using the encoded array and feature names '''
        encoded_df = pd.DataFrame(encoded_column, columns = encoded_column_names )

        ''' get an array of category names used for encoding '''
        encoded_categories = encoder.categories_

        return encoded_df, encoded_categories
    
    def _encode_column_ord(input_df, column_name_list, ordered_categories):
    
        """
        This encodes categorical vlaues into an ordinal ones
        Parameters
        ------
        input_df: a pandas dataframe object
        column_name_list: a list ([]) of column names to encode
        ordered_categories: an array of categories ordered ascendingly in importance or weights 
            e.g., if two columns are encoded, the input array looks like this
            ordered_categories = [['Preschool', '1st-4th', '5th-6th', '7th-8th', '9th', '10th',
                                   '11th', '12th', 'HS-grad', 'Prof-school','Assoc-voc',
                                   'Assoc-acdm', 'Some-college', 'Bachelors', 'Masters','Doctorate'],
                                  ['White','Black','Asian-Pac-Islander','Amer-Indian-Eskimo','Other']]

        Returns
        ------
        a pandas dataframe in which a column is encoded
        an array of categories used in encoding
        """

        ''' initialized an encoder '''
        if ordered_categories is None:
            encoder = preprocessing.OrdinalEncoder()
                # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html
        else:
            encoder = preprocessing.OrdinalEncoder(categories=ordered_categories)

        ''' transform column(s) into an array of encoded values ''' 
        encoded_column = encoder.fit_transform(input_df[column_name_list])

        ''' create a pandas dataframe using the encoded array and feature names '''
        encoded_df = pd.DataFrame(encoded_column, columns = column_name_list)

        ''' get an array of category names used for encoding '''
        encoded_categories = encoder.categories_

        return encoded_df, encoded_categories
    
    
    
    ''' create a dataframe of encoded columns '''
    if method == 'ohe':
        encoded_df, encoded_categories = _encode_column_ohe(input_df, column_name_list)
    elif method == 'ord':
        encoded_df, encoded_categories = _encode_column_ord(input_df, column_name_list, ordered_categories)
    
    ''' drop columns which encoded columns are created from '''
    df_copy = input_df.copy()
    df_copy.drop(columns = column_name_list, inplace=True)

    ''' add encoded dataframe to input dataframe '''
    df_merged = pd.merge(df_copy, encoded_df, left_index=True, right_index=True, how='left')

    return df_merged, encoded_categories
    


""" print a dataframe """
def print_dataframe (input_df, file_name):
    
    """
    Parameters
    ----------
    input_df: a pandas dataframe to print
    file_name: a name string of an output file; contains a file extension
        e.g., "output_file_name.csv"

    Returns
    -------
    A message indicating that a file is created on the current working directory
    An output file that records the input_df 
    """
    
    ''' create a copy of input dataframe '''
    df_print = input_df.copy()

    ''' set indices as a column '''
    df_print.reset_index(inplace=True)

    ''' print the copied dataframe to a file '''
    df_print.to_csv(file_name, sep=",", encoding="utf-8", index=False)
        # for more options, see https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html

    ''' print a message notifying that a file has been created '''
    print("\nAn output file '" + file_name + "' has been created!\n")


def compare_dataframes (df_pre, df_pos, column_name_list = None, print_or_not = None):
    
    """
    Parameters
    ----------
    df_pre: a pandas dataframe before changes are applied
    df_pos: a pandas dataframe after changes are applied 
    column_name: a list of column names to be compared for changes
    print_or_not: any non-null value to indicate printing; None = no printing
    
    Returns
    -------
    A string message indicating that differences between two dataframes exist (or not <<< if print is turned on)
    if any differences are found: a pandas Series report of counts of total, same, and
                different values with, if needed, a percentage (%) of different values over total values
    df_merged: (1) a pandas dataframe that record differences
               (2) if print_or_not is not None, an output file of df_merged 
    """
    
    """ compare indices between dataframes """
    def _compare_indices(df_pre, df_pos, column_name):
        
        ''' combine two dataframes to compare '''
        df_combined = pd.merge(df_pre[column_name], df_pos[column_name],
                               left_index=True, right_index=True, how='outer',
                               indicator=True, suffixes=('_pre', '_pos'))
        
        ''' split combined dataframe into subsets '''
        df_both, df_only = df_combined.query("_merge == 'both'"), df_combined.query("_merge != 'both'")
            # df_both contains rows that exist in both dataframes
            # df_only contains rows that exist in one of dataframes but not in the other
        
        ''' create a tuple of column names with suffixes '''
        left_col_name, right_col_name = str(column_name) + "_pre", str(column_name) + "_pos"
        
        return df_both, df_only, (left_col_name, right_col_name)
                                                                                
   
    """ compare value differences in a column """
    def _compare_columnwise(df_both, col_names):
        
        ''' create a copy of input dataframe '''
        df_copy =df_both.copy()
        
        ''' create an empty pd.Series report '''
        report = pd.Series([''], index=[''], name='Report')
        
        ''' unless input dataframe is empty '''
        if len(df_copy) > 0:
        
            ''' get a list of indices of rows where different values exist between dataframes '''
            index_list = df_copy.loc[df_copy[col_names[0]].isin(df_copy[col_names[1]])==False].index

            ''' count same, different, and total values ''' 
            count_diff, count_total = len(index_list), len(df_copy)
            count_same = count_total - count_diff

            ''' calculate percentage of different values over total values '''
            percentage = f'{count_diff / count_total: .2%}'

            ''' create a pd.Series report of counts and percentage '''
            report = pd.Series([col_names, count_total, count_same, count_diff, percentage],
                               index=['Compared Columns', 'Value Total', 'Same Value', 'Diff Value', 'Diff %'],
                               name='Report')
        
            ''' filter rows that contain different values between dataframes '''
            df_copy = df_copy.loc[index_list].replace(np.nan, '_NaN_')
                # replace np.nan with '_NaN_' for a reporting purpose
        
        ''' drop '_merge' column '''
        df_copy.drop(columns='_merge', inplace=True)
        
        return df_copy, report
        
   
    def _compare_rowwise(df_only, col_names):
        
        ''' create a copy of input dataframe '''
        df_copy = df_only.copy()
        
        ''' create an empty pd.Series report '''
        report = pd.Series([''], index=[''], name='Report')
       
        ''' unless input dataframe is empty '''
        if len(df_copy) > 0:

            ''' count dropped, added, and total rows ''' 
            count_drop   = len(df_copy[df_copy['_merge'].isin(['left_only' ])]) 
            count_append = len(df_copy[df_copy['_merge'].isin(['right_only'])])
            count_total  = len(df_copy)

            ''' create a pd.Series report of counts and percentage '''
            report = pd.Series([col_names, count_total, count_drop, count_append],
                               index=['Compared Columns', 'Rows Total', 'Dropped Rows', 'Appended Rows'],
                               name = 'Report')
            
            ''' replace np.nan '''
            df_copy.fillna({col_names[0]:'_NaN_', col_names[1]:'_DRP_'}, inplace=True)

        ''' drop '_merge' column '''
        df_copy.drop(columns='_merge', inplace=True)
        
        return df_copy, report
            
  
    """ implement a main function """
    def _compare_main_(df_pre, df_pos, column_name):
        
        ''' merge and split two dataframes into 'union (-> both)' set and 'either (-> only)' set '''
        df_both, df_only, col_names = _compare_indices(df_pre, df_pos, column_name)
        
        ''' create a dataframe and a report for the union set '''
        df_diff_both, report_both = _compare_columnwise(df_both, col_names)
        
        ''' create a dataframe and a report for the either set '''
        df_diff_only, report_only = _compare_rowwise(df_only, col_names)
            
        df_appended = df_diff_both.append(df_diff_only).sort_index()
        
        ''' if any value difference is not found '''
        if len(df_appended) == 0:
            
            ''' print a message '''
            #print("\nDifferent values not found between dataframes in the column '" + str(column_name) + "'.\n")
            
            return df_appended

        else:
            
            ''' if columnwise difference exists '''
            if len(df_diff_both) > 0:
                ''' print a report '''
                print("\nCompared columns have different values for the same rows.\n")
                print(report_both)
            
            ''' if rowwise difference exists '''
            if len(df_diff_only) > 0:
                print("\nCompared columns have different row sizes.\n")
                print(report_only)
           
            return df_appended
        
    
    ''' a column name list is not given '''
    if column_name_list is None:
         
        ''' creat and sort a list of column names common in two dataframes '''
        column_name_list = list(set(df_pre.columns.to_list()).intersection(df_pos.columns.to_list()))
        column_name_list.sort()
        
    ''' create an empty dataframe to contain output '''
    df_merged = pd.DataFrame()

    ''' iterate main function for each column name '''
    for column_name in column_name_list:
        
        ''' create a dataframe that contains differences between dataframes in the column '''
        df_diff = _compare_main_(df_pre, df_pos, column_name)
        
        ''' if any difference is found '''
        if len(df_diff) > 0:
            
            ''' add the dataframe to the existing df_merged '''
            df_merged = pd.merge(df_merged, df_diff, left_index=True, right_index=True, how='outer')

    if print_or_not is not None:

        ''' write a file name for output '''
        file_name = "list of different values in two dataframes.csv"
            # Note: current file exetention is '.csv'
        
        ''' produce an output file in the current working directory '''
        print_dataframe(df_merged, file_name)

    return df_merged

