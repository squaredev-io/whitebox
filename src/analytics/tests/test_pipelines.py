import pytest
from src.analytics.metrics.pipelines import *
from src.analytics.drift.pipelines import *
from src.analytics.models.pipelines import *
from src.analytics.xai_models.pipelines import *
from unittest import TestCase
from sklearn.datasets import fetch_california_housing
from sklearn.datasets import load_breast_cancer, load_wine

test_metrics_df = pd.read_csv("src/analytics/data/testing/metrics_test_data.csv")
test_classification_df = pd.read_csv(
    "src/analytics/data/testing/classification_test_data.csv"
)
drift_data = fetch_california_housing(as_frame=True)
drift_data = drift_data.frame
reference = drift_data.head(500)
current = drift_data.iloc[1000:1200]
reference_concept_drift = test_classification_df.head(5)
current_concept_drift = test_classification_df.tail(5)
concept_drift_detected_dataset = pd.read_csv(
    "src/analytics/data/testing/udemy_fin_adj.csv"
)
reference_concept_drift_detected = concept_drift_detected_dataset.head(1000)
current_concept_drift_detected = concept_drift_detected_dataset.tail(1000)
df_load_binary = load_breast_cancer()
df_binary = pd.DataFrame(df_load_binary.data, columns=df_load_binary.feature_names)
df_binary["target"] = df_load_binary.target
df_binary_inference=df_binary.drop(columns=['target'])
df_binary_inference=df_binary_inference.tail(10)
df_load_multi = load_wine()
df_multi = pd.DataFrame(df_load_multi.data, columns=df_load_multi.feature_names)
df_multi["target"] = df_load_multi.target
df_multi_inference=df_multi.drop(columns=['target'])
df_multi_inference=df_multi_inference.tail(10)


class TestNodes:
    def test_create_feature_metrics_pipeline(self):
        features_metrics = dict(create_feature_metrics_pipeline(test_metrics_df))
        missing_count = features_metrics["missing_count"]
        non_missing_count = features_metrics["non_missing_count"]
        mean = features_metrics["mean"]
        minimum = features_metrics["minimum"]
        maximum = features_metrics["maximum"]
        sum = features_metrics["sum"]
        standard_deviation = features_metrics["standard_deviation"]
        variance = features_metrics["variance"]
        TestCase().assertDictEqual(
            {"num1": 1, "num2": 2, "num3": 0, "cat1": 1, "cat2": 2}, missing_count
        )
        TestCase().assertDictEqual(
            {"num1": 9, "num2": 8, "num3": 10, "cat1": 9, "cat2": 8}, non_missing_count
        )
        TestCase().assertDictEqual(
            {"num1": 156.33333333333334, "num2": 9.223817500000001, "num3": 1.0}, mean
        )
        TestCase().assertDictEqual({"num1": 0.0, "num2": 0.00054, "num3": 0.0}, minimum)
        TestCase().assertDictEqual(
            {"num1": 1000.0, "num2": 45.896, "num3": 2.0}, maximum
        )
        TestCase().assertDictEqual(
            {"num1": 1407.0, "num2": 73.79054000000001, "num3": 10.0}, sum
        )
        TestCase().assertDictEqual(
            {
                "num1": 322.0283372624217,
                "num2": 15.488918075768835,
                "num3": 0.816496580927726,
            },
            standard_deviation,
        )
        TestCase().assertDictEqual(
            {
                "num1": 103702.25000000001,
                "num2": 239.90658315787854,
                "num3": 0.6666666666666666,
            },
            variance,
        )

    def test_create_binary_classification_evaluation_metrics_pipeline(self):
        binary_metrics = dict(
            create_binary_classification_evaluation_metrics_pipeline(
                test_classification_df["y_testing_binary"],
                test_classification_df["y_prediction_binary"],
            )
        )

        assert binary_metrics["accuracy"] == 0.6
        assert binary_metrics["precision"] == 0.6
        assert binary_metrics["recall"] == 0.6
        assert binary_metrics["f1"] == 0.6
        assert binary_metrics["true_negative"] == 3
        assert binary_metrics["false_positive"] == 2
        assert binary_metrics["false_negative"] == 2
        assert binary_metrics["true_positive"] == 3

    def test_create_multiple_classification_evaluation_metrics_pipeline(self):
        multi_metrics = create_multiple_classification_evaluation_metrics_pipeline(
            test_classification_df["y_testing_multi"],
            test_classification_df["y_prediction_multi"],
        )
        assert multi_metrics.accuracy == 0.6

        TestCase().assertDictEqual(
            {"micro": 0.6, "macro": 0.6444444444444445, "weighted": 0.64},
            multi_metrics.precision.dict(),
        )
        TestCase().assertDictEqual(
            {"micro": 0.6, "macro": 0.5833333333333334, "weighted": 0.6},
            multi_metrics.recall.dict(),
        )
        TestCase().assertDictEqual(
            {"micro": 0.6, "macro": 0.6, "weighted": 0.6066666666666667},
            multi_metrics.f1.dict(),
        )
        TestCase().assertDictEqual(
            {
                "true_negative": 5,
                "false_positive": 2,
                "false_negative": 2,
                "true_positive": 1,
            },
            multi_metrics.confusion_matrix["class0"].dict(),
        )
        TestCase().assertDictEqual(
            {
                "true_negative": 4,
                "false_positive": 2,
                "false_negative": 1,
                "true_positive": 3,
            },
            multi_metrics.confusion_matrix["class1"].dict(),
        )
        TestCase().assertDictEqual(
            {
                "true_negative": 7,
                "false_positive": 0,
                "false_negative": 1,
                "true_positive": 2,
            },
            multi_metrics.confusion_matrix["class2"].dict(),
        )

    def test_create_data_drift_pipeline(self):
        data_drift_report = dict(run_data_drift_pipeline(reference, current))
        assert data_drift_report["number_of_columns"] == 9
        assert data_drift_report["number_of_drifted_columns"] == 7
        assert (
            round(
                dict(data_drift_report["drift_by_columns"]["Population"])[
                    "drift_score"
                ],
                2,
            )
            == 0.06
        )
        assert (
            dict(data_drift_report["drift_by_columns"]["Longitude"])["drift_detected"]
            == True
        )
        assert (
            dict(data_drift_report["drift_by_columns"]["AveBedrms"])["drift_detected"]
            == False
        )

    def test_create_concept_drift_pipeline_drift_not_detected(self):
        concept_drift_report = run_concept_drift_pipeline(
            reference_concept_drift, current_concept_drift, "y_testing_multi"
        )
        assert list(concept_drift_report.keys()) == [
            "timestamp",
            "concept_drift_summary",
        ]
        assert (
            round(concept_drift_report["concept_drift_summary"]["drift_score"], 3)
            == 0.082
        )
        assert concept_drift_report["concept_drift_summary"]["drift_detected"] == False
        assert (
            concept_drift_report["concept_drift_summary"]["column_name"]
            == "y_testing_multi"
        )

    def test_create_concept_drift_pipeline_drift_detected(self):
        concept_drift_report = run_concept_drift_pipeline(
            reference_concept_drift_detected,
            current_concept_drift_detected,
            "discount_price__currency",
        )
        assert list(concept_drift_report.keys()) == [
            "timestamp",
            "concept_drift_summary",
        ]
        assert (
            round(concept_drift_report["concept_drift_summary"]["drift_score"], 3)
            == 0.008
        )
        assert concept_drift_report["concept_drift_summary"]["drift_detected"] == True
        assert (
            concept_drift_report["concept_drift_summary"]["column_name"]
            == "discount_price__currency"
        )

    def test_create_binary_classification_training_model_pipeline(self):
        model, eval = create_binary_classification_training_model_pipeline(df_binary, "target")
        eval_score = eval["roc_auc_score"]
        assert (round(eval_score, 3)) == 0.986

    def test_create_multiclass_classification_training_model_pipeline(self):
        model, eval = create_multiclass_classification_training_model_pipeline(
            df_multi, "target"
        )
        eval_score = eval["precision"]
        assert (round(eval_score, 2)) == 0.97

    def test_create_xai_pipeline_classification(self):
        binary_class_report = create_xai_pipeline_classification(df_binary,"target",df_binary_inference,"binary_classification")
        multi_class_report = create_xai_pipeline_classification(df_multi,"target",df_multi_inference,"multiclass_classification")

        # TODO: Find a way to make the results of LIME reproducable. I added random state in the explainer but this didn't solve the problem.

        binary_contribution_check_one = binary_class_report["row0"]["worst perimeter"]
        binary_contribution_check_two = binary_class_report["row2"]['worst texture']
        multi_contribution_check_one = multi_class_report["row0"]["hue"]
        multi_contribution_check_two = multi_class_report["row9"]["proanthocyanins"]
        
        assert (len(binary_class_report)) == len(df_binary_inference)
        assert (len(multi_class_report)) == len(df_multi_inference)
        
        assert (round(binary_contribution_check_one, 3)) == 0.253
        assert (round(binary_contribution_check_two, 2)) == -0.09
        assert (round(multi_contribution_check_one, 2)) == -0.08
        assert (round(multi_contribution_check_two, 3)) == -0.023

