import torch
from torch import nn
from d2l import torch as d2l

def corr2d(X, K):
    h, w = K.shape
    Y = torch.zeros((X.shape[0] - h + 1, X.shape[1] - w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i, j] = (X[i:i + h, j:j + w] * K).sum()
    return Y

X = torch.tensor([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0], [6.0, 7.0, 8.0]])
K = torch.tensor([[0.0, 1.0], [2.0, 3.0]])
Y=corr2d(X, K)
#print(Y)


class Conv2D(nn.Module):
    def __init__(self,kernel_size):
        super().__init__()
        self.weghts= nn.Parameter(torch.rand(kernel_size))
        self.bias=nn.Parameter(torch.zeros(1))
    def forward(self,x):
        return corr2d(x,self.weghts)+self.bias

X = torch.ones((6,8))
X [:,2:6]= 0

print("gias trij X la ", X.data)
# print(X)
# print(X.t())

K = torch.tensor([[1.0,-1.0]])

Y = corr2d(X,K)
print("giá trị Y sau tích chập thông thường", Y)
conv2d = nn.LazyConv2d(1,kernel_size=(1,2), bias = False)

X = X.reshape((1,1,6,8))
Y = Y.reshape((1, 1, 6, 7))
lr = 3e-2  # Learning rate

for i in range(10):
    Y_hat = conv2d(X) ### khai báo Y = mạng neuron X
    l = (Y_hat - Y) ** 2  ## loss
    conv2d.zero_grad()   ## đạo hàm
    l.sum().backward()  ## lan truyền ngược
    # Update the kernel
    conv2d.weight.data[:] -= lr * conv2d.weight.grad  ## cập nhật giá trị weghts = lan truyền ngược
    if (i + 1) % 2 == 0:
        print(f'epoch {i + 1}, loss {l.sum():.3f}, gia trị hàm weghts: {conv2d.weight.data.shape}')



