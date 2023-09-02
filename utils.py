import torch
import numpy as np
import torch.nn as nn
import torchvision.transforms as tfs
from torchvision.utils import make_grid
from PIL import Image
import matplotlib.pyplot as plt

from ffaNet import FFA



class Dehaze:
    def __init__(self) -> None:
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.gps=3
        self.blocks=19
        self.model_weights = 'weights/FFA.pk'


    def load_model(self):
        ckp = torch.load(self.model_weights, map_location=self.device)
        net = FFA(gps=self.gps, blocks=self.blocks)
        net = nn.DataParallel(net)
        net.load_state_dict(ckp['model'])
        return net

    def dehaze(self, img_path):
        haze = Image.open(img_path)
        haze1 = tfs.Compose([
            tfs.ToTensor(),
            tfs.Normalize(mean=[0.64, 0.6, 0.58],std=[0.14,0.15, 0.152])
        ])(haze)[None,::]
        model = self.load_model()
        model.eval()
        with torch.no_grad():
            pred = model(haze1)
        ts = torch.squeeze(pred.clamp(0,1).cpu())
        ts = make_grid(ts, nrow=1, normalize=True)

        ts = np.transpose(ts, (1, 2, 0))
        return ts
    
if __name__ == "__main__":
    output = Dehaze().dehaze(img_path='test.png')
    plt.imshow(output)
    plt.savefig('output.png')