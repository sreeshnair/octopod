import numpy as np
from sklearn.metrics import accuracy_score
import torch
import torch.nn as nn
import torch.nn.functional as F


def _softmax_final_layer(x):
    return F.softmax(x, dim=1)


def _multi_class_accuracy_preprocess(x):
    return torch.max(torch.tensor(x), 1)[1].numpy()


def _multi_label_accuracy_preprocess(x):
    return np.round(x, 0)


def _multi_class_accuracy(y_true, preds):
    """
    Takes in raw outputs from Tonks task heads and outputs an accuracy metric
    and the processed predictions after a softmax as been applied

    Parameters
    ----------
    y_true: np.array
        Target labels for a specific task for the predicted samples in `preds`
    preds: np.array
        predicted values for the validation set for a specific task

    Returns
    -------
    acc: float
        Output of a sklearn accuracy score function
    y_preds: np.array
        array of predicted values where a softmax has been applied

    """
    tensor_y_pred = torch.from_numpy(preds)
    y_preds = _softmax_final_layer(tensor_y_pred).numpy()
    task_preds = (
        _multi_class_accuracy_preprocess(y_preds)
    )
    acc = accuracy_score(y_true, task_preds)
    return acc, y_preds


def _multi_label_accuracy(y_true, preds):
    """
    Takes in raw outputs from Tonks task heads and outputs an accuracy metric
    and the processed predictions after a sigmoid as been applied

    Parameters
    ----------
    y_true: np.array
        Target labels for a specific task for the predicted samples in `preds`
    preds: np.array
        predicted values for the validation set for a specific task

    Returns
    -------
    acc: float
        Output of a sklearn accuracy score function
    y_preds: np.array
        array of predicted values where a sigmoid has been applied
    """
    tensor_y_pred = torch.from_numpy(preds)
    y_preds = torch.sigmoid(tensor_y_pred).numpy()
    task_preds = (
        _multi_label_accuracy_preprocess(y_preds)
    )
    acc = accuracy_score(y_true, task_preds)
    return acc, y_preds


DEFAULT_LOSSES_DICT = {
    'categorical_cross_entropy': nn.CrossEntropyLoss(),
    'bce_logits': nn.BCEWithLogitsLoss(),
}


DEFAULT_ACC_DICT = {
    'multi_class_acc': _multi_class_accuracy,
    'multi_label_acc': _multi_label_accuracy,
}
