import joblib
import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download ('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, svm
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, chi2
import numpy as np

cell_df = pd.read_csv("dataset/mix_dataset.csv")
print('Shape:', cell_df.shape)
print(cell_df.head(5))
cell_df.dropna(inplace=True)
"""
import nltk
nltk.download("stopwords")
nltk.download("wordnet")
"""

cell_df['text'] = [str(entry).lower() for entry in cell_df['text']]
words = stopwords.words("english")

wl = WordNetLemmatizer()
cell_df['cleaned'] = cell_df['text'].apply(
    lambda x: " ".join([wl.lemmatize(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())
cell_df.head(5)

Train_X, Test_X, Train_y, Test_y = model_selection.train_test_split(cell_df['cleaned'], cell_df['label'], test_size=0.2)
# Test_y.fillna(Test_X.mean())

print("Train_X Shape => ", Train_X.shape)
print("Train y Shape => ", Train_y.shape)
print("Test_X Shape => ", Test_X.shape)
print("Test_y Shape => ", Test_y.shape)

pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
                     ('chi', SelectKBest(chi2, k=10000)),
                     ('clf', svm.SVC(C=2.0, kernel='linear', gamma='auto'))])

model = pipeline.fit(Train_X, Train_y)

vect = model.named_steps['vect']
try:
   print("\nFeature names => \n", vect.get_feature_names())
except AttributeError:
    print('No such attribute')

print("accuracy score: " + str(model.score(Test_X, Test_y)))

# print("Prediction",model.predict(["Just at home watching movies"]))

svm_model = "svm.pkl"
joblib.dump(model, svm_model)
