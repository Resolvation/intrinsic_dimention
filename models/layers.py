import torch
from torch import nn
from torch.autograd import Variable
from torch.nn import init, Parameter
import torch.nn.functional as F
from torch.nn.modules.utils import _pair


class Flatten(nn.Module):
    """Flattens input saving batch structure."""
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return x.view(x.size(0), -1)


class StochasticLinear(nn.Module):
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.mu = Parameter(torch.Tensor(out_features, in_features))
        self.log_sigma_sqr = Parameter(torch.Tensor(out_features, in_features))
        if bias:
            self.bias = Parameter(torch.Tensor(1, out_features))
        else:
            self.register_parameter('bias', None)
        self._reset_parameters()

    def _reset_parameters(self):
        init.kaiming_normal_(self.mu)
        init.zeros_(self.log_sigma_sqr)
        if self.bias is not None:
            init.zeros_(self.bias)

    def forward(self, input):
        h_mean = F.linear(input, self.mu, self.bias)
        h_std = Variable.sqrt_(
            1e-16 + F.linear(input * input, self.sigma.exp()))
        if self.training:
            print('In stochastic mode.')
            eps = torch.randn_like(lrt_std)
        else:
            print('In determenistic mode.')
            eps = 0.
        return h_mean + eps * h_std, kl

    def kl(self):
        return ((self.log_sigma_sqr.exp() + self.mu * self.mu
                 - self.log_sigma_sqr).sum()
                - self.in_features * self.out_features) / 2

    def __repr__(self):
        return (self.__class__.__name__ + '('
                + 'in_features=' + str(self.in_features)
                + ', out_features=' + str(self.out_features)
                + ', bias=' + str(self.bias is not None) + ')')


class StochasticConv2d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1,
                 padding=0, dilation=1, groups=1, bias=True):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = _pair(kernel_size)
        self.stride = _pair(stride)
        self.padding = _pair(padding)
        self.dilation = _pair(dilation)
        self.groups = groups
        self.mu = Parameter(torch.Tensor(
            out_channels, in_channels, *self.kernel_size
        ))
        self.log_sigma_sqr = Parameter(torch.Tensor(
            out_channels, in_channels, *self.kernel_size
        ))
        if bias:
            self.bias = Parameter(torch.Tensor(1, out_channels, 1, 1))
        else:
            self.register_parameter('bias', None)
        self._reset_parameters()

    def _reset_parameters(self):
        pass

    def forward(self, input):
        return
