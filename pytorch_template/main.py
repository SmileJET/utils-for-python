# encoding:utf8

import argparse
import os
import sys

import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.nn import DataParallel
from torch.utils import data
from torchvision import models, transforms

from dataloader import data_loader
from network import get_model

parser = argparse.ArgumentParser(description='DeepLesion classification')
parser.add_argument('--image_size', type=int, default=224)
parser.add_argument('--epoch', type=int, default=30)
parser.add_argument('--batch_size', type=int, default=16)
parser.add_argument('--num_workers', type=int, default=8)
parser.add_argument('--lr', type=float, default=0.0001)
parser.add_argument('--network', type=str, default='resnet18')

# dataset config
parser.add_argument('--root_path', type=str, default='./dataset')
parser.add_argument('--img_path', type=str, default='Images_png')
parser.add_argument('--csv_file', type=str, default='DL_info.csv')
parser.add_argument('--npy_path', type=str, default='./npy_files')
parser.add_argument('--type_train_npy', type=str, default='type_train_list.npy')
parser.add_argument('--type_test_npy', type=str, default='type_test_list.npy')

parser.add_argument('--need_save_checkpoint', type=bool, default=False)
parser.add_argument('--need_multi_gpus', type=bool, default=True)
parser.add_argument('--need_save_accuracy_log', type=bool, default=True)
parser.add_argument('--save_path', type=str, default='checkpoint')
parser.add_argument('--display_train_interval', type=int, default=10)
parser.add_argument('--display_test_interval', type=int, default=10)
parser.add_argument('--class_num', type=int, default=8)

# 选择GPUid
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

def main(network_name):
    num_gpu = torch.cuda.device_count()
    args = parser.parse_args()
    args.network = network_name
    print(args)
    save_path = args.save_path+'_'+args.network
    if args.need_save_checkpoint:
        if os.path.exists(save_path):
            os.system('rm -rf %s/*'%(save_path))
        else:
            os.system('mkdir %s'%(save_path))

    if args.need_save_accuracy_log:
        log_file = open('log_%s.txt'%(args.network), 'w')


    train_dataset = data_loader(args, train=True)
    test_dataset = data_loader(args, train=False)

    train_loader = data.DataLoader(dataset=train_dataset,
                                  batch_size=args.batch_size,
                                  shuffle=True,
                                  num_workers=args.num_workers)

    test_loader = data.DataLoader(dataset=test_dataset,
                                  batch_size=args.batch_size,
                                  shuffle=False,
                                  num_workers=args.num_workers)

    model = get_model(args).cuda()
    if args.need_multi_gpus:
        model = DataParallel(model, device_ids=range(num_gpu))

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    loss_func = nn.CrossEntropyLoss()
    loss_func = loss_func.cuda()

    train_total_step = len(train_loader)
    test_total_step = len(test_loader)

    for epoch in range(args.epoch):
        loss_sum = 0
        model.train()

        train_class_correct = list(0. for i in range(args.class_num))
        train_class_total = list(0. for i in range(args.class_num))

        for i, (images, label) in enumerate(train_loader):
            images = Variable(images.cuda())
            label = Variable(label.cuda())

            output = model(images)

            prediction = torch.argmax(output, 1)
            res = prediction == label
            for label_idx in range(len(label)):
                label_single = label[label_idx]
                train_class_correct[label_single] += res[label_idx].item()
                train_class_total[label_single] += 1

            loss = loss_func(output, label)
            loss_sum+=loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if i % args.display_train_interval == 0:
                sys.stdout.write('[TRAIN net] Epoch [%d/%d], Step[%d/%d], loss:%.6f\r' % (epoch + 1, args.epoch, i, train_total_step, loss.cpu().data.numpy()))
        print()
        loss_mean = loss_sum/train_total_step
        if args.need_save_checkpoint:
            if args.need_multi_gpus:
                torch.save(model.module.state_dict(),"{}/net{}_{}.pth".format(save_path, epoch, loss_mean.cpu().data.numpy()))
            else:
                torch.save(model.state_dict(),"{}/net{}_{}.pth".format(save_path, epoch, loss_mean.cpu().data.numpy()))

        print('[LOSS] %f'%(loss_mean.cpu().data.numpy()))

        print()
        model.eval()
        test_class_correct = list(0. for i in range(args.class_num))
        test_class_total = list(0. for i in range(args.class_num))
        for i, (images, label) in enumerate(test_loader):
            images = Variable(images.cuda())
            label = Variable(label.cuda())
            output = model(images)

            prediction = torch.argmax(output, 1)
            res = prediction == label
            for label_idx in range(len(label)):
                label_single = label[label_idx]
                test_class_correct[label_single] += res[label_idx].item()
                test_class_total[label_single] += 1

            if i % args.display_test_interval == 0:
                sys.stdout.write('[TEST] Step[%d/%d]\r' % (i, test_total_step))
        
        
        print()
        acc_str = '[NET %s][EPOCH %3d/%3d] Train Accuracy: %f\tTest Accuracy: %f'%(args.network, epoch + 1, args.epoch, sum(train_class_correct)/sum(train_class_total), sum(test_class_correct)/sum(test_class_total))
        acc_str+='\t[TRAIN]\t'
        for acc_idx in range(len(train_class_correct)):
            try:
                acc = train_class_correct[acc_idx]/train_class_total[acc_idx]
            except:
                acc = 0
            finally:
                acc_str += '\taccID:%d\tacc:%f\t'%(acc_idx+1, acc)
        acc_str+='\t[TEST]\t'
        for acc_idx in range(len(test_class_correct)):
            try:
                acc = test_class_correct[acc_idx]/test_class_total[acc_idx]
            except:
                acc = 0
            finally:
                acc_str += '\taccID:%d\tacc:%f\t'%(acc_idx+1, acc)

        print(acc_str)
        if args.need_save_accuracy_log:
            log_file.write(acc_str+'\n')
            log_file.flush()
    
    if args.need_save_accuracy_log:
        log_file.close()

            

if __name__ == '__main__':
    networks = [
        'vgg11', 
        'vgg13',  
        'vgg16',
        'vgg19',
        'vgg11_bn', 
        'vgg13_bn',
        'vgg16_bn', 
        'vgg19_bn', 
        'resnet18',
        'resnet34',
        'resnet50', 
        'resnet101',
        'resnet152', 
        'densenet121', 
        'densenet169', 
        'densenet161',   
        'densenet201'
        ]
    for i in range(len(networks)):
        main(networks[i])
