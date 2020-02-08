import torch
import torch.nn as nn


class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.in_channels = 6
        self.ndf = 64
        self.out_channels = 1

        self.main = nn.Sequential(
            nn.Conv2d(self.in_channels, self.ndf, 4, 2, 1, bias=False),

            nn.Conv2d(self.ndf, self.ndf*2, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ndf*2),

            nn.Conv2d(self.ndf*2, self.ndf*4, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ndf*4),

            nn.Conv2d(self.ndf*4, self.ndf*8, 4, 1, 1, bias=False),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ndf*8),

            nn.Conv2d(self.ndf*8, self.out_channels, 4, 1, 1, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x, label):
        out = torch.cat((x, label), dim=1)
        out = self.main(out)
        return out


class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()

        self.input_dim = 3
        self.ngf = 64
        self.output_dim = 3

        self.conv1 = nn.Sequential(
            nn.Conv2d(self.input_dim, self.ngf, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ngf)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(self.ngf, self.ngf*2, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ngf*2)
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(self.ngf*2, self.ngf*4, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ngf*4)
        )

        self.conv4 = nn.Sequential(
            nn.Conv2d(self.ngf*4, self.ngf*8, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ngf*8)
        )

        self.conv5 = nn.Sequential(
            nn.Conv2d(self.ngf*8, self.ngf*8, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ngf*8)
        )

        self.conv6 = nn.Sequential(
            nn.Conv2d(self.ngf*8, self.ngf*8, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ngf*8)
        )

        self.conv7 = nn.Sequential(
            nn.Conv2d(self.ngf*8, self.ngf*8, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.BatchNorm2d(self.ngf*8)
        )

        self.conv8 = nn.Sequential(
            nn.Conv2d(self.ngf*8, self.ngf*8, 4, 2, 1),
            nn.LeakyReLU(0.2)
        )

        self.deconv1 = nn.Sequential(
            nn.ConvTranspose2d(self.ngf*8, self.ngf*8, 4, 2, 1),
            nn.BatchNorm2d(self.ngf*8),
            nn.Dropout2d(0.5),
            nn.ReLU()
        )

        self.deconv2 = nn.Sequential(
            nn.ConvTranspose2d(self.ngf*16, self.ngf*8, 4, 2, 1),
            nn.BatchNorm2d(self.ngf*8),
            nn.Dropout2d(0.5),
            nn.ReLU()
        )

        self.deconv3 = nn.Sequential(
            nn.ConvTranspose2d(self.ngf*16, self.ngf*8, 4, 2, 1),
            nn.BatchNorm2d(self.ngf*8),
            nn.Dropout2d(0.5),
            nn.ReLU()
        )

        self.deconv4 = nn.Sequential(
            nn.ConvTranspose2d(self.ngf*16, self.ngf*8, 4, 2, 1),
            nn.BatchNorm2d(self.ngf*8),
            nn.ReLU()
        )

        self.deconv5 = nn.Sequential(
            nn.ConvTranspose2d(self.ngf*16, self.ngf*4, 4, 2, 1),
            nn.BatchNorm2d(self.ngf*4),
            nn.ReLU()
        )

        self.deconv6 = nn.Sequential(
            nn.ConvTranspose2d(self.ngf*8, self.ngf*2, 4, 2, 1),
            nn.BatchNorm2d(self.ngf*2),
            nn.ReLU()
        )

        self.deconv7 = nn.Sequential(
            nn.ConvTranspose2d(self.ngf*4, self.ngf, 4, 2, 1),
            nn.BatchNorm2d(self.ngf),
            nn.ReLU()
        )

        self.deconv8 = nn.Sequential(
            nn.ConvTranspose2d(self.ngf*2, self.output_dim, 4, 2, 1),
            nn.ReLU()
        )

    def forward(self, x):
        enc1 = self.conv1(x)
        enc2 = self.conv2(enc1)
        enc3 = self.conv3(enc2)
        enc4 = self.conv4(enc3)
        enc5 = self.conv5(enc4)
        enc6 = self.conv6(enc5)
        enc7 = self.conv7(enc6)
        enc8 = self.conv8(enc7)

        dec1 = torch.cat([self.deconv1(enc8), enc7], dim=1)
        dec2 = torch.cat([self.deconv2(dec1), enc6], dim=1)
        dec3 = torch.cat([self.deconv3(dec2), enc5], dim=1)
        dec4 = torch.cat([self.deconv4(dec3), enc4], dim=1)
        dec5 = torch.cat([self.deconv5(dec4), enc3], dim=1)
        dec6 = torch.cat([self.deconv6(dec5), enc2], dim=1)
        dec7 = torch.cat([self.deconv7(dec6), enc1], dim=1)
        dec8 = self.deconv8(dec7)
        out = nn.Tanh()(dec8)

        return out