from Models import *
from tqdm import tqdm
import os.path
import sys
from utils.prepare_images import *

# Usage: python face_scaler.py source_dir target_dir
source_dir, target_dir = sys.argv[1], sys.argv[2]

# Load pre-trained model
# UpConv7 (Wifu2x)
model = UpConv_7()
model.load_pre_train_weights(json_file='model_check_points/Upconv_7/anime/noise2_scale2.0x_model.json')
# If GPU
model = network_to_half(model).cuda()

# # CRANv2
# model = CARN_V2(color_channels=3, mid_channels=64, conv=nn.Conv2d,
#                         single_conv_size=3, single_conv_group=1,
#                         scale=2, activation=nn.LeakyReLU(0.1),
#                         SEBlock=True, repeat_blocks=3, atrous=(1, 1, 1))
# model = network_to_half(model)
# model.load_state_dict(torch.load("model_check_points/CRAN_V2/CARN_model_checkpoint.pt", 'cpu'))
# # CPU
# model = model.float()
# GPU
# model = model.cuda()

model.eval()

# Preprocessing of images
img_splitter = ImageSplitter(seg_size=64, scale_factor=2, boarder_pad_size=3)

# Walk through every file in source folder
# Save the result into the target folder
pbar = tqdm(os.walk(source_dir))
if not os.path.exists(target_dir): os.makedirs(target_dir)
for dirpath, dirnames, filenames in pbar:
  for dirname in dirnames:
    if not os.path.exists(os.path.join(target_dir, dirname)):
      os.makedirs(os.path.join(target_dir, dirname))

  for filename in filenames:
    src_path  = os.path.join(dirpath, filename)
    tar_path  = os.path.join(target_dir, filename)
    image = Image.open(src_path).convert('RGB')
    img_patches = img_splitter.split_img_tensor(image, scale_method=None, img_pad=0)
    with torch.no_grad():
      out = [model(i.cuda().half()) for i in img_patches]
    out = img_splitter.merge_img_tensor(out)
    # From (0, 1) to (0, 255)
    if out.dim() == 4: out = out.squeeze(0)
    out = out.mul_(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to('cpu', torch.uint8).numpy()
    image = Image.fromarray(out)
    image.save(tar_path)
    print(tar_path)