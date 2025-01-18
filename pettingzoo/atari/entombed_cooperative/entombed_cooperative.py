"""
合作迷墓环境。

这个环境模拟了一个双人合作的迷墓探险游戏，玩家需要在不断生成的
迷宫中协同探索和生存，通过团队配合来获取资源并避免危险。

主要特点：
1. 双人合作
2. 迷宫探索
3. 资源管理
4. 生存挑战

环境规则：
1. 基本设置
   - 探险者角色
   - 动态迷宫
   - 生存资源
   - 危险陷阱

2. 交互规则
   - 角色移动
   - 资源收集
   - 陷阱避免
   - 团队配合

3. 智能体行为
   - 路径规划
   - 资源分配
   - 危险规避
   - 互助合作

4. 终止条件
   - 资源耗尽
   - 陷入陷阱
   - 时间结束
   - 任务完成

环境参数：
- 观察空间：游戏画面状态
- 动作空间：角色移动和交互
- 奖励：生存时间和资源收集
- 最大步数：由关卡设置决定

环境特色：
1. 迷宫系统
   - 动态生成
   - 路径变化
   - 资源分布
   - 陷阱布置

2. 控制机制
   - 角色移动
   - 资源获取
   - 陷阱躲避
   - 团队互助

3. 战术元素
   - 资源规划
   - 路径选择
   - 风险评估
   - 团队协作

4. 评估系统
   - 生存时间
   - 资源数量
   - 合作效率
   - 整体表现

注意事项：
- 路径选择
- 资源管理
- 风险控制
- 团队配合
"""
# noqa: D212, D415
"""
合作探墓游戏环境。

这个环境实现了雅达利游戏《探墓》的合作模式，两名玩家在不断生成的迷宫中探索前进，
需要互相配合来收集资源和避开危险。

主要特点：
1. 双人合作
2. 程序生成迷宫
3. 资源管理
4. 动态难度

游戏规则：
1. 基本设置
   - 两名玩家
   - 动态迷宫
   - 有限资源
   - 多种道具

2. 探索规则
   - 收集资源得分
   - 避开陷阱
   - 互助合作
   - 共享资源

3. 角色控制
   - 上下左右移动
   - 使用道具
   - 破坏墙壁
   - 救援队友

4. 终止条件
   - 生命耗尽
   - 资源用完
   - 到达终点
   - 双方同意退出

环境参数：
- 观察空间：游戏画面（RGB数组）
- 动作空间：8个离散动作
- 奖励：收集资源和生存时间
- 最大步数：由迷宫长度决定

游戏特色：
1. 迷宫特性
   - 自动生成
   - 不断延伸
   - 多条路径
   - 隐藏区域

2. 资源系统
   - 生命值
   - 能量值
   - 特殊道具
   - 解密工具

3. 合作机制
   - 资源共享
   - 互相救援
   - 协同探索
   - 团队奖励

4. 危险元素
   - 移动陷阱
   - 毒气区域
   - 坍塌通道
   - 时间限制

注意事项：
- 资源管理关键
- 需要沟通配合
- 路线规划重要
- 风险评估必要
"""
"""
# 活埋：合作版（Emtombed: Cooperative）

```{figure} atari_entombed_cooperative.gif
:width: 140px
:name: entombed_cooperative
```

此环境是<a href='..'>Atari 环境</a>的一部分。请先阅读该页面以了解基本信息。

| 导入               | `from pettingzoo.atari import entombed_cooperative_v3` |
|----------------------|--------------------------------------------------------|
| 动作类型           | 离散                                                   |
| 并行 API          | 支持                                                    |
| 手动控制          | 不支持                                                 |
| 智能体            | `agents= ['first_0', 'second_0']`                      |
| 智能体数量        | 2                                                      |
| 动作形状          | (1,)                                                   |
| 动作值范围        | [0,17]                                                 |
| 观察形状          | (210, 160, 3)                                          |
| 观察值范围        | (0,255)                                                |
| 平均总奖励        | 6.23                                                   |


活埋的合作版本是一个探索游戏，
你需要与队友合作，尽可能深入
迷宫。

你们两个都需要快速在一个不断生成的迷宫中导航，
而你只能看到其中的一部分。如果你被困住了，你就输了。
注意，你很容易发现自己陷入死胡同，只能通过使用稀有的能量提升道具来逃脱。
如果玩家通过使用这些能量提升道具互相帮助，他们可以坚持更久。注意，最佳协调要求智能体在地图的两侧，因为能量提升道具会出现在一侧或另一侧，但可以用来打破两侧的墙
（破坏是对称的，会影响屏幕的两半）。
此外，还有危险的僵尸潜伏在周围需要避开。

奖励的设计与单人游戏的奖励相同。具体来说，一个活埋关卡被分为 5 个不可见的区域。你在改变区域后或重置关卡后立即获得奖励。注意，这意味着当你失去一条生命时会获得奖励，
因为它会重置关卡，但当你失去最后一条生命时不会获得奖励，因为游戏会在关卡重置之前终止。


[官方活埋游戏手册](https://atariage.com/manual_html_page.php?SoftwareLabelID=165)


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

* v3：最小动作空间 (1.18.0)
* v2：对整个 API 进行重大更改，修复了活埋游戏的奖励 (1.4.0)
* v1：修复了所有环境处理过早死亡的方式 (1.3.0)
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
        game="entombed", num_players=2, mode_num=3, env_name=name, **kwargs
    )


env = base_env_wrapper_fn(raw_env)
parallel_env = parallel_wrapper_fn(env)
