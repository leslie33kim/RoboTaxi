neighbors = NearestNeighbors(n_neighbors=4)
    neighbors_fit = neighbors.fit(features)
    distances, indices = neighbors_fit.kneighbors(features)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]

    # Compute elbow point
    gradients = np.gradient(np.gradient(distances))
    elbow_index = np.argmax(gradients)
    elbow_value = distances[elbow_index]
    print(elbow_value)
    plt.plot(distances)
    plt.xlabel("Distance from the nth neighbor")
    plt.ylabel("Points sorted on ascending kth neighbor distance")
    plt.show()