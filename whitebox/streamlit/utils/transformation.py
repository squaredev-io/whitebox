import pandas as pd


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
