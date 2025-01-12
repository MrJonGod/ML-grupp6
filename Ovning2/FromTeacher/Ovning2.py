"""

# Import necessary libraries
from sklearn.datasets import load_iris, fetch_california_housing
import pandas as pd

# Load the datasets
iris = load_iris()
california = fetch_california_housing()

# Convert the datasets into DataFrames for easier exploration
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target

california_df = pd.DataFrame(data=california.data, columns=california.feature_names)
california_df['target'] = california.target

# Display the first few rows of each dataset to understand the data structure
print("Iris Dataset (Classification Task):")
print(iris_df.head())

print("\nCalifornia Housing Dataset (Regression Task):")
print(california_df.head())

# Brief descriptions of the datasets to guide discussion
print("\nIris target variable (classification):", set(iris.target))
print("California Housing target variable (regression): range =", (california_df['target'].min(), california_df['target'].max()))



"""


#mport necessary libraries
from sklearn.datasets import load_iris, fetch_california_housing
import pandas as pd

# Load the datasets
iris = load_iris()
california = fetch_california_housing()

# Convert the datasets into DataFrames for easier exploration
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target

california_df = pd.DataFrame(data=california.data, columns=california.feature_names)
california_df['target'] = california.target

# Display the first few rows of each dataset to understand the data structure
print("Iris Dataset (Classification Task):")
print(iris_df.head().to_string(index=False))

print("\nCalifornia Housing Dataset (Regression Task):")
print(california_df.head().to_string(index=False))

# Brief descriptions of the datasets to guide discussion
print("\nIris target variable (classification):", set(iris.target))
print("California Housing target variable (regression): range =", (california_df['target'].min(), california_df['target'].max()))