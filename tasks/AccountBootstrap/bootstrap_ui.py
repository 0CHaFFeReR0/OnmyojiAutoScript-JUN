# This Python file uses the following encoding: utf-8
"""起号新 UI 步骤（珍旅居借入 / 觉醒 / 成就 / 新手活动 / 新手商店 / 等级 OCR）。

这些界面当前没有采集模板（无连接设备）。每个步骤先用 asset_ready() 检查关键
图片是否存在，未采集则打印「待实机补图」并跳过，使编排核心可以先跑起来。
采集模板后这些步骤即生效；页内具体选择/坐标仍需按实机截图标定。
"""
from pathlib import Path

from module.logger import logger


class BootstrapUi:
    def asset_ready(self, asset) -> bool:
        file = getattr(asset, 'file', None)
        return bool(file) and Path(file).exists()

    def _skip_pending(self, label: str, asset) -> bool:
        if self.asset_ready(asset):
            return False
        logger.warning(f'起号「{label}」资产待实机补图，跳过（{Path(asset.file).name}）')
        return True

    def read_player_level(self):
        """读取玩家等级；模板未采集或识别失败返回 None（编排退回轮数上限）。"""
        if self._skip_pending('玩家等级识别', self.I_AB_LEVEL_PANEL):
            return None
        self.screenshot()
        if not self.appear(self.I_AB_LEVEL_PANEL):
            return None
        level = self.O_AB_PLAYER_LEVEL.ocr(self.device.image)
        if isinstance(level, int) and 1 <= level <= 60:
            return level
        logger.warning(f'起号玩家等级 OCR 异常：{level}')
        return None

    def phase_setup(self, con):
        logger.hr('起号 准备：借入式神 / 觉醒辅助 / 编队', 2)
        self.borrow_shikigami(con.borrow_shikigami)
        self.awaken_support(con.support_shikigami)
        self.build_bootstrap_team(con)

    def borrow_shikigami(self, name: str) -> bool:
        """珍旅居借入五星 SP 式神（新号 30 天内）。页内选择待采集后标定。"""
        if self._skip_pending(f'珍旅居借入 {name}', self.I_AB_TRAVEL_BORROW):
            return False
        from tasks.GameUi.page import page_travel
        self.goto_page(page_travel)
        self.ui_click(self.I_AB_TRAVEL_BORROW, self.I_AB_TRAVEL_CONFIRM)
        self.ui_get_reward(self.I_AB_TRAVEL_CONFIRM)
        self.screenshot()
        if self.appear(self.I_AB_BORROW_SUCCESS):
            logger.info(f'起号已借入 {name}')
            return True
        logger.warning(f'起号借入 {name} 未校验到成功标识')
        return False

    def awaken_support(self, name: str) -> bool:
        """觉醒辅助式神（默认 R 座敷童子），材料齐全时一键觉醒。"""
        if self._skip_pending(f'觉醒 {name}', self.I_AB_AWAKEN_READY):
            return False
        from tasks.GameUi.page import page_shikigami_records
        self.goto_page(page_shikigami_records)
        if not self.appear_then_click(self.I_AB_AWAKEN_READY, interval=1):
            logger.info(f'起号 {name} 未出现可觉醒按钮，可能已觉醒')
            return False
        self.ui_get_reward(self.I_AB_AWAKEN_CONFIRM)
        logger.info(f'起号已觉醒 {name}')
        return True

    def build_bootstrap_team(self, con):
        """借入输出 + 觉醒座敷童子 + 狗粮的编队建议；具体预设由用户在式神录配置。"""
        logger.info(
            f'起号编队建议：借入 {con.borrow_shikigami} 作输出，'
            f'{con.support_shikigami}（觉醒）供火，其余位放狗粮；'
            '请在式神录保存为预设队伍，供探索/秘闻等子任务调用。'
        )

    def phase_claim(self, con):
        logger.hr('起号 领取：成就 / 新手活动 / 新手商店', 2)
        if con.claim_achievements:
            self.claim_achievements()
        if con.claim_newbie_activity:
            self.claim_newbie_activity()
        if con.buy_newbie_shop:
            self.buy_newbie_shop()

    def claim_achievements(self) -> bool:
        if self._skip_pending('成就领取', self.I_AB_ACHIEVEMENT_ENTRY):
            return False
        self.ui_click(self.I_AB_ACHIEVEMENT_ENTRY, self.I_AB_ACHIEVEMENT_CLAIM)
        self.ui_click_until_disappear(self.I_AB_ACHIEVEMENT_CLAIM, interval=1)
        logger.info('起号成就领取完成')
        return True

    def claim_newbie_activity(self) -> bool:
        if self._skip_pending('新手活动领取', self.I_AB_NEWBIE_ENTRY):
            return False
        self.ui_click(self.I_AB_NEWBIE_ENTRY, self.I_AB_NEWBIE_CLAIM)
        self.ui_click_until_disappear(self.I_AB_NEWBIE_CLAIM, interval=1)
        logger.info('起号新手活动领取完成')
        return True

    def buy_newbie_shop(self) -> bool:
        if self._skip_pending('新手商店购买', self.I_AB_NEWBIE_SHOP_ENTRY):
            return False
        self.ui_click(self.I_AB_NEWBIE_SHOP_ENTRY, self.I_AB_NEWBIE_SHOP_BUY)
        self.ui_get_reward(self.I_AB_NEWBIE_SHOP_BUY)
        logger.info('起号新手商店购买完成')
        return True

    def phase_raise(self, con):
        """三十天借用到期后的可持续单刷困28方案：培养自有 SR 姑获鸟。"""
        logger.hr('起号 培养自有输出', 2)
        logger.info(
            f'起号培养计划：将自有 {con.raise_carry} 升至六星满技能、配暴击/爆伤御魂，'
            f'目标单刷困难{con.exploration_chapter}；借用到期后由它接替 {con.borrow_shikigami}。'
            '升级/升星/技能请在式神录手动完成，御魂可由 Orochi 子任务持续刷取。'
        )