# -*- coding: utf-8 -*-

from cgitb import reset
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier,VotingClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


def data_preprocess(file):
    #資料空值處理 性別編碼轉換
    df=pd.read_excel('./app/data/'+file)
    df = df.dropna(axis=0,how ='any') #清除空值行
    df["gender"] = df["gender"].replace(["M","F"],[0,1])
    #去除非必要特徵
    df_drop_unnecessary = df.drop(["id", "Index","sending date","check date","birth date","aid"], axis=1)
    return df_drop_unnecessary


# RFE Vot
def RFE_Vot_acc(delete_list,df_drop_unnecessary):
  df_AccTest = df_drop_unnecessary.drop(labels=['groupno'],axis=1)
  RFE_acc = []
  for i in range(len(delete_list)):
    #取得data & label
    data = df_AccTest.values # 移除Species並取得剩下欄位資料
    label = df_drop_unnecessary['groupno'].values
    le = LabelEncoder()
    label = le.fit_transform(label)
    #資料標準化
    scaler = StandardScaler().fit(data)
    X_scaledS = scaler.transform(data)
    #切分資料集與訓練集
    X_train, X_test, y_train, y_test = train_test_split(X_scaledS, label, test_size=0.1, random_state=42, stratify=label) #資料打散分群
    # 建立 voting 模型
    clf1 = XGBClassifier(n_estimators=100, learning_rate= 0.3)
    clf2 = RandomForestClassifier(n_estimators=9, random_state=1)
    clf3 = LGBMClassifier()
    ve= VotingClassifier(estimators=[('xg', clf1),('rf', clf2),('lgbm', clf3)],voting='hard')
    # 使用訓練資料訓練模型
    ve.fit(X_train, y_train)
    #存入準確率
    RFE_acc.append(round(ve.score(X_test,y_test),4))
    #去除最小影響特徵
    df_AccTest = df_AccTest.drop([delete_list[i][0]], axis=1)
  RFE_acc.reverse()
  return RFE_acc


def get_delete_list_cat(df_drop_unnecessary):
    data = df_drop_unnecessary.drop(labels=['groupno'],axis=1).values # 移除Species並取得剩下欄位資料
    label = df_drop_unnecessary['groupno'].values
    le = LabelEncoder()
    label = le.fit_transform(label)

    RFECAT_estimator = CatBoostClassifier(iterations=300,learning_rate=0.3 )
    RFECAT_selector = RFE(RFECAT_estimator, n_features_to_select=1, step=1) # n_features_to_select 最後保留的特徵數 step 每次刪減多少個特徵
    RFECAT_selector = RFECAT_selector.fit(data, label, verbose=False)

    delete_list_CAT = np.stack((df_drop_unnecessary.drop(labels=['groupno'],axis=1).columns, RFECAT_selector.ranking_), axis=1) 
    delete_list_CAT = sorted(delete_list_CAT, key = lambda s: s[1],reverse = True)

    return delete_list_CAT

def get_delete_list_RF(df_drop_unnecessary):
    data = df_drop_unnecessary.drop(labels=['groupno'],axis=1).values # 移除Species並取得剩下欄位資料
    label = df_drop_unnecessary['groupno'].values
    le = LabelEncoder()
    label = le.fit_transform(label)

    RFECAT_estimator = RandomForestClassifier(n_estimators=100, criterion = 'gini')
    RFECAT_selector = RFE(RFECAT_estimator, n_features_to_select=1, step=1) # n_features_to_select 最後保留的特徵數 step 每次刪減多少個特徵
    RFECAT_selector = RFECAT_selector.fit(data, label)

    delete_list_RF = np.stack((df_drop_unnecessary.drop(labels=['groupno'],axis=1).columns, RFECAT_selector.ranking_), axis=1) 
    delete_list_RF = sorted(delete_list_RF, key = lambda s: s[1],reverse = True)

    return delete_list_RF

def RFE_acc_print(RFE_acc,delete_list_CAT):
    delete_list_CAT.reverse() 
    result1 = "最佳準確度之特徵數量: " + str(RFE_acc.index(max(RFE_acc))+1) 
    result2 = "最佳準確度之特徵: " 

    for i in range(RFE_acc.index(max(RFE_acc))+1):
        result2 = result2 + " " + delete_list_CAT[i][0]
    
    result3  = "最佳準確度: " + str(max(RFE_acc))

    return result1 , result2 , result3


def result(file):
    df_drop_unnecessary = data_preprocess(file)
    delete_list_RF = get_delete_list_RF(df_drop_unnecessary)
    RFE_acc = RFE_Vot_acc(delete_list_RF,df_drop_unnecessary)
    return RFE_acc_print(RFE_acc,delete_list_RF)

#if __name__ == "__main__":
 #   result('./app/data/cleanresultV4_20210602.xlsx')
