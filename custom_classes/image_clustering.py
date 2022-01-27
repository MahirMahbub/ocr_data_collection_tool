from typing import List

import numpy
import numpy as np
from skimage import io
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.cluster import kmeans_plusplus
from sqlalchemy.orm import Session

from app.cruds.character import CharacterCrud
from db.models import Characters


class ImageClustering(object):
    def __init__(self, db: Session, class_id: int):
        self.crud_object = CharacterCrud(db=db)
        self.class_id = class_id
        self.image_paths = []
    def __get_image_objects(self):
        image_objects: List[Characters] = self.crud_object.get_by_class_id(class_id=str(self.class_id))
        return [image.character_path for image in image_objects]

    def __read_images(self):
        self.image_paths = self.__get_image_objects()
        images = numpy.array([io.imread(image_path, as_gray=True) for image_path in self.image_paths])
        X = images.reshape(-1, images.shape[1] * images.shape[2])
        # for ind, x in enumerate(X):
        #     x = [1 if val>0 else 0 for val in x ]
        #     X[ind] = x
        # print(X.shape, images.shape)
        # print(sum(X[10]))

        return X

    def apply_pca(self):
        images = self.__read_images()
        # images = StandardScaler().fit_transform(images)
        # Make an instance of the Model
        variance = 0.98  # The higher the explained variance the more accurate the model will remain, but more dimensions will be present
        pca = PCA(n_components=variance, svd_solver='full')

        pca.fit(images)
        # images = TSNE(n_components=2, learning_rate='auto',init = 'random').fit_transform(images)
        # print("Number of components before PCA  = " + str(images.shape[1]))
        # print("Number of components after PCA 0.98 = " + str(pca.n_components_))
        if pca.n_components_ > 25:

            # print(pca.explained_variance_ratio_)
            images = pca.fit_transform(images)
            # print(images.shape)

        else:
            pca = PCA(n_components=25)
            pca.fit(images)
            images = pca.fit_transform(images)
        return images

    def apply_kmean(self):
        images = self.apply_pca()
        # k_means = KMeans(init= "k-means++", n_clusters = 3, n_init = 35)
        centers, indices = kmeans_plusplus(images, n_clusters = 3)
        # k_means.fit(images)
        # print(k_means.cluster_centers_)
        # print(indices )
        return np.array(self.image_paths)[list(indices)]
