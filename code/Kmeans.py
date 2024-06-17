import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
from collections import defaultdict
import math

class KMeans:
    def __init__(self, n_clusters, max_iter=300, tol=1e-4):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.centroids = None
        self.feature_keywords = {
            "Energy-Efficient": ["energy", "efficient", "power", "eco", "saving", "green", "consumption", "sustainable"],
            "Compact": ["compact", "small", "space", "sleek", "portable", "tiny", "minimal", "mini"],
            "Durable": ["durable", "sturdy", "robust", "long-lasting", "strong", "tough", "resilient", "hard-wearing"],
            "Innovative": ["innovative", "creative", "novel", "unique", "cutting-edge", "advanced", "original", "breakthrough"],
            "Ergonomic": ["ergonomic", "comfortable", "user-friendly", "easy-to-use", "handy", "intuitive", "well-designed"],
            "Quiet": ["quiet", "silent", "noise-free", "hushed", "low-noise", "soundless", "peaceful", "whisper-quiet"],
            "Smart": ["smart", "intelligent", "automated", "connected", "high-tech", "AI", "advanced", "clever"],
            "Stylish": ["stylish", "fashionable", "elegant", "chic", "sleek", "trendy", "modern", "aesthetic"],
            "Versatile": ["versatile", "multi-purpose", "adaptable", "flexible", "all-around", "universal", "multi-functional"],
            "High-Capacity": ["high-capacity", "large", "roomy", "spacious", "big", "substantial", "ample", "vast"],
            "Fast": ["fast", "quick", "speedy", "rapid", "swift", "high-speed", "efficient", "prompt"],
            "Safe": ["safe", "secure", "risk-free", "protected", "harmless", "trustworthy", "reliable", "riskless"],
            "User-Friendly": ["user-friendly", "easy-to-use", "accessible", "simple", "intuitive", "convenient", "straightforward"],
            "Affordable": ["affordable", "cheap", "inexpensive", "budget", "cost-effective", "economical", "low-cost", "reasonable"],
            "Reliable": ["reliable", "dependable", "consistent", "trustworthy", "steady", "unfailing", "proven", "stable"]
        }
        self.features = list(self.feature_keywords.keys())
        self.feature_to_id = {feature: i for i, feature in enumerate(self.features)}
        self.keywords = [word for keywords in self.feature_keywords.values() for word in keywords]

    def preprocess_text(self, text):
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        
        # Remove non-alphabetic characters and convert to lowercase
        text = re.sub(r'[^a-zA-Z]', ' ', text).lower()
        # Tokenize and lemmatize
        words = text.split()
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return ' '.join(words)

    def fit_from_file(self, file_path):
        texts = []
        labels = []
        with open(file_path, 'r') as file:
            for line in file:
                label, text = line.split("]: ", 1)
                label = label.strip("[")
                texts.append(text.strip())
                labels.append(self.features.index(label))

        self.fit(texts, labels)

    def fit(self, texts, labels):
        # Preprocess texts
        processed_texts = [self.preprocess_text(text) for text in texts]

        # Vectorize texts using TF-IDF
        X = self._tfidf_vectorize(processed_texts)
        
        # Initialize centroids based on labeled data
        self.centroids = np.zeros((self.n_clusters, X.shape[1]))
        for i in range(self.n_clusters):
            self.centroids[i] = X[np.array(labels) == i].mean(axis=0)

        for i in range(self.max_iter):
            # Assign clusters based on closest centroid
            distances = self._cosine_distances(X, self.centroids)
            new_labels = np.argmin(distances, axis=1)

            # Calculate new centroids
            new_centroids = np.array([X[new_labels == j].mean(axis=0) for j in range(self.n_clusters)])

            # Check for convergence
            if np.linalg.norm(self.centroids - new_centroids) < self.tol:
                break

            self.centroids = new_centroids

        self.labels_ = new_labels

    def predict(self, text):
        # Preprocess text
        processed_text = self.preprocess_text(text)

        # Vectorize text using TF-IDF
        X = self._tfidf_vectorize([processed_text], fit=False)

        # Assign cluster based on closest centroid
        distances = self._cosine_distances(X, self.centroids)
        label = np.argmin(distances, axis=1)
        
        feature = self.features[label[0]]
        feature_id = self.feature_to_id[feature]

        return feature, feature_id

    def _tfidf_vectorize(self, texts, fit=True):
        # Calculate term frequencies (TF)
        term_frequencies = []
        for text in texts:
            word_count = defaultdict(int)
            words = text.split()
            for word in words:
                if word in self.keywords:
                    word_count[word] += 1
            term_frequencies.append(word_count)

        # Calculate document frequencies (DF)
        doc_frequencies = defaultdict(int)
        for word_count in term_frequencies:
            for word in word_count:
                doc_frequencies[word] += 1

        # Calculate TF-IDF
        N = len(texts)
        tfidf_matrix = []
        for word_count in term_frequencies:
            tfidf_vector = []
            for word in self.keywords:
                tf = word_count[word]
                df = doc_frequencies[word]
                idf = math.log((N + 1) / (df + 1)) + 1
                tfidf_vector.append(tf * idf)
            tfidf_matrix.append(tfidf_vector)

        return np.array(tfidf_matrix)

    def _cosine_distances(self, X, centroids):
        distances = np.zeros((X.shape[0], centroids.shape[0]))
        for i, x in enumerate(X):
            for j, centroid in enumerate(centroids):
                distances[i, j] = 1 - np.dot(x, centroid) / (np.linalg.norm(x) * np.linalg.norm(centroid))
        return distances

"""
if __name__ == "__main__":
    kmeans = KMeans(n_clusters=15)
    kmeans.fit_from_file("commentGenSamples.txt")
    
    new_comment = "I love how this device consumes minimal power without compromising performance."
    assigned_feature, assigned_feature_id = kmeans.predict(new_comment)
    print(f"Comment: {new_comment}\nAssigned Feature: {assigned_feature}, Feature ID: {assigned_feature_id}\n")
"""
