import argparse
import base64
import json
import os
import os.path as osp

import imgviz
import PIL.Image

from labelme.logger import logger
from labelme import utils


# 从dir_path中提取tar_type类型的文件，返回文件名列表
# 注意: tar_type: ".txt",".json",必须包含"."
def take_samefile(dir_path, tar_type):
    tar_filenames = []
    files = os.listdir(dir_path)  # 读取dir_path文件列表
    for filename in files:
        if osp.splitext(filename)[1] == tar_type:  # 读取文件名后缀
            tar_filenames.append(filename)
    print("%s文件共有%d个" % (tar_type, len(tar_filenames)))
    return tar_filenames  # 只有文件名字，不包含路径的列表


# 将json_dir文件夹中的json文件转化为mask.png图片，并保存在mask_dir文件夹下
def json_to_mask(json_dir, mask_dir, label_name_to_value):
    json_files = take_samefile(json_dir, ".json")  # 从json所在的文件夹提取json文件
    for file in json_files:
        json_file = osp.join(json_dir, file)       # json文件路径
        mask_file = file.replace("json", "png")
        mask_file = osp.join(mask_dir, mask_file)  # mask文件路径

        # 从json文件中获取原图img
        data = json.load(open(json_file))
        imageData = data.get("imageData")
        if not imageData:
            imagePath = osp.join(osp.dirname(json_file), data["imagePath"])
            with open(imagePath, "rb") as f:
                imageData = f.read()
                imageData = base64.b64encode(imageData).decode("utf-8")
        img = utils.img_b64_to_arr(imageData)  # 原图

        # label_name_to_value
        for shape in data["shapes"]:
            label_name = shape["label"]
            if label_name not in label_name_to_value:
                label_value = len(label_name_to_value)
                label_name_to_value[label_name] = label_value

        # 获取mask图片并保存
        lbl, _ = utils.shapes_to_label(img.shape, data["shapes"], label_name_to_value)
        utils.lblsave(mask_file, lbl)


def export(json_dir, out_dir=None):
    if out_dir is None:
        out_dir = osp.join(json_dir, "mask")
    if not osp.exists(out_dir):
        os.mkdir(out_dir)
    label_name_to_value = {"_background_": 0}  # 整个文件夹的图片用相同的label
    json_to_mask(json_dir, out_dir, label_name_to_value)  # 一次保存每个mask图片
    with open(osp.join(out_dir, "label.txt"), "w") as f:  # 保存txt说明文档
        for name, value in label_name_to_value.items():
            f.write(name + " :  " + str(value) + "\n")
    logger.info("Saved to: {}".format(out_dir))           # 提示


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_dir")
    parser.add_argument("-o", "--out", default=None)
    args = parser.parse_args()

    json_dir = args.json_dir        # json所在文件夹的目录

    if args.out is None:
        out_dir = osp.join(osp.dirname(json_dir), "mask")
    else:
        out_dir = args.out
    if not osp.exists(out_dir):
        os.mkdir(out_dir)

    label_name_to_value = {"_background_": 0}  # 整个文件夹的图片用相同的label
    json_to_mask(json_dir, out_dir, label_name_to_value)
    with open(osp.join(out_dir,"label.txt"),"w") as f:
        for name, value in label_name_to_value.items():
            f.write(name + " :  " + str(value) + "\n")
    logger.info("Saved to: {}".format(out_dir))


if __name__ == "__main__":
    main()