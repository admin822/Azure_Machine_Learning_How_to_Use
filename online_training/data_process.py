import torch

class my_dataset(torch.utils.data.Dataset):
    def __init__(self,x):
        super().__init__()
        self.x=x
    def __len__(self):
        return self.x.shape[0]
    def __getitem__(self,index):
        return self.x[index]


def get_training_data(data_path,batch_size):
    test_tensor=torch.load(data_path)
    dataset=my_dataset(test_tensor)
    return torch.utils.data.DataLoader(dataset,shuffle=True,batch_size=batch_size)

