import pandas as pd
import seaborn as sns


def desriptive_statistics_plot(report, timestep):
    df = pd.DataFrame.from_dict(report[timestep]["feature_metrics"])
    df = df.drop(["target"])
    df["class"] = df.index
    df_pivot = pd.melt(df, id_vars="class", var_name="statistics", value_name="value")
    gfg = sns.catplot(
        x="statistics",
        y="value",
        hue="class",
        data=df_pivot,
        kind="bar",
        orient="v",
        aspect=7 / 3,
        palette="Spectral",
    )
    sns.set_theme(style="whitegrid")
    gfg.set(
        xlabel="",
        ylabel="",
        title="Descriptive Statistics for "
        + report[timestep]["timestamp"].strip("T00:00:00"),
    )

    return gfg
