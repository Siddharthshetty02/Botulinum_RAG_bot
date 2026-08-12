import os
import json
from datetime import datetime

LOGS_FILE = "chat_logs.jsonl"
FEEDBACK_FILE = "feedback_logs.jsonl"
RL_REWARDS_FILE = "rl_rewards.json"
DPO_DATASET_FILE = "dpo_dataset.json"

LEARNING_RATE = 0.2
DISCOUNT_FACTOR = 0.9

def load_jsonl(filepath):
    data = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data.append(json.loads(line))
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    return data

DEFAULT_ML_REWARDS = {
    "machine": 0.85, "learning": 0.85, "xgboost": 0.90, "hyperparameter": 0.85,
    "classification": 0.80, "regression": 0.80, "clustering": 0.80,
    "overfitting": 0.85, "bias": 0.85, "variance": 0.85, "validation": 0.75,
    "precision": 0.80, "recall": 0.80, "f1": 0.80, "chromadb": 0.75, "vector": 0.75,
    "regularization": 0.80, "supervised": 0.80, "unsupervised": 0.80
}

def load_rl_rewards():
    if os.path.exists(RL_REWARDS_FILE):
        try:
            with open(RL_REWARDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure default ML rewards are merged if not already present
                rewards = data.get("chunk_rewards", {})
                for k, v in DEFAULT_ML_REWARDS.items():
                    if k not in rewards:
                        rewards[k] = v
                data["chunk_rewards"] = rewards
                return data
        except Exception as e:
            print(f"Error reading {RL_REWARDS_FILE}: {e}")
    return {"chunk_rewards": DEFAULT_ML_REWARDS.copy(), "total_feedback_processed": 0, "last_updated": None}

def save_rl_rewards(rewards_data):
    try:
        with open(RL_REWARDS_FILE, "w", encoding="utf-8") as f:
            json.dump(rewards_data, f, indent=2)
        print(f"Successfully saved RL rewards to {RL_REWARDS_FILE}")
    except Exception as e:
        print(f"Error saving {RL_REWARDS_FILE}: {e}")

def optimize_rl_rewards():
    """
    RL Engine: Reads interaction & feedback logs, computes reward signals R in [+1.0, -1.0],
    updates chunk preference weights via Q-learning update rule, and exports DPO preference pairs.
    """
    print("\n--- Running Reinforcement Learning Feedback Optimization ---")
    chat_logs = load_jsonl(LOGS_FILE)
    feedback_logs = load_jsonl(FEEDBACK_FILE)
    
    if not feedback_logs:
        print("No user feedback logs found yet. RL engine waiting for user ratings.")
        return load_rl_rewards()
        
    chat_map = {log["id"]: log for log in chat_logs if "id" in log}
    rl_state = load_rl_rewards()
    chunk_rewards = rl_state.get("chunk_rewards", {})
    
    dpo_pairs = []
    processed_count = 0
    
    # Query to positive/negative answer mapping for DPO pair construction
    query_answers = {}

    for fb in feedback_logs:
        log_id = fb.get("log_id")
        rating = fb.get("rating")
        
        if not log_id or log_id not in chat_map:
            continue
            
        chat_item = chat_map[log_id]
        question = chat_item.get("question", "")
        answer = chat_item.get("answer", "")
        
        # Reward signal: +1.0 for thumbs up, -1.0 for thumbs down
        reward_signal = 1.0 if rating == "up" else -1.0
        
        # Track answers for DPO dataset generation
        if question not in query_answers:
            query_answers[question] = {"chosen": [], "rejected": []}
        if rating == "up":
            query_answers[question]["chosen"].append(answer)
        else:
            query_answers[question]["rejected"].append(answer)
            
        # Update chunk reward weights based on feedback
        # If question contains keyword topics, adjust weight for related chunks
        words = [w.lower() for w in question.split() if len(w) > 3]
        for word in words:
            current_weight = chunk_rewards.get(word, 0.0)
            # RL TD update: W_new = W_old + lr * (reward - W_old)
            new_weight = current_weight + LEARNING_RATE * (reward_signal - current_weight)
            chunk_rewards[word] = round(new_weight, 4)
            
        processed_count += 1

    # Build DPO Preference Dataset (chosen vs rejected)
    for q, pairs in query_answers.items():
        if pairs["chosen"] and pairs["rejected"]:
            for chosen in pairs["chosen"]:
                for rejected in pairs["rejected"]:
                    dpo_pairs.append({
                        "prompt": q,
                        "chosen": chosen,
                        "rejected": rejected
                    })

    if dpo_pairs:
        try:
            with open(DPO_DATASET_FILE, "w", encoding="utf-8") as f:
                json.dump(dpo_pairs, f, indent=2)
            print(f"Exported {len(dpo_pairs)} DPO preference pairs to {DPO_DATASET_FILE}")
        except Exception as e:
            print(f"Error saving DPO dataset: {e}")

    rl_state["chunk_rewards"] = chunk_rewards
    rl_state["total_feedback_processed"] = processed_count
    rl_state["dpo_pair_count"] = len(dpo_pairs)
    rl_state["last_updated"] = datetime.now().isoformat()
    
    save_rl_rewards(rl_state)
    print(f"RL Optimization complete. Updated {len(chunk_rewards)} topic reward weights.")
    return rl_state

if __name__ == "__main__":
    optimize_rl_rewards()
