
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':

    print("Loading data...")
    # x_train = np.load("../dataset/train_X_3.npy")
    # x_test = np.load("../dataset/test_X_3.npy")
    # y_train = np.load("../dataset/train_Y_2.npy")
    # y_test = np.load("../dataset/test_Y_2.npy")

    x = np.load("../dataset/processed_X.npy")
    y = np.load("../dataset/processed_Y.npy")

    print("Loaded data.")

    # x = np.concatenate((x_train, x_test), axis=0).astype(np.byte)
    # y = np.concatenate((y_train, y_test), axis=0)

    assert len(x) == len(y)

    shuffler = np.random.permutation(len(x))
    x = x[shuffler]
    y = y[shuffler]

    # renormalize y
    # y[abs(y)>1] = np.sign(y[abs(y)>1])*1 + y[abs(y)>1]/10

    print("Writing files...")
   
    with open('../dataset/X_train.npy', 'wb') as f:
        np.save(f, x[:800000, :])

    with open('../dataset/X_val.npy', 'wb') as f:
        np.save(f, x[800000:900000, :])

    with open('../dataset/X_test.npy', 'wb') as f:
        np.save(f, x[900000:, :])

    with open('../dataset/Y_train.npy', 'wb') as f:
        np.save(f, y[:800000])

    with open('../dataset/Y_val.npy', 'wb') as f:
        np.save(f, y[800000:900000])

    with open('../dataset/Y_test.npy', 'wb') as f:
        np.save(f, y[900000:])
    
    print("Done.")

    