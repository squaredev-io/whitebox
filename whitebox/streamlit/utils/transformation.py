import pandas as pd
from pandas.api.types import is_datetime64_any_dtype


def convert_drift_timeseries_dict_to_pd(timeseries_dict):
    df = pd.DataFrame.from_dict(timeseries_dict, orient="index")
    df = df.reset_index()
    df["index"] = pd.to_datetime(df["index"])

    return df


def export_drift_timeseries_from_dict(drift):
    timeseries_value = {}
    timeseries_drift = {}
    for i in range(len(drift)):
        drift_by_columns = drift[i]["data_drift_summary"]["drift_by_columns"]
        temp_col_value_dict = {}
        temp_col_drift_dict = {}
        for j in drift_by_columns.keys():
            temp_col_value_dict[j] = drift_by_columns[j]["drift_score"]
            temp_col_drift_dict[j] = drift_by_columns[j]["drift_detected"]

        timeseries_value[drift[i]["timestamp"]] = temp_col_value_dict
        timeseries_drift[drift[i]["timestamp"]] = temp_col_drift_dict

    value_df = convert_drift_timeseries_dict_to_pd(timeseries_value)
    drift_df = convert_drift_timeseries_dict_to_pd(timeseries_drift)

    return value_df, drift_df


def get_dataframe_from_regression_performance_dict(performance_dict):
    df = pd.DataFrame(performance_dict)
    df = df[["r_square", "mean_squared_error", "mean_absolute_error", "timestamp"]]
    return df


def get_dataframe_from_classification_performance_dict(performance_dict):
    timeseries = {}
    for i in range(len(performance_dict)):
        acc = performance_dict[i]["accuracy"]
        prec = performance_dict[i]["precision"]["macro"]
        rec = performance_dict[i]["recall"]["macro"]
        f1 = performance_dict[i]["f1"]["macro"]
        timeseries[performance_dict[i]["timestamp"]] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
        }

    performance_df = pd.DataFrame.from_dict(timeseries, orient="index").reset_index()
    performance_df["index"] = pd.to_datetime(performance_df["index"])

    performance_df = performance_df.rename({"index": "timestamp"}, axis=1)
    return performance_df


def adjust_inference_column_positions(inf_df, target_column):
    df_columns = inf_df.columns
    # Find only the feature columns
    df_feature_columns = df_columns.drop([target_column, "timestamp", "id", "actual"])
    # Inser the id and timestamp in front positions
    df_adj_columns = df_feature_columns.insert(0, "id")
    df_adj_columns = df_adj_columns.insert(1, "timestamp")
    # Append target column and actual column
    df_adj_columns = df_adj_columns.to_list()
    df_adj_columns.append(target_column)
    df_adj_columns.append("actual")

    return inf_df.reindex(columns=df_adj_columns)


def convert_inference_dict_to_df(inf_dict, target_column):
    temp_full_dict = {}
    for i in range(len(inf_dict)):
        temp_row_dict = inf_dict[i]["nonprocessed"]
        temp_row_dict["timestamp"] = inf_dict[i]["timestamp"]
        temp_row_dict["id"] = inf_dict[i]["id"]
        temp_row_dict["actual"] = inf_dict[i]["actual"]

        temp_full_dict[i] = temp_row_dict

    inf_df = pd.DataFrame.from_dict(temp_full_dict, orient="index")
    return adjust_inference_column_positions(inf_df, target_column)


def get_recent_alert(alerts_df):
    """
    Function that gets alerts dataframe and results on the
    most recent alert row for each unique id
    """
    alerts_df["timestamp"] = pd.to_datetime(alerts_df["timestamp"])

    # datetime with no timezone
    if is_datetime64_any_dtype(alerts_df["timestamp"]):
        alerts_df["timestamp"] = alerts_df["timestamp"].dt.tz_localize(None)

    # sort the dataframe by 'date' column in descending order
    alerts_df = alerts_df.sort_values(by="timestamp", ascending=False)
    # drop duplicates based on 'id' column, keeping only the first occurrence (most recent date)
    alerts_df = alerts_df.drop_duplicates(subset="model_monitor_id", keep="first")

    return alerts_df.reset_index(drop=True)


def combine_monitor_with_alert_for_alerts(monitor_df, alert_df):

    merged_df = pd.merge(
        monitor_df[["id", "metric", "name"]],
        alert_df[["model_monitor_id", "timestamp", "description"]],
        how="right",
        left_on="id",
        right_on="model_monitor_id",
    )
    return merged_df


def combine_monitor_with_alert_for_monitors(monitor_df, alert_df):
    merged_df = pd.merge(
        monitor_df,
        alert_df[["model_monitor_id", "description"]],
        how="left",
        left_on="id",
        right_on="model_monitor_id",
    )
    return merged_df
