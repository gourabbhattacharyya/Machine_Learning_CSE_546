import numpy as np


class ClassificationBase:
    """
    Methods common to classification.
    """
    def __init__(self, X, y, w=None, w0=0):

        self.X = X #sp.csc_matrix(X)
        self.N, self.d = self.X.shape
        self.y = y
        assert self.y.shape == (self.N, )

        # number of classes may be 2, or more than 2.
        self.C = np.unique(y).shape[0]

        if w is None:
            self.w = np.ones(self.d)
        elif type(w) == np.ndarray:
            self.w = w
        else:
            assert False, "w is not None or a numpy array."
        assert self.w.shape == (self.d ,), \
            "shape of w is {}".format(self.w.shape)
        if w0 is None:
            self.w0=0
        else:
            self.w0 = w0

    def pred_to_01_loss(self, class_calls):
        """
        + one point for every class that's correctly called.
        """
        return self.N - np.equal(self.y, class_calls).sum()

    #def pred_to_normalized_01_loss(self, class_calls):
    #    return self.loss_01(class_calls)/self.N

    def step(self):
        pass

    def run(self):
        pass

