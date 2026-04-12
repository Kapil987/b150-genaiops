import os
import argparse
import math
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn


def parse_args():
    p = argparse.ArgumentParser()

    # Core inputs
    p.add_argument("--csv", default="data/wine_data.csv") # provide input here
    p.add_argument("--target", default="quality")
    p.add_argument("--experiment", default="wine-prediction")

    # Hyperparameters (single source)
    p.add_argument("--n_estimators", type=int, default=50)
    p.add_argument("--max_depth", type=int, default=5)
    p.add_argument("--test_size", type=float, default=0.2)
    p.add_argument("--random_state", type=int, default=42)

    return p.parse_args()


def main():
    args = parse_args()

    # Tracking URI (must include http)
    mlflow.set_tracking_uri("http://34.207.117.242:5000/") # provide input here

    # Experiment
    mlflow.set_experiment(args.experiment)

    # Auto run name
    run_name = f"rf-{args.n_estimators}-{args.max_depth}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # Load data
    df = pd.read_csv(args.csv)

    X = df.drop(columns=[args.target])
    y = df[args.target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=args.test_size,
        random_state=args.random_state
    )

    with mlflow.start_run(run_name=run_name):

        # -------------------------
        # LOG ALL PARAMS (AUTO)
        # -------------------------
        mlflow.log_params(vars(args))  #

        # -------------------------
        # Dataset artifact
        # -------------------------
        mlflow.log_artifact(args.csv)

        # -------------------------
        # Train model
        # -------------------------
        model = RandomForestRegressor(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=args.random_state,
        )
        model.fit(X_train, y_train)

        # -------------------------
        # Metrics
        # -------------------------
        preds = model.predict(X_test)

        mse = mean_squared_error(y_test, preds)
        rmse = math.sqrt(mse)
        r2 = r2_score(y_test, preds)

        mlflow.log_metrics({
            "mse": float(mse),
            "rmse": float(rmse),
            "r2": float(r2)
        })

        # -------------------------
        # Model logging
        # -------------------------
        mlflow.sklearn.log_model(model, "model")

        # -------------------------
        # Extra artifact
        # -------------------------
        X_train.to_csv("train.csv", index=False)
        mlflow.log_artifact("train.csv")

        # -------------------------
        # Tags
        # -------------------------
        mlflow.set_tags({
            "model": "RandomForest",
            "env": "dev"
        })

        # -------------------------
        # Debug
        # -------------------------
        print("Run Name:", run_name)
        print("Run ID:", mlflow.active_run().info.run_id)
        print("Artifact URI:", mlflow.get_artifact_uri())


if __name__ == "__main__":
    main()