
from sklearn.metrics import multilabel_confusion_matrix
import pandas as pd
from typing import Dict, Union


def format_feature_metrics(missing_count:int,non_missing_count:int,mean:float,minimum:float,maximum:float,sum:float,standard_deviation:float,variance:float)->Dict[str,Union[int,float]]:
    formated_metrics={'missing_count':missing_count,'non_missing_count':non_missing_count,'mean':mean,'minimum':minimum,'maximum':maximum,'sum':sum,'standard_deviation':standard_deviation,'variance':variance}

    return formated_metrics


def format_evaluation_metrics_binary(accuracy:float, precision:float, recall:float, f1:float, tn:int, fp:int, fn:int, tp:int)->Dict[str,Union[int,float]]:
    formated_metrics_for_binary={'accuracy':accuracy,'precision':precision,'recall':recall,'f1':f1,'true_negative':tn,'false_positive':fp,'false_negative':fn,'true_positive':tp}

    return formated_metrics_for_binary


def confusion_for_multiclass(test_set:pd.DataFrame,prediction_set:pd.DataFrame)->Dict[str,Dict[str,int]]:
    cm=multilabel_confusion_matrix(test_set,prediction_set)
    mult_dict={}
    class_key=0
    for i in cm:
        tn, fp, fn, tp = i.ravel()
        eval_dict= {'true_negative':tn,'false_positive':fp,'false_negative':fn,'true_positive':tp}
        mult_dict['class{}'.format(class_key)]=eval_dict
        class_key=class_key+1
    return mult_dict


def format_evaluation_metrics_multiple(accuracy:float, precision_statistics:Dict[str,float], recall_statistics:Dict[str,float], f1_statistics:Dict[str,float], conf_matrix:Dict[str,Dict[str,int]])->Dict[str,Union[float,Dict[str,Union[int,float]]]]:
    formated_metrics_for_multiple={'accuracy':accuracy,'precision_statistics':precision_statistics,'recall_statistics':recall_statistics,'f1_statistics':f1_statistics,'multiple_confusion_matrix':conf_matrix}

    return formated_metrics_for_multiple