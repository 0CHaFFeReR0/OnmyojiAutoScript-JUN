# This Python file uses the following encoding: utf-8
"""起号新 UI 资产契约。

这些 ROI 均为占位值，对应的 res/*.png 尚未采集（当前无连接设备）。
bootstrap_ui.py 通过 asset_ready() 检查图片文件是否存在：未采集的步骤会
打印「待实机补图」并跳过，不会用占位 ROI 去做无意义的匹配。

采集方法：连接设备后运行
    toolkit/python.exe dev_tools/account_bootstrap/capture_assets.py
保存整屏截图到 res/，再按下列清单裁剪模板并回填 ROI。

清单（name -> 用途）：
    ab_travel_borrow      珍旅居「借入」入口/按钮
    ab_travel_confirm     借用确认弹窗的确认按钮
    ab_borrow_success     借用成功标识（用于校验）
    ab_awaken_ready       式神录「觉醒」按钮（材料齐全态）
    ab_awaken_confirm     觉醒确认按钮
    ab_achievement_entry 成就入口
    ab_achievement_claim  成就「领取」按钮
    ab_newbie_entry       新手活动入口
    ab_newbie_claim       新手活动「领取」按钮
    ab_newbie_shop_entry  新手商店入口
    ab_newbie_shop_buy    新手商店「购买」按钮
    ab_level_panel        玩家等级面板标识（存在时才启用等级 OCR）
"""
from module.atom.image import RuleImage
from module.atom.ocr import RuleOcr


class AccountBootstrapAssets:
    # 占位 ROI：roi_front 待裁剪模板后由 load_image 自动校正，roi_back 待标定。
    I_AB_TRAVEL_BORROW = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_travel_borrow.png")
    I_AB_TRAVEL_CONFIRM = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_travel_confirm.png")
    I_AB_BORROW_SUCCESS = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_borrow_success.png")

    I_AB_AWAKEN_READY = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_awaken_ready.png")
    I_AB_AWAKEN_CONFIRM = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_awaken_confirm.png")

    I_AB_ACHIEVEMENT_ENTRY = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_achievement_entry.png")
    I_AB_ACHIEVEMENT_CLAIM = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_achievement_claim.png")

    I_AB_NEWBIE_ENTRY = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_newbie_entry.png")
    I_AB_NEWBIE_CLAIM = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_newbie_claim.png")

    I_AB_NEWBIE_SHOP_ENTRY = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_newbie_shop_entry.png")
    I_AB_NEWBIE_SHOP_BUY = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_newbie_shop_buy.png")

    I_AB_LEVEL_PANEL = RuleImage(roi_front=(0, 0, 1, 1), roi_back=(0, 0, 1280, 720), threshold=0.8, method="Template matching", profile="High", file="./tasks/AccountBootstrap/res/ab_level_panel.png")
    # 玩家等级数字 OCR，ROI 待实机标定；仅在 I_AB_LEVEL_PANEL 采集后启用。
    O_AB_PLAYER_LEVEL = RuleOcr(roi=(0, 0, 1, 1), area=(0, 0, 1, 1), mode="Digit", method="Default", keyword="", name="ab_player_level")