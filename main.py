import streamlit as st
from sklearn import datasets
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

st.title("Machine Learning Web App")

st.write("""
# Exploring Different Datasets and Classifiers
Which one is the best?
""")

dataset_name = st.sidebar.selectbox("Select Dataset", ("Iris", "Breast Cancer", "Wine Dataset"))
st.write(dataset_name)

classifier_name = st.sidebar.selectbox("Select Classifier", ("KNN", "SVM", "Random Forest", "Decision Tree"))

def get_dataset(dataset_name):
    if dataset_name == "Iris":
        data = datasets.load_iris()
    elif dataset_name == "Breast Cancer":
        data = datasets.load_breast_cancer()
    else:
        data = datasets.load_wine()
    X = data.data
    y = data.target
    return X, y

X, y = get_dataset(dataset_name)
st.write("Shape of he dataset", X.shape)
st.write("Number of classes", len(np.unique(y)))

def add_parameter_ui(clf_name):
    params = dict()
    if clf_name == "KNN":
        K = st.sidebar.slider("K", 1, 15)
        params["K"] = K
    elif clf_name == "SVM":
        C = st.sidebar.slider("C", 0.01, 10.0)
        params["C"] = C
    elif clf_name == "Random Forest":
        max_depth = st.sidebar.slider("max_depth", 2, 15)
        n_estimators = st.sidebar.slider("n_estimators", 1, 200)
        params["max_depth"] = max_depth
        params["n_estimators"] = n_estimators
    else:
        max_depth = st.sidebar.slider("max_depth", 2, 15)
        min_samples_leaf = st.sidebar.slider("min_samples_leaf", 1, 20)
        params["max_depth"] = max_depth
        params["min_samples_leaf"] = min_samples_leaf
    return params

params = add_parameter_ui(classifier_name)

def get_classifier(clf_name, params):
    if clf_name == "KNN":
        clf = KNeighborsClassifier(n_neighbors=params["K"])
    elif clf_name == "SVM":
        clf = SVC(C=params["C"])
    elif clf_name == "Random Forest":
        clf = RandomForestClassifier(n_estimators=params["n_estimators"],
                                     max_depth=params["max_depth"], random_state=42)
    else:
        clf = DecisionTreeClassifier(min_samples_leaf=params["min_samples_leaf"],
                                     max_depth=params["max_depth"], random_state=42)
    return clf

clf = get_classifier(classifier_name, params)

#Classidication
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

st.write(f"Classifier = {classifier_name}")
st.write(f"Accuracy = {acc}")
st.write(f"Classification Report = {report}")

# Plot
pca = PCA(2)
X_projected = pca.fit_transform(X)

x1 = X_projected[:, 0]
x2 = X_projected[:, 1]

fig = plt.show()
plt.scatter(x1, x2, c=y, alpha=0.8, cmap="viridis")
plt. xlabel("Principal componenet 1")
plt. ylabel('Principal componenet 2')
plt.colorbar()

#plt.show()
st.pyplot()