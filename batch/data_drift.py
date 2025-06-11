import pandas as pd
import logging
import json


def load_training_stats(stats_path: str) -> dict:
    with open(stats_path, 'r') as f:
        return json.load(f)
    
def check_data_drift(current_df: pd.DataFrame, training_stats: dict, threshold: float = 0.1):
    drift_report = {}
    for col, stats in training_stats.items():
        if col not in current_df.columns:
            continue
        # Numerical columns
        if 'mean' in stats:
            current_mean = current_df[col].mean()
            train_mean = stats['mean']
            if abs(current_mean - train_mean) > threshold * abs(train_mean):
                drift_report[col] = {
                    'type': 'numerical',
                    'train_mean': train_mean,
                    'current_mean': current_mean,
                    'drift': abs(current_mean - train_mean)
                }
        # Categorical columns
        elif 'most_frequent_value' in stats:
            current_mode = current_df[col].mode().iloc[0] if not current_df[col].mode().empty else None
            train_mode = stats['most_frequent_value']
            if current_mode != train_mode:
                drift_report[col] = {
                    'type': 'categorical',
                    'train_mode': train_mode,
                    'current_mode': current_mode,
                    'drift': 'mode_changed'
                }
            # Optionally check unique values
            current_unique = current_df[col].nunique()
            train_unique = stats['unique_values']
            if abs(current_unique - train_unique) > 0:
                drift_report.setdefault(col, {}).update({
                    'unique_values_train': train_unique,
                    'unique_values_current': current_unique
                })
    if drift_report:
        logging.warning(f"Data drift detected: {drift_report}")
    else:
        logging.info("No significant data drift detected.")