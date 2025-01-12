from sklearn.linear_model import LinearRegression
import numpy as np

# Sample data
X = np.array([[1], [2], [3], [4], [5]])  # Hours studied shape (5,1)
y = np.array([50, 55, 65, 70, 80])       # Test scores

# Create a linear regression model
model = LinearRegression()

# Train the model
model.fit(X, y)


hour_studied = 3

# Convert the hour_studied to a 2D array
X_test = np.array([[hour_studied]])

# Use the model to predict the test score
predict_score = model.predict(X_test)

print(f"Predicted score for studying {hour_studied} hours: {predict_score[0]}")




# Predict
#predictions = model.predict(X)

# Output the predictions
#print(predictions)