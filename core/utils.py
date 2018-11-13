import os

import torch


def lr(optimizer):
    """
    Return learning rate of the optimizer.
    """
    for param_group in optimizer.param_groups:
        return param_group["lr"]


def adjust_learning_rate(optimizer, lr):
    """
    Set the learning rate of the optimizer to lr.
    """
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr


def lr_linear(epoch, decay_start, total, initial_lr):
    """
    Return linearly decaying learning rate for given epoch.
    """
    if epoch < decay_start:
        return initial_lr
    return initial_lr * float(total-epoch) / float(total-decay_start)


def save(net, name="last_net"):
    """
    Save net with standart PyTorch methods.
    """
    base = "./logs"
    if not os.path.exists(base):
        os.mkdir(base)
    torch.save(net.state_dict(), base+ '/'+name+".tar")
