import pandas as pd
import numpy as np
import warnings
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

books = pd.read_csv('var/Books.csv')
users = pd.read_csv('var/Users.csv')
ratings = pd.read_csv('var/Ratings.csv')


books.isnull().sum()
books.dropna(inplace=True)
books['Year-Of-Publication'] = books['Year-Of-Publication'].astype(str)

users.isnull().sum()
users.drop('Age', axis=1, inplace=True)

ratings.isnull().sum()


ratings_with_name = pd.merge(ratings, books, on='ISBN')
# Group the data by 'Book-Title' and count the number of 'Book-Rating' entries for each book
num_rating_df = ratings_with_name.groupby('Book-Title').count()

# Reset the index to reformat the grouped data into a new DataFrame
num_rating_df = num_rating_df.reset_index()

# Rename the 'Book-Rating' column to 'num_ratings'
num_rating_df = num_rating_df.rename(columns={'Book-Rating': 'num_ratings'})


# Grouping the data by 'Book-Title' and calculate the mean (average) of 'Book-Rating' for each book
avg_rating_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].mean()

# Converting the resulting Series to a DataFrame and reset the index
avg_rating_df = avg_rating_df.reset_index()

# Renaming the 'Book-Rating' column to 'avg_rating'
avg_rating_df = avg_rating_df.rename(columns={'Book-Rating': 'avg_rating'})

# Rounding the 'avg_rating' column to two decimal places
avg_rating_df['avg_rating'] = avg_rating_df['avg_rating'].round(2)

# Merging the 'num_rating_df' and 'avg_rating_df' DataFrames based on the 'Book-Title' column
popular_df = pd.merge(num_rating_df, avg_rating_df, on='Book-Title')

# Filtering the 'popular_df' DataFrame to create 'no_of_ratings_df' where 'num_ratings' is greater than or equal to 250
no_of_ratings_df = popular_df.loc[popular_df['num_ratings'] >= 250]

# Sorting the 'no_of_ratings_df' DataFrame in descending order based on the 'avg_rating' column
sorted_df = no_of_ratings_df.sort_values(by='avg_rating', ascending=False)

# Merging the 'books' DataFrame with 'sorted_df' based on the common 'Book-Title' column
merge_df = pd.merge(books, sorted_df, on='Book-Title')

# Removing duplicate entries based on the 'Book-Title' column
remove_duplicate_df = merge_df.drop_duplicates(subset='Book-Title')

# Grouping the 'ratings_with_name' DataFrame by 'User-ID' and count the number of 'Book-Rating' entries for each user
x = ratings_with_name.groupby('User-ID')['Book-Rating'].count() > 200

Educated_users = x[x].index

filtered_rating = ratings_with_name[ratings_with_name['User-ID'].isin(Educated_users)]

# Grouping the 'filtered_rating' DataFrame by 'Book-Title' and count the number of 'Book-Rating' entries for each book
y = filtered_rating.groupby('Book-Title')['Book-Rating'].count() >= 50

# Creating a new Series 'famous_books' by selecting the indices (Book-Titles) where 'y' is True
famous_books = y[y].index

# Filtering the 'filtered_rating' DataFrame to include only rows where the 'Book-Title' is in the 'famous_books' Series
final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]

# Creating a pivot table 'pt' using the .pivot_table() function on the 'final_ratings' DataFrame
pt = final_ratings.pivot_table(index='Book-Title', columns=['User-ID'], values='Book-Rating')

# Filling any missing values (NaN) in the pivot table 'pt' with zeros
pt.fillna(0, inplace=True)

similarity_scores = cosine_similarity(pt)
