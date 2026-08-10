# Machine Learning Model Evaluation & Performance Metrics

## 1. Classification Evaluation Metrics

Classification models predict categorical outcomes. Evaluating them requires looking beyond simple accuracy, especially when dealing with imbalanced datasets.

### 1.1 Confusion Matrix Elements
- **True Positive (TP)**: Correctly predicted positive class.
- **True Negative (TN)**: Correctly predicted negative class.
- **False Positive (FP)**: Incorrectly predicted positive (Type I error).
- **False Negative (FN)**: Incorrectly predicted negative (Type II error).

### 1.2 Key Formulas
- **Accuracy**: 
  $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
- **Precision**: Proportion of positive predictions that were actually positive (crucial when false positives are expensive, e.g., spam detection).
  $$\text{Precision} = \frac{TP}{TP + FP}$$
- **Recall (Sensitivity / True Positive Rate)**: Proportion of actual positives correctly identified (crucial when false negatives are dangerous, e.g., cancer detection).
  $$\text{Recall} = \frac{TP}{TP + FN}$$
- **F1-Score**: Harmonic mean of Precision and Recall.
  $$\text{F1} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

### 1.3 ROC Curve and AUC
- **ROC Curve**: Plots True Positive Rate (TPR) against False Positive Rate ($\text{FPR} = \frac{FP}{FP+TN}$) across different classification probability thresholds.
- **ROC-AUC**: Area Under the ROC Curve. Ranges from 0.5 (random guessing) to 1.0 (perfect classification). Robust against class imbalance.

---

## 2. Regression Evaluation Metrics

Regression models predict continuous target variables $y_i$ with predicted values $\hat{y}_i$.

- **Mean Squared Error (MSE)**: Penalizes larger errors more heavily due to squaring.
  $$\text{MSE} = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2$$
- **Root Mean Squared Error (RMSE)**: Interpretable in the same units as the target variable.
  $$\text{RMSE} = \sqrt{\text{MSE}}$$
- **Mean Absolute Error (MAE)**: Average magnitude of absolute errors, less sensitive to extreme outliers than MSE.
  $$\text{MAE} = \frac{1}{n} \sum_{i=1}^n |y_i - \hat{y}_i|$$
- **R-squared ($R^2$ Score / Coefficient of Determination)**: Proportion of variance in the target variable explained by the model features.
  $$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$

---

## 3. Clustering Evaluation Metrics

Unsupervised clustering models are evaluated without ground truth labels using intrinsic geometric properties:

- **Silhouette Coefficient**: Measures how similar an object is to its own cluster compared to other clusters. Values range from -1 (poor clustering) to +1 (dense, well-separated clusters).
- **Davies-Bouldin Index**: Measures average similarity between each cluster and its most similar one. Lower values indicate better separation.
- **Inertia (Within-Cluster Sum of Squares)**: Used in K-Means to pick optimal $K$ via the Elbow Method.
