import numpy as np
import scipy.sparse as sp

class Lasso:
    def __init__(self, X, y, lam, w, w0=0, delta=0.01):
        """

        :param X: A scipy.csc matrix (sparse matrix) of features.
                  Rows are training data and columns are features.
        :param wo: initial weight to use for bias.  Not sparse.
        """
        assert type(X) == sp.csc_matrix
        self.X = X
        assert type(y) == np.ndarray
        self.y = y
        assert w.shape[0] == self.X.shape[1]
        self.w = w        # sp.csc_matrix
        self.w0 = w0*1.
        self.lam = lam
        self.delta = delta
        self.yhat = None  # sp.csc_matrix
        self.N = self.X.shape[0]

    def optimize_weights(self):
        print("begin optimizing weights")

        # have to initialize old_w before entering the while loop.
        old_w = self.w + \
                sp.csc_matrix(np.ones(self.w.shape[0])).T*2*self.delta #sparse

        assert(self.is_converged(old_w) is False)

        # check that the weights haven't converged.
        while not self.is_converged(old_w):
            old_w = self.w.copy()   #sparse

            # calculate predictions to avoid numerical drift.
            # import pdb; pdb.set_trace()
            old_yhat = self.calculate_yhat()  #not sparse

            # update the bias.
            old_w0 = self.w0  # get it before we write over it
            self.update_w0(old_yhat)  # updates self.w0

            # update our predictions, yhat, using the new w0.
            self.update_yhat(old_yhat, old_w0)  # updates self.yhat

            # iterate over the d features
            for k in range(0, self.w.shape[0]):
                self.update_wk(k)

            # check that the objective function decreased
            old_objective_fun_val = None  #todo: calc
            new_objective_fun_val = None  #todo: calc
            #assert(new_objective_fun_val < old_objective_fun_val)

        print("Lasso optimized.")
        print("w: {}, w0: {}".format(self.w.toarray(), self.w0))

        return

    def calculate_yhat(self):
        # multiply X*w + w_o
        # returns vector of predictions, yhat.
        print("Calc X*w + w_0 for w = {}, w_0={}".format(self.w, self.w0))

        # don't want to store this yhat.  Temporary.
        yhat = self.X.dot(self.w) + self.w0
        yhat = yhat.toarray()
        assert yhat.shape[1] == 1
        return yhat

    def update_w0(self, old_yhat):
        new_w0 = sum(self.y - old_yhat)/self.N + self.w0
        assert type(new_w0*1.0 == float)  # sometimes I had int.
        return new_w0

    def update_yhat(self, old_yhat, old_w0):
        self.yhat = old_yhat + self.w0 - old_w0
        assert type(self.yhat == np.array)
        assert self.yhat.shape[1] == 1

    def update_wk(self, k):
        """
        :param k: zero-indexed column
        :return:
        """
        Xik = self.X[:, k]  # array  (slice of sparse matrix)
        wk = self.extract_scalar(self.w[k])
        #import pdb; pdb.set_trace()
        ak = 2*self.extract_scalar(Xik.T.dot(Xik))

        tmp = self.y - self.yhat + Xik.toarray()*wk
        assert tmp.shape[1] == 1  # column vector
        ck = 2*self.extract_scalar(Xik.T.dot(tmp))

        # apply the update rule.
        print("ck: {}, lambda: {}".format(ck, self.lam))
        if ck < - self.lam:
            self.w[k] = (ck + self.lam)/ak
        elif ck > self.lam:
            self.w[k] = (ck - self.lam)/ak
        else:
            self.w[k] = 0

    @staticmethod
    def calc_objective_fun(X, w, w0, y):
        pass

    def is_converged(self, old_w):
        # stop when no element of w changes by more than some small delta
        # return True if it is time to stop.
        # see HW pg 8.

        print("Testing convergence.")
        print("Old w: {}, new w: {}".format(old_w.toarray(),
                                            self.w.toarray()))

        # make a vector of the differences in each element
        delta_w = old_w - self.w

        for w_i in delta_w :
            if abs(w_i) > self.delta:
                return False

        return True

    @staticmethod
    def check_for_objective_increase():
        # need a nonincreasing objective value
        pass

    @staticmethod
    def extract_scalar(m):
        """
        :param m: A 1x1 sparse matrix.
        :return: The entry in that matrix.
        """
        assert(m.shape == (1,1))
        return m[0,0]


class RegularizationPath:
    def __init__(self):
        pass

    def determine_smallest_lambda(self):
        pass