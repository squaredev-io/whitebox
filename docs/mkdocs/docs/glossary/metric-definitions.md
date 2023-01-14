# Metric Definitions

## Descriptive statistics

### Missing values
Missing values metric calculates the summary of the number of missing values per feature. Missing values include `NaN` in numeric arrays, `NaN` or `None` in object arrays and `NaT` in datetimelike.

### Non-Missing values
Non-Missing values metric calculates the summary of the number of non-missing values per feature. Non-Missing values are all values beside `NaN` for numeric arrays, `NaN` or `None` for object arrays and `NaT` for datetimelike.

### Mean or Average value
Returns the average value per feature excluding `NaN` and `null` values.

### Minimum value
Returns the minimum value per feature.

### Maximum value
Returns the maximum value per feature.

### Summary
Returns the summary of the values per feature. Excludes `NaN` and `null` values during calculations.

### Standard Deviation
Returns the sample standard deviation per feature normalized by N-1 excluding `NaN` and `null` values during calculations. Formula:

$$ 
σ = \sqrt{Σ(x_i-μ)^2 \over Ν-1}
$$

### Variance
Returns the unbiased variance per feature normalized by N-1 excluding `NaN` and `null` values during calculations. Formula:

$$ 
σ^2 = {Σ(x_i-μ)^2 \over Ν-1}
$$

## Evaluation metrics

### Confusion Matrix
Returns the number of TP, TN, FP and FN. In case of a `multi-class classification` returns the number of TP, TN, FP and FN per class.

A typical example for `binary classification` could be seen below in which:

- 20 observations were correctly classified as positive.
- 10 observations were incorrectly classified as negative while they were actually positive.
- 5 observations were incorrectly classified as positive while they were actually negative.
- 75 observations were correctly classified as negative.

|               | Predicted Positive | Predicted Negative |
|----------------|--------------------|--------------------|
| Actual Positive |         20  *(TP)*       |         10 *(FN)*        |
| Actual Negative |         5 *(FP)*          |         75 *(TN)*         |

A typical example for `multi-class classification` could be seen below in which:

- 15 observations were correctly classified as Class A.
- 5 observations were incorrectly classified as Class B while they were actually Class A.
- 2 observations were incorrectly classified as Class C while they were actually Class A.
- 4 observations were incorrectly classified as Class A while they were actually Class B.
- 20 observations were correctly classified as Class B.
- 3 observations were incorrectly classified as Class C while they were actually Class B.
- 2 observations were incorrectly classified as Class A while they were actually Class C.
- 8 observations were incorrectly classified as Class B while they were actually Class C.
- 25 observations were correctly classified as Class C.

|               | Predicted Class A | Predicted Class B | Predicted Class C |
|----------------|--------------------|--------------------|--------------------|
| Actual Class A |         15 *(TP_A)*         |          5        |         2         |
| Actual Class B |         4         |         20 *(TP_B)*        |         3         |
| Actual Class C |         2          |         8         |         25 *(TP_C)*        |

### Accuracy
Returns the accuracy classification score. In `multi-class classification`, this function computes subset accuracy: the set of labels predicted for a sample must exactly match the corresponding set of labels in y_true. Formula:

$$ 
accuracy = {(TP + TN) \over (TP + TN + FP + FN)}
$$

### Precision
Returns the precision classification score. In `multi-class classification`, returns the below 3 scores:

- `micro`: Calculate metrics globally by counting the total true positives, false negatives and false positives.
- `macro`: Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
- `weighted`: Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). This alters ‘macro’ to account for label imbalance; it can result in an F-score that is not between precision and recall.

Formula:

$$ 
precision = {TP \over (TP + FP)}
$$

### Recall
Returns the recall classification score. In `multi-class classification`, returns the below 3 scores:

- `micro`: Calculate metrics globally by counting the total true positives, false negatives and false positives.
- `macro`: Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
- `weighted`: Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). This alters ‘macro’ to account for label imbalance; it can result in an F-score that is not between precision and recall.

Formula:

$$ 
recall = {TP \over (TP + FN)}
$$

### F1 score
Returns the f1 classification score. In `multi-class classification`, returns the below 3 scores:

- `micro`: Calculate metrics globally by counting the total true positives, false negatives and false positives.
- `macro`: Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
- `weighted`: Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). This alters ‘macro’ to account for label imbalance; it can result in an F-score that is not between precision and recall.

Formula:

$$ 
F1 = 2 * {(precision * recall) \over (precision + recall)}
$$

## Statistical tests and techniques

### Kolmogorov-Smirnov Two Sample test
When there are two datasets then K-S two sample test can be used to test the agreement between their distributions. The null hypothesis states that there is no difference between the two distributions. Formula:

$$ 
D = Max|{F_a(X)-F_b(X)}| 
$$

where:

- $a$ = observations from first dataset.
- $b$ = observations from second dataset.
- $F_n(X)$ = observed cumulative frequency distribution of a random sample of n observations.

### Chi-squared test
A chi-square test is a statistical test used to compare 2 datasets. The purpose of this test is to determine if a difference between data of 2 datasets is due to chance, or if it is due to a relationship between the variables you are studying. Formula:

$$ 
x^2 = Σ{(O_i - E_i)^2 \over E_i}
$$

where:

- $x^2$ = chi-square
- $O_i$ = 1st dataset values
- $E_i$ = 2nd dataset values

### Z-score for independent proportions
The purpose of the z-test for independent proportions is to compare two independent datasets. Formula:

$$ 
Z = {p_1 - p_2 \over \sqrt{p'  q' ({1\over n_1} + {1\over n_2})}}
$$

where:

- $Z$ = Z-statistic which is compared to the standard normal deviate
- $p_1 , p_2$ = two datasets proportions
- $p'$ = estimated true proportion under the null hypothesis
- $q'$ = $(1-p')$
- $n_1 , n_2$ = number of observations in two datasets

### Wasserstein distance
The Wasserstein distance is a metric to describe the distance between the distributions of 2 datasets. Formula:

$$ 
W = ({\int_0^1}{{|{F_A}^{-1}(u) - {F_B}^{-1}(u)|}^2 du} )^{0.5}
$$

where:

- $W$ = Wasserstein distance
- $F_A , F_B$ = corresponding cumulative distribution functions of two datasets
- ${F_A}^{-1} , {F_B}^{-1}$ = respective quantile functions

### Jensen–Shannon divergence
The Jensen–Shannon divergence is a method of measuring the similarity between two probability distributions. Formula:

$$ 
JS = 1/2 * KL(P || M) + 1/2 * KL(Q || M)
$$

where:

- $JS$ = Jensen–Shannon divergence
- $KL$ = Kullback-Leibler divergence: $– sum x$ in $X$ $P(x)$ * $log(Q(x) / P(x))$
- $P,Q$ = distributions of 2 datasets
- $M$ = ${1 \over 2} * (P+Q)$
