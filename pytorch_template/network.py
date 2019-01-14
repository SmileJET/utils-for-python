# encoding:utf8

import torch
import torchvision.models as models
import vgg 
import densenet

def get_model(args):
    network = args.network
    
    if network == 'vgg11':
        model = vgg.vgg11(num_classes=args.class_num)
    elif network == 'vgg13':
        model = vgg.vgg13(num_classes=args.class_num)
    elif network == 'vgg16':
        model = vgg.vgg16(num_classes=args.class_num)
    elif network == 'vgg19':
        model = vgg.vgg19(num_classes=args.class_num)
    elif network == 'vgg11_bn':
        model = vgg.vgg11_bn(num_classes=args.class_num)
    elif network == 'vgg13_bn':
        model = vgg.vgg13_bn(num_classes=args.class_num)
    elif network == 'vgg16_bn':
        model = vgg.vgg16_bn(num_classes=args.class_num)
    elif network == 'vgg19_bn':
        model = vgg.vgg19_bn(num_classes=args.class_num)
    elif network == 'resnet18':
        model = models.resnet18(num_classes=args.class_num)
        model.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=model.conv1.out_channels, kernel_size=model.conv1.kernel_size, stride=model.conv1.stride, padding=model.conv1.padding, bias=model.conv1.bias)
    elif network == 'resnet34':
        model = models.resnet34(num_classes=args.class_num)
        model.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=model.conv1.out_channels, kernel_size=model.conv1.kernel_size, stride=model.conv1.stride, padding=model.conv1.padding, bias=model.conv1.bias)
    elif network == 'resnet50':
        model = models.resnet50(num_classes=args.class_num)
        model.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=model.conv1.out_channels, kernel_size=model.conv1.kernel_size, stride=model.conv1.stride, padding=model.conv1.padding, bias=model.conv1.bias)
    elif network == 'resnet101':
        model = models.resnet101(num_classes=args.class_num)
        model.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=model.conv1.out_channels, kernel_size=model.conv1.kernel_size, stride=model.conv1.stride, padding=model.conv1.padding, bias=model.conv1.bias)
    elif network == 'resnet152':
        model = models.resnet152(num_classes=args.class_num)
        model.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=model.conv1.out_channels, kernel_size=model.conv1.kernel_size, stride=model.conv1.stride, padding=model.conv1.padding, bias=model.conv1.bias)
    elif network == 'densenet121':
        model = densenet.densenet121(num_classes=args.class_num)
    elif network == 'densenet169':
        model = densenet.densenet169(num_classes=args.class_num)
    elif network == 'densenet161':
        model = densenet.densenet161(num_classes=args.class_num)
    elif network == 'densenet201':
        model = densenet.densenet201(num_classes=args.class_num)


    return model