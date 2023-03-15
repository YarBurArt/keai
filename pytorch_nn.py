import torch
from torch.autograd import Variable
from torch.nn import Module, Linear, NLLLoss
from torch.nn.functional import relu, log_softmax
from torch.optim import SGD
from torchvision.datasets import MNIST
from torchvision.transforms import Compose, ToTensor, Normalize
from torch.utils.data import DataLoader


def simple_gradient():
    # print the gradient of 2x^2 + 5x
    x = Variable(torch.ones(2, 2) * 2, requires_grad=True)
    z = 2 * (x * x) + 5 * x
    # run the backpropagation
    z.backward(torch.ones(2, 2))
    print(x.grad)


def create_nn(batch_size=200, learning_rate=0.01, epochs=10,
              log_interval=10):

    train_loader = DataLoader(
        MNIST('../data', train=True, download=True,
              transform=Compose([
                  ToTensor(),
                  Normalize((0.1307,), (0.3081,))
               ])),
        batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(
        MNIST('../data', train=False, transform=Compose([
            ToTensor(),
            Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=batch_size, shuffle=True)

    class Net(Module):
        def __init__(self):
            super(Net, self).__init__()
            self.fc1 = Linear(28 * 28, 200)
            self.fc2 = Linear(200, 200)
            self.fc3 = Linear(200, 10)

        def forward(self, x):
            x = relu(self.fc1(x))
            x = relu(self.fc2(x))
            x = self.fc3(x)
            return log_softmax(x)

    net = Net()
    print(net)

    # create a stochastic gradient descent optimizer
    optimizer = SGD(net.parameters(), lr=learning_rate, momentum=0.9)
    # create a loss function
    criterion = NLLLoss()

    # run the main training loop
    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = Variable(data), Variable(target)
            # resize data from (batch_size, 1, 28, 28) to (batch_size, 28*28)
            data = data.view(-1, 28*28)
            optimizer.zero_grad()
            net_out = net(data)
            loss = criterion(net_out, target)
            loss.backward()
            optimizer.step()
            if batch_idx % log_interval == 0:
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                    100. * batch_idx / len(train_loader), loss.data[0]))

    # run a test loop
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        data, target = Variable(data, volatile=True), Variable(target)
        data = data.view(-1, 28 * 28)
        net_out = net(data)
        # sum up batch loss
        test_loss += criterion(net_out, target).data[0]
        pred = net_out.data.max(1)[1]  # get the index of the max log-probability
        correct += pred.eq(target.data).sum()

    len_test_dataset = len(test_loader.dataset)
    test_loss /= len_test_dataset
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len_test_dataset,
        100. * correct / len_test_dataset))


if __name__ == "__main__":
    run_opt = 2
    if run_opt == 1:
        simple_gradient()
    elif run_opt == 2:
        create_nn()
