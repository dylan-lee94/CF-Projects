#%%
import numpy as np
import pandas as pd

class PCA(object):
    def __init__(self,n_components=None,  standardized =True):
        self.n_components = n_components
        self.standardized = standardized


    def transform(self,df):
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)

        if self.standardized:
            mat = df.corr()
        else:
            mat = df.cov()

        # Eigenvalues and eigenvectors of the data
        eig_values, eig_vec = np.linalg.eig(mat)

         # Sort the eigenvalues and eigenvectors
        idx = eig_values.argsort()[::-1]
        eig_values = eig_values[idx]
        eig_vec = eig_vec[:,idx]

        self.eig_values, self.eig_vec = eig_values[:self.n_components], eig_vec[:,:self.n_components]

        # Calculate Explained Variance 
        self.explained_variance_ratio = (self.eig_values/np.sum(eig_values)*100)

        # Return reduced data
        return np.dot(df,self.eig_vec)

