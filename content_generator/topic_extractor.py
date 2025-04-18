from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from collections import Counter


class TopicExtractor:
    def __init__(self):
        self.Vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 3)
        )

    def extract_topics_from_text(self, texts):

        if not texts:
            return []

        #set import scores
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        features_name = self.vectorizer.get_feature_names_out()

        # Sum the importance scores across documents
        importance_score = np.asarray(tfidf_matrix.sum(axis=0)).flatten()
        word_importance = {feature_names[i]: importance_score[i] for i in range(len(feature_names))}

        #sort by importance

        sorted_topics = sorted(word_importance.items(), key=lambda x: x[1], reverse=True)

        return [topic[0] for topic in sorted_topics[:20]]

    def extract_topics_from_trends(self, trends_data):

        all_texts = []

        for article in trends_data.get("news_api", []):
            if article.get("title"):
                all_texts.append(article.get("title", ""))
            if article.get("description"):
                all_texts.append(article.get("description", ""))

        for article in trends_data.get("tech_blogs", []):
            if article.get("title"):
                all_texts.append(article.get("title", ""))

            if article.get("summary"):
                all_texts.append(article.get("summary", ""))

        return self.extract_topics_from_text(all_texts)

