import torch.nn as nn

class dummy_model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.fc=nn.Linear(10,10)
        self.ac=nn.ReLU()
    def forward(self,x):
        x=self.fc(x)
        return self.ac(x)