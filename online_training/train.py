import argparse
import torch.nn as nn
import torch
import os
from data_process import get_training_data
from data_process import get_training_data
from dummy import dummy_model

def train_dummy(training_data,model_save_path):
    model=dummy_model()
    criterion=nn.MSELoss(reduction='mean')
    opt=torch.optim.Adam(model.parameters(),lr=1e-4)
    model.train()
    for e in range(10000):
        for x in training_data:
            opt.zero_grad()
            result=model(x)
            loss=criterion(result,x)
            loss.backward()
            opt.step()
            print("The current loss is {}".format(loss.cpu().item()))
    print(model_save_path)
    torch.save(model.state_dict(),model_save_path)
    print("model saved!")



if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, help='Path to the training data')
    parser.add_argument('--batch_size', type=int, help='batch size for training')
    parser.add_argument('--model_path', type=str, help='path to save model')
    args=parser.parse_args()
    training_set=get_training_data(args.data_path,args.batch_size)
    
    train_dummy(training_set,os.path.join(args.model_path,'saved_model.pt'))


    
