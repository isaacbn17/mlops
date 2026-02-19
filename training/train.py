import joblib
import json
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

TRAIN_PATH = "training/data/train_small.csv"
TEST_PATH = "training/data/test_small.csv"
MODEL_BUILD_PATH = "training/models/"

models = {
    "nb": MultinomialNB(),
    "logreg": LogisticRegression(solver="saga", max_iter=1000, random_state=42),
}


def load_data():
    train = pd.read_csv(TRAIN_PATH)
    test = pd.read_csv(TEST_PATH)
    X_train = train["subject"].fillna("") + " " + train["message"].fillna("")
    y_train = train["label"]
    X_test = test["subject"].fillna("") + " " + test["message"].fillna("")
    y_test = test["label"]
    return X_train, y_train, X_test, y_test

def build_pipeline(model):
    return Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("model", model)
    ])

def flatten_params(params: dict):
    flat = {}
    for k, v in params.items():
        # if nested dict/tuple/list — stringify or convert
        if isinstance(v, (dict, list, tuple)):
            params_str = json.dumps(v, default=str)
        else:
            try:
                params_str = json.dumps(v, default=str)
            except Exception:
                params_str = str(v)
        flat[k] = params_str
    return flat

def get_loggable_parameters(pipeline):
    # build  params dictionary from pipeline pieces
    params = {}
    # vectorizer params (tfidf)
    tfidf = pipeline.named_steps.get("tfidf")
    if tfidf is not None:
        params["tfidf__ngram_range"] = tfidf.ngram_range
        params["tfidf__max_df"] = tfidf.max_df
        params["tfidf__min_df"] = getattr(tfidf, "min_df", None)
        params["tfidf__stop_words"] = getattr(tfidf, "stop_words", None)

    # model params
    model = pipeline.named_steps.get("model")
    if model is not None:
        # get_params returns a dict of all hyperparams
        mp = model.get_params()
        # prefix model params so keys are unique
        params.update({f"model__{k}": mp[k] for k in mp})
    return params

def main():
    X_train, y_train, X_test, y_test = load_data()
    mlflow.set_experiment("spam_experiments")

    for name, model in models.items():
        pipeline = build_pipeline(model)
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        spam_score = f1_score(y_test, preds, pos_label=1)
        ham_score = f1_score(y_test, preds, pos_label=0)
        macro_f1 = f1_score(y_test, preds, average="macro")
        accuracy = accuracy_score(y_test, preds)
        print(f"{name}\tF1 (spam): {spam_score:.3f}\tF1 (ham): {ham_score:.3f}\tMacro F1: {macro_f1:.3f}\tAccuracy: {accuracy:.3f}")
        joblib.dump(pipeline, MODEL_BUILD_PATH + "model-" + name + ".joblib")

        full_params = get_loggable_parameters(pipeline)
        flat_params = flatten_params(full_params)
        with mlflow.start_run(run_name="model-" + name):
            mlflow.log_param("model_type", name)
            mlflow.log_metric("macro_f1", macro_f1)
            mlflow.log_params(flat_params)
            mlflow.log_dict(full_params, "params.json")
            mlflow.sklearn.log_model(pipeline, artifact_path="model")

if __name__ == "__main__":
    main()
