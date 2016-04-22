# Movie Recommendation Systems
# Ryan Wedoff & Zongsheng Sun
# Data From http://grouplens.org/datasets/movielens/
# Citations
# F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History
# and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4,
# Article 19 (December 2015), 19 pages. DOI=http://dx.doi.org/10.1145/2827872

# Notes:  20M data set was too big for my laptop!
import scipy.sparse
from scipy.sparse import linalg
import numpy as np
import scipy.io


def convert_to_titles(rel_array2):
    # Sort the values so that the least worst movie is first, and the best used movie is last.
    # Values is a sorted array of the indexes, sorting low to high
    values = np.argsort(rel_array2)
    # Save and print the 10 most closely associated songs for word i = row 1
    movie_indices = np.array(
        [values[-1], values[-2], values[-3], values[-4], values[-5], values[-6], values[-7], values[-8], values[-9],
         values[-10]]) + 1  # just for the index start from 0
    # print(movie_indices)
    # Search the movie file for the movie title
    movies_file = open('ml-100k/u.item', 'r', encoding="ISO-8859-1")  # Used for ml-100k
    # movies_file = open('ml-1m/movies.dat', 'r', encoding="ISO-8859-1") # Used for ml-1m
    movie_dict = {}
    for movieLine in movies_file:
        # chunk = movieLine.split("::")  # Used for ml-1m
        chunk = movieLine.split("|")  # Used for ml-100k
        movie_dict[str(chunk[0])] = chunk[1]
    movies_file.close()
    recommend_movies = []
    for movieId in movie_indices:
        try:
            recommend_movies.append(movie_dict[str(movieId)])
        except:
            pass
    # print(recommend_movies)
    return recommend_movies


def recommend(file_name):
    f = open(file_name, 'r', encoding='utf-8')
    # chunk[0] = user id
    # chunk[1] = item id
    # chunk[2] = rating
    # chunk[3] = timestamp
    row_list = []
    col_list = []
    val_list = []
    f.readline()
    for line in f:
        chunk = line.split("\t")  # Used for ml-100k
        # chunk = line.split("::")  # Used for ml-1m
        row_list.append(int(chunk[0]) - 1)  # as the index starts from 0
        col_list.append(int(chunk[1]) - 1)  # as the index starts from 0
        val_list.append(float(chunk[2]))
    f.close()

    # create sparse matrices
    sparse_matrix = scipy.sparse.csr_matrix((val_list, (row_list, col_list)))
    weight_for_movie = (sparse_matrix != 0).sum(axis=0)
    alpha = 0.9
    weight_for_movie = 1 - alpha ** np.asarray(weight_for_movie).flatten()

    # print(max(row_list) + 1)  # This number is used in test file
    weight = np.asarray((sparse_matrix != 0).sum(axis=0)).flatten()
    weight[np.where(weight == 0)[0]] = 1

    # calculate the average of nonzero element
    average_rating = np.multiply(sparse_matrix.sum(axis=0), 1.0 / weight)  # calculate the average of nonzero element

    sparse_matrix -= scipy.sparse.csr_matrix((sparse_matrix != 0).multiply(average_rating))

    # get the average exceed average rate for each user
    average_exceed_rating = np.multiply(sparse_matrix.sum(axis=1), 1.0 / (sparse_matrix != 0).sum(axis=1))

    # get the r matrix
    sparse_matrix -= scipy.sparse.csr_matrix((sparse_matrix != 0).multiply(average_exceed_rating))

    # SVD Computation
    u, sing_values, vt = scipy.sparse.linalg.svds(sparse_matrix,
                                                  k=20)

    # Convert the singular values to a diagonal matrix shape
    sigma = np.diag(sing_values)

    # If the given id is not a user, throw an error and load next screen
    # if not user_count >= chosen_row >= 1:

    svd_result = []
    movie_names = []  # This is the row/user we will choose
    chosen_row = 0
    while chosen_row < max(row_list) + 1:
        # Multiply row i or left singular vectors, and multiply by the diagonal
        # of the singular values times the transpose of the right singular values
        # add back the average rate and the AverageExceed Rate
        rel_array1 = u[chosen_row].dot(sigma).dot(vt) + average_rating + average_exceed_rating.item(chosen_row)
        rel_array1 = np.multiply(rel_array1, weight_for_movie) + (1 - weight_for_movie) * 3
        rel_array2 = rel_array1 - (sparse_matrix.getrow(chosen_row) != 0).multiply(rel_array1)

        rel_array1 = np.asarray(rel_array1).flatten()
        rel_array2 = np.asarray(rel_array2).flatten()

        # print(rel_array1)
        svd_result.append(rel_array1)
        names = convert_to_titles(rel_array2)
        movie_names.append(names)
        chosen_row += 1
    svd_result = np.asmatrix(svd_result)
    svd_result.dump("svd_result-100k.dat")
    movie_names = np.asmatrix(movie_names)
    movie_names.dump("rec_results-100k.dat")
    # svd_result.dump("svd_result-1m.dat")
    # movie_names = np.asmatrix(movie_names)
    # movie_names.dump("rec_results-1m.dat")
