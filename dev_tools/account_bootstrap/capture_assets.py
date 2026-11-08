# This Python file uses the following encoding: utf-8
"""起号新 UI 资产采集助手。

连接设备后截取整屏保存到 tasks/AccountBootstrap/res/，并列出尚未采集的模板清单，
供人工裁剪模板、回填 assets.py 的 ROI。对 config/*.json 只读，不写用户配置。

用法：
    PYTHONPATH=. toolkit/python.exe dev_tools/account_bootstrap/capture_assets.py [配置名]
默认配置名 oas1。可重复运行采集不同界面（珍旅居/式神录/成就/新手活动/新手商店/等级面板）。
"""
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import cv2

from module.atom.image import RuleImage
from tasks.AccountBootstrap.assets import AccountBootstrapAssets


def pending_assets() -> list:
    pending = []
    for name in dir(AccountBootstrapAssets):
        asset = getattr(AccountBootstrapAssets, name)
        if isinstance(asset, RuleImage) and not Path(asset.file).exists():
            pending.append((name, asset.file))
    return pending


def main():
    config_name = sys.argv[1] if len(sys.argv) > 1 else 'oas1'
    print('待采集模板清单：')
    for name, file in pending_assets():
        print(f'  {name:28s} -> {file}')
    if not pending_assets():
        print('  （全部已采集）')

    from module.config.config import Config
    from module.device.device import Device
    config = Config(config_name)
    device = Device(config)
    image = device.screenshot()
    res_dir = REPO / 'tasks' / 'AccountBootstrap' / 'res'
    res_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    out = res_dir / f'capture_{stamp}.png'
    cv2.imwrite(str(out), image)
    print(f'整屏截图已保存：{out}')
    print('请按清单裁剪对应模板放到 res/，并回填 assets.py 的 roi_front/roi_back。')


if __name__ == '__main__':
    main()