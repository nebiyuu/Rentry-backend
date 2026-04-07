import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similar_items(target_uuid, product_data):
    if not product_data:
        return []

    # 1. Prepare Data
    df = pd.DataFrame(product_data, columns=['id', 'name', 'description'])
    df['combined_features'] = df['name'].fillna('') + " " + df['description'].fillna('')

    # 2. Math Logic (TF-IDF)
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])

    # 3. Similarity Logic
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    try:
        # Find the row for our target product
        idx = df.index[df['id'] == target_uuid].tolist()[0]
        
        # Calculate similarity scores
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top 3 similar (excluding itself)
        top_indices = [i[0] for i in sim_scores[1:4]]
        
        # Return the IDs
        return df['id'].iloc[top_indices].tolist()
    except Exception:
        return []