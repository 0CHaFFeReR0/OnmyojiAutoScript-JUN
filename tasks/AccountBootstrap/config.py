# This Python file uses the following encoding: utf-8
from pydantic import BaseModel, Field

from tasks.Component.config_base import ConfigBase, TimeDelta
from tasks.Component.config_scheduler import Scheduler as BaseScheduler


class Scheduler(BaseScheduler):
    success_interval: TimeDelta = Field(default=TimeDelta(hours=6), description='success_interval_help')
    failure_interval: TimeDelta = Field(default=TimeDelta(hours=1), description='failure_interval_help')


class BootstrapConfig(BaseModel):
    target_level: int = Field(title='Target Level', default=40, ge=1, le=60, description='target_level_help')
    borrow_shikigami: str = Field(title='Borrow Shikigami', default='姑获鸟', description='borrow_shikigami_help')
    support_shikigami: str = Field(title='Support Shikigami', default='座敷童子', description='support_shikigami_help')
    raise_carry: str = Field(title='Raise Carry', default='姑获鸟', description='raise_carry_help')

    secret_max_layer: int = Field(title='Secret Max Layer', default=7, ge=1, le=10, description='secret_max_layer_help')
    exploration_chapter: int = Field(title='Exploration Chapter', default=28, ge=1, le=28, description='exploration_chapter_help')
    max_farm_rounds: int = Field(title='Max Farm Rounds', default=6, ge=1, le=50, description='max_farm_rounds_help')

    enable_setup: bool = Field(title='Enable Setup', default=True, description='enable_setup_help')
    enable_claim: bool = Field(title='Enable Claim', default=True, description='enable_claim_help')
    enable_farm: bool = Field(title='Enable Farm', default=True, description='enable_farm_help')
    enable_raise: bool = Field(title='Enable Raise', default=True, description='enable_raise_help')

    farm_auto_story: bool = Field(title='Farm Auto Story', default=True, description='farm_auto_story_help')
    farm_secret: bool = Field(title='Farm Secret', default=True, description='farm_secret_help')
    farm_evo_zone: bool = Field(title='Farm Evo Zone', default=True, description='farm_evo_zone_help')
    farm_orochi: bool = Field(title='Farm Orochi', default=True, description='farm_orochi_help')
    farm_exploration: bool = Field(title='Farm Exploration', default=True, description='farm_exploration_help')
    farm_daily_trifles: bool = Field(title='Farm Daily Trifles', default=True, description='farm_daily_trifles_help')
    farm_weekly_trifles: bool = Field(title='Farm Weekly Trifles', default=True, description='farm_weekly_trifles_help')

    claim_achievements: bool = Field(title='Claim Achievements', default=True, description='claim_achievements_help')
    claim_newbie_activity: bool = Field(title='Claim Newbie Activity', default=True, description='claim_newbie_activity_help')
    buy_newbie_shop: bool = Field(title='Buy Newbie Shop', default=True, description='buy_newbie_shop_help')


class AccountBootstrap(ConfigBase):
    scheduler: Scheduler = Field(default_factory=Scheduler)
    bootstrap_config: BootstrapConfig = Field(default_factory=BootstrapConfig)