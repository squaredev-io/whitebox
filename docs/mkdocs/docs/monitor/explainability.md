# Explainability

The target of the explainability feature is to provide a contribution score of each feature to each individual prediction, in a try to explain how the model concluded in the specific prediction. To achieve this we define 3 Levels of confidence in the explainability feature, based on how accessible or not is the client's input:

- **Level-0**: In this level a replacement model is trained in the same training data as client's model, and used for the explainability feature.
- **Level-1** (_pending_): In this level a surrogate model is trained in a way of trying to achieve the same predictions as client's model, and used for the explainability feature.
- **Level-2** (_pending_): Client's model is used for the explainability feature.

## Level-0 of confidence

At this level a replacement model is trained in the same training data as client's model, and used for the explainability feature. Below there is a table of used models per machine learning task.

| Model          | Task             |
| --------------- | ------------------| 
| <a href="/glossary/metric-definitions/#light-gradient-boosting-machine" class="external-link" target="_blank">**LightGBM**</a>      | `binary classification` & `multi-class classification`|
|     |  |
|     |  | 

The fine tuning of models, through a hyper-parameters exploration is a pending task for now. 

The trained model along with the inference data are used as input in <a href="/glossary/metric-definitions/#local-interpretable-model-agnostic-explanations" class="external-link" target="_blank">LIME</a> library, and the below report is provided - presenting the contribution of each feature in a specific prediction (the report includes all the feature contribution score to an descending order based on the absolute score value):

```
{
 'feature1': contribution score,
 'feature2': contribution score,
 'feature3': contribution score,
 ... 
}
```
## Level-1 of confidence (_pending_)

## Level-2 of confidence (_pending_)
