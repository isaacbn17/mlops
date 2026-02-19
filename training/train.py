import joblib
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
    "logreg": LogisticRegression(solver="saga", max_iter=1000, random_state=42)
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

def main():
    X_train, y_train, X_test, y_test = load_data()

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

if __name__ == "__main__":
    main()
