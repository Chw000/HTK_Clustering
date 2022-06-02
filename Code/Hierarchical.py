import numpy as np
import psutil
import os
from time import time
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering


def txt2array(txt_path, delimiter):
    data_list = []
    with open(txt_path) as f:
        data = f.readlines()
    for line in data:
        line = line.strip("\n")
        data_split = line.split(delimiter)
        temp = list(map(float, data_split))
        data_list.append(temp)

    data_array = np.array(data_list)
    return data_array


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)


if __name__ == '__main__':
    begin_time = time()
    # loading txt
    X = txt2array("D:/python program/txt/Ionosphere.txt", ",")
    # setting distance_threshold=0 ensures we compute the full tree.
    model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
    model = model.fit(X)
    plt.title('Hierarchical Clustering Dendrogram')
    # plot the top three levels of the dendrogram
    plot_dendrogram(model, truncate_mode='level', p=3)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    end_time = time()
    run_time = end_time - begin_time
    plt.show()
    print(u'Memory usage of the current process：%.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
    print('The elapsed time of the loop program：', run_time)
