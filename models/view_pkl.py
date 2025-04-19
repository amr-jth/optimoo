import joblib

# Full path to your .pkl file
file_path = r"models\market_classifier.pkl"  # ← Adjust if saved elsewhere

model = joblib.load(file_path)

print("Model Type:", type(model).__name__)
print("Number of Input Features:", getattr(model, 'n_features_in_', 'Unknown'))
print("Model Parameters:")
print(model.get_params())

if hasattr(model, 'feature_importances_'):
    print("\nFeature Importances:")
    print(model.feature_importances_)
