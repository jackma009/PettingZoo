"""
空间战争环境。

这个环境模拟了一个太空战斗游戏，玩家控制宇宙飞船在太空中
进行对抗，需要通过灵活的机动和精准的射击来击败对手。

主要特点：
1. 双人对战
2. 太空战斗
3. 物理引擎
4. 战术对抗

环境规则：
1. 基本设置
   - 飞船单位
   - 武器系统
   - 太空环境
   - 引力场

2. 交互规则
   - 飞船控制
   - 武器发射
   - 碰撞检测
   - 伤害计算

3. 智能体行为
   - 轨道机动
   - 瞄准射击
   - 能源管理
   - 战术规避

4. 终止条件
   - 击毁对手
   - 时间耗尽
   - 能源耗尽
   - 飞船损毁

环境参数：
- 观察空间：游戏画面状态
- 动作空间：飞船控制和武器系统
- 奖励：击中得分和存活奖励
- 最大步数：由比赛设置决定

环境特色：
1. 战斗系统
   - 武器类型
   - 弹道轨迹
   - 护盾系统
   - 能源管理

2. 物理机制
   - 引力效应
   - 惯性运动
   - 动量守恒
   - 碰撞物理

3. 战术元素
   - 轨道计算
   - 能源分配
   - 火力压制
   - 机动规避

4. 评估系统
   - 命中率
   - 存活时间
   - 能源效率
   - 整体表现

注意事项：
- 轨道规划
- 能源管理
- 武器选择
- 战术决策
"""
"""
太空战争游戏环境。

这个环境实现了雅达利游戏《太空战争》，两名玩家在太空中驾驶战舰进行对抗，
需要考虑引力场、能量管理和战术策略。

主要特点：
1. 双人对战
2. 物理引擎
3. 能量管理
4. 战术对抗

游戏规则：
1. 基本设置
   - 两艘战舰
   - 引力场
   - 能量系统
   - 武器装备

2. 战斗规则
   - 能量消耗
   - 引力影响
   - 碰撞伤害
   - 武器命中

3. 战舰控制
   - 推进器
   - 旋转
   - 开火
   - 护盾

4. 终止条件
   - 能量耗尽
   - 战舰摧毁
   - 时间结束
   - 一方认输

环境参数：
- 观察空间：游戏画面（RGB数组）
- 动作空间：6个离散动作
- 奖励：击中对手和生存时间
- 最大步数：由能量限制决定

游戏特色：
1. 物理系统
   - 引力效应
   - 惯性运动
   - 碰撞检测
   - 能量传递

2. 战舰特性
   - 推进系统
   - 武器系统
   - 护盾系统
   - 能量管理

3. 战术元素
   - 位置控制
   - 能量分配
   - 攻击时机
   - 防御策略

4. 环境影响
   - 引力场
   - 太空碎片
   - 能量场
   - 边界效应

注意事项：
- 能量管理
- 引力利用
- 预判轨道
- 战术规划

"""
"""
# 太空战争（Space War）

```{figure} atari_space_war.gif
:width: 140px
:name: space_war
```

此环境是<a href='..'>Atari 环境</a>的一部分。请先阅读该页面以了解基本信息。

| 导入               | `from pettingzoo.atari import space_war_v2` |
|----------------------|---------------------------------------------|
| 动作类型           | 离散                                        |
| 并行 API          | 支持                                         |
| 手动控制          | 不支持                                      |
| 智能体            | `agents= ['first_0', 'second_0']`           |
| 智能体数量        | 2                                           |
| 动作形状          | (1,)                                        |
| 动作值范围        | [0,17]                                      |
| 观察形状          | (250, 160, 3)                               |
| 观察值范围        | (0,255)                                     |


*太空战争*是一个竞争性游戏，预测和定位是关键。

玩家在地图上移动。当你的对手被你的子弹击中时，
你得一分。这个游戏类似于战斗，但有一个更高级的物理系统，需要考虑加速度和动量。

每当你得分时，你获得 +1 奖励，而你的对手受到 -1 惩罚。

[官方太空战争手册](https://atariage.com/manual_html_page.php?SoftwareLabelID=470)

#### 环境参数

环境参数是所有 Atari 环境通用的，在[基础 Atari 文档](../atari)中有描述。

### 动作空间

在任何给定回合中，智能体可以从 18 个动作中选择一个。

| 动作     | 行为    |
|:---------:|---------|
| 0         | 无操作  |
| 1         | 开火    |
| 2         | 向上移动 |
| 3         | 向右移动 |
| 4         | 向左移动 |
| 5         | 向下移动 |
| 6         | 向右上移动 |
| 7         | 向左上移动 |
| 8         | 向右下移动 |
| 9         | 向左下移动 |
| 10        | 向上开火 |
| 11        | 向右开火 |
| 12        | 向左开火 |
| 13        | 向下开火 |
| 14        | 向右上开火 |
| 15        | 向左上开火 |
| 16        | 向右下开火 |
| 17        | 向左下开火 |

### 版本历史

* v2：最小动作空间 (1.18.0)
* v1：对整个 API 进行重大更改 (1.4.0)
* v0：初始版本发布 (1.0.0)


"""

import os
from glob import glob

from pettingzoo.atari.base_atari_env import (
    BaseAtariEnv,
    base_env_wrapper_fn,
    parallel_wrapper_fn,
)


def raw_env(**kwargs):
    name = os.path.basename(__file__).split(".")[0]
    parent_file = glob(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), name + "*.py")
    )
    version_num = parent_file[0].split("_")[-1].split(".")[0]
    name = name + "_" + version_num
    return BaseAtariEnv(
        game="space_war", num_players=2, mode_num=None, env_name=name, **kwargs
    )


env = base_env_wrapper_fn(raw_env)
parallel_env = parallel_wrapper_fn(env)
