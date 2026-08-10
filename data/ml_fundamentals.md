# Machine Learning Fundamentals and Paradigms

## 1. Machine Learning Paradigms

Machine Learning (ML) algorithms learn patterns from data to perform tasks without being explicitly programmed. The primary paradigms are:

### 1.1 Supervised Learning
- **Concept**: The model is trained on labeled data consisting of input features $X$ and target outputs $Y$.
- **Sub-types**:
  - **Regression**: Predicting continuous numerical values (e.g., house prices, temperature). Common models include Linear Regression, Ridge/Lasso, Support Vector Regression (SVR), and Gradient Boosted Trees (XGBoost, LightGBM).
  - **Classification**: Predicting discrete class labels (binary or multi-class). Common models include Logistic Regression, Decision Trees, Random Forests, Support Vector Machines (SVM), Naive Bayes, and Neural Networks.
- **Loss Functions**: Mean Squared Error (MSE), Mean Absolute Error (MAE), Binary Cross-Entropy (Log Loss), Categorical Cross-Entropy.

### 1.2 Unsupervised Learning
- **Concept**: The model discovers hidden patterns or structural relationships in unlabeled data ($X$ only).
- **Key Tasks**:
  - **Clustering**: Grouping data points based on similarity. Algorithms include K-Means, Hierarchical Clustering, DBSCAN, and Gaussian Mixture Models (GMM).
  - **Dimensionality Reduction**: Compressing feature spaces while preserving maximum variance or local geometry. Techniques include Principal Component Analysis (PCA), t-SNE, and UMAP.
  - **Anomaly Detection**: Identifying rare data points (outliers). Methods include Isolation Forests, One-Class SVM, and Autoencoders.

### 1.3 Reinforcement Learning (RL)
- **Concept**: An agent interacts with an environment, taking actions $a$ from state $s$ to maximize cumulative reward $R$.
- **Key Components**: Policy $\pi(a|s)$, Value Function $V(s)$, Q-Function $Q(s, a)$, Environment Dynamics.
- **Algorithms**: Q-Learning, Deep Q-Networks (DQN), Proximal Policy Optimization (PPO), Deep Deterministic Policy Gradient (DDPG).

---

## 2. Bias-Variance Tradeoff

The total generalization error of a machine learning model decomposes into three components:

$$\text{Total Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}$$

- **High Bias (Underfitting)**: The model is too simple to capture underlying patterns. High error on both training and test sets.
  - *Remedies*: Increase model complexity, add feature interactions, decrease regularization.
- **High Variance (Overfitting)**: The model memorizes training noise and fails to generalize to unseen data. Low training error, high test error.
  - *Remedies*: Add regularization (L1/L2), get more data, use dropout, prune decision trees, perform feature selection.

---

## 3. Model Validation & Regularization

### 3.1 Cross-Validation
- **K-Fold Cross-Validation**: Splits data into $K$ equal folds. Trains on $K-1$ folds and validates on the remaining fold, repeating $K$ times to average performance.
- **Stratified K-Fold**: Preserves the percentage of samples for each class across folds, critical for imbalanced datasets.

### 3.2 Regularization Techniques
- **L1 Regularization (Lasso)**: Adds $\lambda \sum |w_i|$ penalty. Enforces sparsity, effectively performing automatic feature selection by driving weights to zero.
- **L2 Regularization (Ridge)**: Adds $\lambda \sum w_i^2$ penalty. Shrinks weights toward zero to prevent any single feature from dominating, smoothing decision boundaries.
- **ElasticNet**: Combines L1 and L2 penalties ($\alpha \text{L1} + (1-\alpha) \text{L2}$).
