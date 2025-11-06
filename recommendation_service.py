import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class RecommendationService:
    def __init__(self, data_path='cleaned_games.csv'):
        self.df = pd.read_csv(data_path)
        self.df['combined_features'] = self.df['combined_features'].astype(str)
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features = 10000)
        self._prepare_engine()

    def _prepare_engine(self):
        # Fit and transform the combined features data
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])

    def get_recommendations(self, game_title, num_results=3):
        if game_title not in self.df['Name'].values:
            return []

        idx_list = self.df[self.df['Name'] == game_title].index.tolist()
        if not idx_list:
            return []

        game_idx = idx_list[0]

        # Calculate similarity ONLY between the target game and ALL other games
        target_game_vector = self.tfidf_matrix[game_idx:game_idx + 1]
        cosine_sim_scores = cosine_similarity(target_game_vector, self.tfidf_matrix).flatten()

        sim_scores = list(enumerate(cosine_sim_scores))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # Sort by score (x[1])

        sim_scores = sim_scores[1:num_results + 1]
        game_indices = [i[0] for i in sim_scores]  # Extract only the index part (i[0])

        return self.df['Name'].iloc[game_indices].tolist()
