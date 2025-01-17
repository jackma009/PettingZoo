# noqa: D212, D415
"""
# 迷宫狂热（Maze Craze）

```{figure} atari_maze_craze.gif
:width: 140px
:name: maze_craze
```

此环境是<a href='..'>Atari 环境</a>的一部分。请先阅读该页面以了解基本信息。

| 导入               | `from pettingzoo.atari import maze_craze_v3` |
|----------------------|----------------------------------------------|
| 动作类型           | 离散                                         |
| 并行 API          | 支持                                          |
| 手动控制          | 不支持                                       |
| 智能体            | `agents= ['first_0', 'second_0']`            |
| 智能体数量        | 2                                            |
| 动作形状          | (1,)                                         |
| 动作值范围        | [0,17]                                       |
| 观察形状          | (250, 160, 3)                                |
| 观察值范围        | (0,255)                                      |


一个考验记忆力和规划能力的竞技游戏！

这是一场离开迷宫的竞赛。游戏有 3 个主要版本。

1. **竞赛**：游戏的基本版本。第一个离开迷宫的玩家获胜
2. **强盗**：有 2 个强盗在迷宫中随机移动。如果你被强盗抓住，你就输了，获得 -1 奖励，并且游戏结束。没有被抓住的玩家不会获得任何奖励，但他们仍然可以离开迷宫并获胜，得到 +1 奖励。
3. **捕获**：每个玩家必须在能够离开迷宫之前捕获所有 3 个强盗。此外，你可以通过创建一个看起来与迷宫墙壁相同的障碍物来迷惑你的对手（如果你不小心，也会迷惑你自己！），所有玩家都可以穿过这个障碍物。你一次只能
创建一面墙，当你创建新的墙时，旧的墙会消失。

第一个离开迷宫的玩家得到 +1 分，另一个玩家得到 -1 分（除非该玩家在强盗模式下已经被抓住）。

[官方迷宫狂热手册](https://atariage.com/manual_html_page.php?SoftwareLabelID=295)。注意，模式表中有一些不准确的地方。特别是，游戏模式 12 启用了障碍物功能，而不是模式 11。

#### 环境参数

一些环境参数是所有 Atari 环境通用的，在[基础 Atari 文档](../atari)中有描述。

迷宫狂热特有的参数如下：

``` python
maze_craze_v3.env(game_version="robbers", visibilty_level=0)
```

`game_version`：可选项为 "robbers"、"race"、"capture"，对应上述 3 个游戏版本

`visibilty_level`：一个从 0-3 的数字。设置为 0 表示地图 100% 可见，3 表示地图 0% 可见。

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
* v2：对整个 API 进行重大更改 (1.4.0)
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

avaliable_versions = {
    "robbers": 2,
    "race": 1,
    "capture": 12,
}


def raw_env(game_version="robbers", visibilty_level=0, **kwargs):
    assert (
        game_version in avaliable_versions
    ), f"`game_version` parameter must be one of {avaliable_versions.keys()}"
    assert (
        0 <= visibilty_level < 4
    ), "visibility level must be between 0 and 4, where 0 is 100% visibility and 3 is 0% visibility"
    base_mode = (avaliable_versions[game_version] - 1) * 4
    mode = base_mode + visibilty_level
    name = os.path.basename(__file__).split(".")[0]
    parent_file = glob(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), name + "*.py")
    )
    version_num = parent_file[0].split("_")[-1].split(".")[0]
    name = name + "_" + version_num
    return BaseAtariEnv(
        game="maze_craze",
        num_players=2,
        mode_num=mode,
        env_name=name,
        **kwargs,
    )


env = base_env_wrapper_fn(raw_env)
parallel_env = parallel_wrapper_fn(env)
