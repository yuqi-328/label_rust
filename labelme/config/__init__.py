import os.path as osp  # os主要提供了文件或文件夹的新建、删除、查看等方法及目录操作
import shutil      # shutil模块提供了移动、复制、 压缩、解压等操作，与os互补

import yaml

import sys
from labelme.logger import logger    # 之前定义配置好的记录器
here = osp.dirname(osp.abspath(__file__))
# osp.abspath(__file__) 该文件的绝对目录：目录中包含了该文件
# osp.dirname() 文件夹目录，是该文件所在文件夹的目录

# 把new_dict的内容更新到target_dict中
def update_dict(target_dict, new_dict, validate_item=None):
    for key, value in new_dict.items():
        if validate_item:
            validate_item(key, value)
        if key not in target_dict:
            logger.warn("Skipping unexpected key in config: {}".format(key))
            continue
        # isdistance(a,b) 判断a是否为b类型
        if isinstance(target_dict[key], dict) and isinstance(value, dict):
            update_dict(target_dict[key], value, validate_item=validate_item)
        else:
            target_dict[key] = value   #感觉是赋单值的形式，如果是字典套字典的形式，就需要递归了


# -----------------------------------------------------------------------------

# 把default_config.yaml配置文件保存在~/.labelmerc，同时把配置文件以dict形式赋给config并返回
def get_default_config():
    #config_file = osp.join(here, "default_config.yaml")
    config_file = "./config/default_config.yaml"
    #print(config_file)
    with open(config_file) as f:
        config = yaml.safe_load(f)   # dict
    
    """
    # save default config to ~/.labelmerc
    user_config_file = osp.join(osp.expanduser("~"), ".labelmerc") # C:/Users/廖雨琪/.labelmerc
    if not osp.exists(user_config_file):
        try:
            #print("搞了一个复制")
            # shutil.copy(源文件，目标地址)  返回值：返回复制之后的路径
            shutil.copy(config_file, user_config_file)
        except Exception:
            logger.warn("Failed to save config: {}".format(user_config_file))
    """

    return config

# 验证key对应的value是否符合要求
def validate_config_item(key, value):
    if key == "validate_label" and value not in [None, "exact"]:
        raise ValueError(
            "Unexpected value for config key 'validate_label': {}".format(
                value
            )
        )
    if key == "shape_color" and value not in [None, "auto", "manual"]:
        raise ValueError(
            "Unexpected value for config key 'shape_color': {}".format(value)
        )
    if key == "labels" and value is not None and len(value) != len(set(value)):
        raise ValueError(
            "Duplicates are detected for config key 'labels': {}".format(value)
        )   # 检测到配置‘label’的重复项


def get_config(config_file_or_yaml=None, config_from_args=None):
    # 1. default config
    config = get_default_config()    # 字典

    """
    # 2. specified as file or yaml  指定为文件或yaml
    if config_file_or_yaml is not None:
        config_from_yaml = yaml.safe_load(config_file_or_yaml)
        if not isinstance(config_from_yaml, dict):
            with open(config_from_yaml) as f:
                logger.info(
                    "Loading config file from: {}".format(config_from_yaml)
                )  # 对应console的info输出
                config_from_yaml = yaml.safe_load(f)
                #print(config==config_from_yaml)
        #print(config)
        #print(config_from_yaml)
        update_dict(
            config, config_from_yaml, validate_item=validate_config_item
        )

    # 3. command line argument or specified config file
    if config_from_args is not None:
        update_dict(
            config, config_from_args, validate_item=validate_config_item
        )
    """
    return config



if __name__ == "__main__":
    config = get_default_config()
