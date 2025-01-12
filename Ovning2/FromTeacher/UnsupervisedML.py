# Unsupervised Learning Example: K-Means Clustering

from sklearn.cluster import KMeans
import numpy as np

def unsupervised_learning_example():
    # Sample data
    X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

    # Create KMeans model
    kmeans = KMeans(n_clusters=2, n_init=10, random_state=0)
    kmeans.fit(X)

    # Predict clusters
    clusters = kmeans.predict(X)
    return clusters

unsupervised_clusters = unsupervised_learning_example()
print(unsupervised_clusters)