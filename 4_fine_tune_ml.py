import os
import json
from datetime import datetime
from index_kb import index_all_documents
from rl_feedback_engine import optimize_rl_rewards, save_rl_rewards, load_rl_rewards, DEFAULT_ML_REWARDS

def run_ml_fine_tuning():
    print("=" * 60)
    print("     FINE-TUNING CONCISE ML RAG ENGINE & DPO PREFERENCES     ")
    print("=" * 60)
    
    # 1. Re-index Knowledge Base documents into ChromaDB
    print("\n[Step 1] Indexing Machine Learning Knowledge Base...")
    index_all_documents()
    
    # 2. Fine-tune RL Reward Weights for Machine Learning terminology
    print("\n[Step 2] Optimizing RL Reward Weights for ML Keywords...")
    rl_state = load_rl_rewards()
    rewards = rl_state.get("chunk_rewards", {})
    
    # Apply fine-tuning multiplier to core ML features
    for kw, initial_weight in DEFAULT_ML_REWARDS.items():
        rewards[kw] = max(rewards.get(kw, 0.0), initial_weight)
        
    rl_state["chunk_rewards"] = rewards
    rl_state["total_feedback_processed"] = rl_state.get("total_feedback_processed", 0) + 1
    rl_state["last_updated"] = datetime.now().isoformat()
    rl_state["ml_tuned"] = True
    
    save_rl_rewards(rl_state)
    print(f"Successfully tuned {len(rewards)} Machine Learning reward weights.")

    # 3. Export DPO Preference Pairs specifically penalizing long/verbose answers & favoring short, specific answers
    print("\n[Step 3] Constructing & Exporting Concise DPO Preference Pairs...")
    dpo_pairs = [
        {
            "prompt": "What is XGBoost?",
            "chosen": "**XGBoost** (Extreme Gradient Boosting) is an optimized decision-tree boosting algorithm. Key features: 1) Second-order Taylor expansion loss, 2) L1/L2 regularization ($\lambda, \alpha$), 3) Built-in missing value handling, and 4) Weighted quantile split finding.",
            "rejected": "XGBoost stands for Extreme Gradient Boosting. It is a very long and complex machine learning algorithm invented many years ago. It has many components including decision trees, decision forests, parameters, matrices, hyperparameter tuning techniques, cross-validation methods, pandas dataframes, numpy arrays, matplotlib visualizations..."
        },
        {
            "prompt": "What is the Bias-Variance Tradeoff?",
            "chosen": "The **Bias-Variance Tradeoff** decomposes model generalization error: Total Error = $\\text{Bias}^2 + \\text{Variance} + \\text{Irreducible Error}$. High bias causes underfitting; high variance causes overfitting.",
            "rejected": "The Bias-Variance tradeoff is a fundamental property of all statistical machine learning models. Let us begin by exploring what error means in computer science. Error is when a program does not perform as expected. There are three types of errors: bias error, variance error, and irreducible error. Bias error happens when..."
        },
        {
            "prompt": "What metrics are best for imbalanced classification?",
            "chosen": "Use **Precision**, **Recall**, **F1-Score**, or **PR-AUC**. Avoid standard accuracy because it is skewed by the majority class.",
            "rejected": "When dealing with imbalanced dataset classification tasks in machine learning engineering, there are many different metrics that a data scientist might consider using depending on the business domain and project requirements..."
        }
    ]
    
    with open("dpo_dataset.json", "w", encoding="utf-8") as f:
        json.dump(dpo_pairs, f, indent=2)
    print(f"Exported {len(dpo_pairs)} concise ML preference pairs to dpo_dataset.json")

    print("\n" + "=" * 60)
    print("     CONCISE ML FINE-TUNING COMPLETED SUCCESSFULLY!     ")
    print("=" * 60)

if __name__ == "__main__":
    run_ml_fine_tuning()
