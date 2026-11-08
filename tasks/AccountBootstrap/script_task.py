# This Python file uses the following encoding: utf-8
"""起号编排任务。

复用现有子任务（CustomTask 同款 EntryConfig 包装）按阶段推进新号：
    准备（珍旅居借入 / 觉醒 / 编队）→ 领取（成就 / 新手活动 / 新手商店）
    → 刷奖励/升级循环（剧情 / 秘闻前七层 / 觉醒 / 御魂 / 探索困28 / 日常周常）
    → 培养自有输出（三十天借用到期后单刷困28）。

刷奖励循环以玩家等级 OCR 为退出条件；等级模板未采集时退回 max_farm_rounds 轮数上限。
新 UI 步骤在模板采集前会打印「待实机补图」并跳过，不影响复用子任务运行。
"""
from importlib import import_module

from module.config.config_model import ConfigModel
from module.config.utils import convert_to_underscore
from module.exception import TaskEnd
from module.logger import logger
from tasks.AccountBootstrap.assets import AccountBootstrapAssets
from tasks.AccountBootstrap.bootstrap_ui import BootstrapUi
from tasks.AccountBootstrap.config import AccountBootstrap, BootstrapConfig
from tasks.Exploration.config import ExplorationDifficulty, ExplorationLevel, UpType
from tasks.GameUi.game_ui import GameUi


class BootstrapModel(ConfigModel):
    def save(self):
        return None


class BootstrapEntryConfig:
    """深拷贝配置并覆写单个子任务的设置，捕获其调度结果；改动仅本轮生效。"""

    cooperation_runtime = None
    defer_task_courtyard_return = True

    def __init__(self, config, task_type, overrides):
        self._config = config
        self.task = convert_to_underscore(task_type)
        snapshot = config.model.model_copy(deep=True)
        fields = vars(snapshot).copy()
        task_model = fields[self.task]
        merged = task_model.model_dump()
        for key, value in overrides.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = {**merged[key], **value}
            else:
                merged[key] = value
        fields[self.task] = type(task_model).model_validate(merged)
        self.model = BootstrapModel.model_construct(**fields)
        self.success = None

    def __getattr__(self, name):
        if name in type(self.model).model_fields:
            return getattr(self.model, name)
        return getattr(self._config, name)

    def task_delay(self, task, *, success=None, **kwargs):
        if convert_to_underscore(task) == self.task:
            self.success = success
        else:
            logger.info(f'起号忽略子任务的额外调度：{task}')

    def task_call(self, task=None, **kwargs):
        logger.info(f'起号忽略子任务的调度请求：{task}')

    def save(self):
        return None


class ScriptTask(GameUi, BootstrapUi, AccountBootstrapAssets):
    def run(self):
        con: BootstrapConfig = self.config.model.account_bootstrap.bootstrap_config
        logger.hr('起号 AccountBootstrap', 1)
        logger.info(
            f'目标等级 {con.target_level}，借入 {con.borrow_shikigami}，'
            f'辅助 {con.support_shikigami}，秘闻前 {con.secret_max_layer} 层，'
            f'探索困难{con.exploration_chapter}，刷奖励上限 {con.max_farm_rounds} 轮'
        )
        if con.enable_setup:
            self.phase_setup(con)
        if con.enable_claim:
            self.phase_claim(con)
        if con.enable_farm:
            self.phase_farm(con)
        if con.enable_raise:
            self.phase_raise(con)
        self.set_next_run(task='AccountBootstrap', success=True, finish=True)
        self.finish_task_navigation()
        raise TaskEnd('AccountBootstrap')

    def phase_farm(self, con: BootstrapConfig):
        for round_idx in range(1, con.max_farm_rounds + 1):
            level = self.read_player_level()
            if level is not None and level >= con.target_level:
                logger.info(f'玩家等级 {level} 已达目标 {con.target_level}，结束刷奖励')
                return
            logger.hr(f'起号刷奖励 第 {round_idx}/{con.max_farm_rounds} 轮', 2)
            if con.farm_auto_story:
                self.run_subtask('AutoStory')
            if con.farm_secret:
                self.run_subtask('Secret', {'secret_config': {'max_layer': con.secret_max_layer}})
            if con.farm_evo_zone:
                self.run_subtask('EvoZone')
            if con.farm_orochi:
                self.run_subtask('Orochi')
            if con.farm_exploration:
                self.run_subtask('Exploration', self.exploration_overrides(con))
            if con.farm_daily_trifles:
                self.run_subtask('DailyTrifles')
            if con.farm_weekly_trifles:
                self.run_subtask('WeeklyTrifles')
            if con.claim_achievements:
                self.claim_achievements()
        logger.info(f'起号刷奖励已达轮数上限 {con.max_farm_rounds}（等级模板未采集或尚未达标）')

    @staticmethod
    def exploration_overrides(con: BootstrapConfig) -> dict:
        chapter = list(ExplorationLevel)[con.exploration_chapter - 1].value
        return {
            'exploration_config': {
                'exploration_level': chapter,
                'difficulty': ExplorationDifficulty.HARD.value,
                'up_type': UpType.EXP.value,
            }
        }

    def run_subtask(self, task_type: str, overrides: dict = None) -> bool:
        logger.hr(f'起号子任务：{task_type}', 3)
        self.device.stuck_record_clear()
        self.device.click_record_clear()
        config = BootstrapEntryConfig(self.config, task_type, overrides or {})
        try:
            runner = import_module(f'tasks.{task_type}.script_task').ScriptTask(config, self.device)
            runner._battle_cooperation_prepared = True
            result = runner.run()
        except TaskEnd:
            return config.success is True
        except Exception as exc:
            logger.warning(f'起号子任务 {task_type} 异常，继续下一项：{exc}')
            return False
        return config.success is True if config.success is not None else result is not False


if __name__ == '__main__':
    from module.config.config import Config
    from module.device.device import Device

    c = Config('oas1')
    d = Device(c)
    t = ScriptTask(c, d)
    t.run()