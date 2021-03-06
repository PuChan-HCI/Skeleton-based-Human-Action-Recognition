#coding:utf-8
# License: BSD
# Original author: Fanyang Meng, nkliuyifang

import torch.nn as nn
from torchvision import models

    
#fine-tuning VGG19 
class FullCNN(nn.Module):
    def __init__(self,actionType):
        super(FullCNN, self).__init__()
        loadmodel = models.vgg19(pretrained=True)
        ##you can vision model
        #print(loadmodel)
        loadmodel.classifier._modules["6"] = nn.Linear(4096,actionType)
        self.premodel = loadmodel
        #self.relu = nn.ReLU() 
        #softmax = nn.Softmax()
        #bilinear = nn.Upsample(size=224,mode='bilinear')

    def forward(self, inputs):
        out = self.premodel(inputs)
        #out   = self.softmax(self.relu(self.premodel(self.bilinear(inputs))))
        return out
		
		
class MobileNet(nn.Module):
    def __init__(self,actionType):
        super(MobileNet, self).__init__()
        def conv_bn(inp, oup, stride):
            return nn.Sequential(
                nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
                nn.BatchNorm2d(oup),
                nn.ReLU(inplace=True)
            )

        def conv_dw(inp, oup, stride):
            return nn.Sequential(
                nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
                nn.BatchNorm2d(inp),
                nn.ReLU(inplace=True),
    
                nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
                nn.BatchNorm2d(oup),
                nn.ReLU(inplace=True),
            )

        self.model = nn.Sequential(
            conv_bn(  3,  32, 2), 
            conv_dw( 32,  64, 1),
            conv_dw( 64, 128, 2),
            conv_dw(128, 128, 1),
            conv_dw(128, 256, 2),
            conv_dw(256, 256, 1),
            conv_dw(256, 512, 2),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 512, 1),
            conv_dw(512, 1024, 2),
            conv_dw(1024, 1024, 1),
            nn.AvgPool2d(7),
        )
        self.fc = nn.Linear(1024, actionType)

    def forward(self, x):
        x = self.model(x)
        x = x.view(-1, 1024)
        x = self.fc(x)
        return x
    

