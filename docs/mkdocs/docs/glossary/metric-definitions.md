# Metric Definitions

## Descriptive metrics

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


