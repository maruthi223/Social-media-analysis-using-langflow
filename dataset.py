import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# Set a random seed for reproducibility
np.random.seed(42)

# Number of records
num_records = 100

# Generate synthetic data
data = {
    'User_ID': np.arange(1001, 1001 + num_records),
    'Followers_Count': np.random.randint(0, 1000000, size=num_records),
    'Post_Type': np.random.choice(['Carousel', 'Reels', 'Static Images'], size=num_records),
    'Likes_Received': np.random.randint(1, 10000, size=num_records),
    'Comments_Received': np.random.randint(1, 5000, size=num_records),
    'Share_Count': np.random.randint(1, 2000, size=num_records),
    'Popularity_Level': np.random.choice(['Low', 'Medium', 'High'], size=num_records)
}

# Introduce missing values in the 'Likes_Received' and 'Comments_Received' columns
missing_percentage = 0.05  # You can adjust this percentage as needed

missing_likes = np.random.choice([True, False], size=num_records, p=[missing_percentage, 1 - missing_percentage])
missing_comments = np.random.choice([True, False], size=num_records, p=[missing_percentage, 1 - missing_percentage])

# Convert the column to float before assigning NaN
data['Likes_Received'] = data['Likes_Received'].astype(float)
data['Comments_Received'] = data['Comments_Received'].astype(float)

data['Likes_Received'][missing_likes] = np.nan
data['Comments_Received'][missing_comments] = np.nan
imputer = SimpleImputer(strategy='mean')
# Create a DataFrame
df = pd.DataFrame(data)
df[['Likes_Received', 'Comments_Received']] = imputer.fit_transform(df[['Likes_Received', 'Comments_Received']])

print(df.head())

df.to_csv('dataset.csv')