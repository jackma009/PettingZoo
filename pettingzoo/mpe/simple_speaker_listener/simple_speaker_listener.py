"""
简单说听环境。

这个环境模拟了一个多智能体通信场景，包括说话者和听众，
通过语言交流来指导行动，实现信息传递和目标达成。

主要特点：
1. 通信交互
2. 角色分工
3. 信息传递
4. 协同行动

环境规则：
1. 基本设置
   - 说话者
   - 听众
   - 通信空间
   - 得分规则

2. 交互规则
   - 信息发送
   - 信息接收
   - 行动执行
   - 结果评估

3. 智能体行为
   - 信息编码
   - 信息解读
   - 行动规划
   - 目标追踪

4. 终止条件
   - 目标达成
   - 时间耗尽
   - 通信完成
   - 回合结束

环境参数：
- 观察空间：通信状态
- 动作空间：通信和移动选择
- 奖励：通信效果和目标完成度
- 最大步数：由时间限制决定

环境特色：
1. 通信系统
   - 信息编码
   - 信息传递
   - 噪声处理
   - 反馈机制

2. 角色机制
   - 说话职责
   - 听众职责
   - 信息流向
   - 行动响应

3. 策略元素
   - 信息选择
   - 表达方式
   - 理解准确
   - 行动配合

4. 评估系统
   - 通信效果
   - 理解程度
   - 行动准确
   - 整体表现

注意事项：
- 信息准确
- 表达清晰
- 理解到位
- 行动协调
"""
"""
# Simple Speaker Listener

```{figure} mpe_simple_speaker_listener.gif
:width: 140px
:name: simple_speaker_listener
```

This environment is part of the <a href='..'>MPE environments</a>. Please read that page first for general information.

| Import               | `from pettingzoo.mpe import simple_speaker_listener_v4` |
|----------------------|---------------------------------------------------------|
| Actions              | Discrete/Continuous                                     |
| Parallel API         | Yes                                                     |
| Manual Control       | No                                                      |
| Agents               | `agents=[speaker_0, listener_0]`                        |
| Agents               | 2                                                       |
| Action Shape         | (3),(5)                                                 |
| Action Values        | Discrete(3),(5)/Box(0.0, 1.0, (3)), Box(0.0, 1.0, (5))  |
| Observation Shape    | (3),(11)                                                |
| Observation Values   | (-inf,inf)                                              |
| State Shape          | (14,)                                                   |
| State Values         | (-inf,inf)                                              |


This environment is similar to simple_reference, except that one agent is the 'speaker' (gray) and can speak but cannot move, while the other agent is the listener (cannot speak, but must navigate to correct landmark).

Speaker observation space: `[goal_id]`

Listener observation space: `[self_vel, all_landmark_rel_positions, communication]`

Speaker action space: `[say_0, say_1, say_2, say_3, say_4, say_5, say_6, say_7, say_8, say_9]`

Listener action space: `[no_action, move_left, move_right, move_down, move_up]`

### Arguments

``` python
simple_speaker_listener_v4.env(max_cycles=25, continuous_actions=False, dynamic_rescaling=False)
```



`max_cycles`:  number of frames (a step for each agent) until game terminates

`continuous_actions`: Whether agent action spaces are discrete(default) or continuous

`dynamic_rescaling`: Whether to rescale the size of agents and landmarks based on the screen size

"""

import numpy as np
from gymnasium.utils import EzPickle

from pettingzoo.mpe._mpe_utils.core import Agent, Landmark, World
from pettingzoo.mpe._mpe_utils.scenario import BaseScenario
from pettingzoo.mpe._mpe_utils.simple_env import SimpleEnv, make_env
from pettingzoo.utils.conversions import parallel_wrapper_fn


class raw_env(SimpleEnv, EzPickle):
    def __init__(
        self,
        max_cycles=25,
        continuous_actions=False,
        render_mode=None,
        dynamic_rescaling=False,
    ):
        EzPickle.__init__(
            self,
            max_cycles=max_cycles,
            continuous_actions=continuous_actions,
            render_mode=render_mode,
        )
        scenario = Scenario()
        world = scenario.make_world()
        SimpleEnv.__init__(
            self,
            scenario=scenario,
            world=world,
            render_mode=render_mode,
            max_cycles=max_cycles,
            continuous_actions=continuous_actions,
            dynamic_rescaling=dynamic_rescaling,
        )
        self.metadata["name"] = "simple_speaker_listener_v4"


env = make_env(raw_env)
parallel_env = parallel_wrapper_fn(env)


class Scenario(BaseScenario):
    def make_world(self):
        world = World()
        # set any world properties first
        world.dim_c = 3
        num_landmarks = 3
        world.collaborative = True
        # add agents
        world.agents = [Agent() for i in range(2)]
        for i, agent in enumerate(world.agents):
            agent.name = "speaker_0" if i == 0 else "listener_0"
            agent.collide = False
            agent.size = 0.075
        # speaker
        world.agents[0].movable = False
        # listener
        world.agents[1].silent = True
        # add landmarks
        world.landmarks = [Landmark() for i in range(num_landmarks)]
        for i, landmark in enumerate(world.landmarks):
            landmark.name = "landmark %d" % i
            landmark.collide = False
            landmark.movable = False
            landmark.size = 0.04
        return world

    def reset_world(self, world, np_random):
        # assign goals to agents
        for agent in world.agents:
            agent.goal_a = None
            agent.goal_b = None
        # want listener to go to the goal landmark
        world.agents[0].goal_a = world.agents[1]
        world.agents[0].goal_b = np_random.choice(world.landmarks)
        # random properties for agents
        for i, agent in enumerate(world.agents):
            agent.color = np.array([0.25, 0.25, 0.25])
        # random properties for landmarks
        world.landmarks[0].color = np.array([0.65, 0.15, 0.15])
        world.landmarks[1].color = np.array([0.15, 0.65, 0.15])
        world.landmarks[2].color = np.array([0.15, 0.15, 0.65])
        # special colors for goals
        world.agents[0].goal_a.color = world.agents[0].goal_b.color + np.array(
            [0.45, 0.45, 0.45]
        )
        # set random initial states
        for agent in world.agents:
            agent.state.p_pos = np_random.uniform(-1, +1, world.dim_p)
            agent.state.p_vel = np.zeros(world.dim_p)
            agent.state.c = np.zeros(world.dim_c)
        for i, landmark in enumerate(world.landmarks):
            landmark.state.p_pos = np_random.uniform(-1, +1, world.dim_p)
            landmark.state.p_vel = np.zeros(world.dim_p)

    def benchmark_data(self, agent, world):
        # returns data for benchmarking purposes
        return self.reward(agent, world)

    def reward(self, agent, world):
        # squared distance from listener to landmark
        a = world.agents[0]
        dist2 = np.sum(np.square(a.goal_a.state.p_pos - a.goal_b.state.p_pos))
        return -dist2

    def observation(self, agent, world):
        # goal color
        goal_color = np.zeros(world.dim_color)
        if agent.goal_b is not None:
            goal_color = agent.goal_b.color

        # get positions of all entities in this agent's reference frame
        entity_pos = []
        for entity in world.landmarks:
            entity_pos.append(entity.state.p_pos - agent.state.p_pos)

        # communication of all other agents
        comm = []
        for other in world.agents:
            if other is agent or (other.state.c is None):
                continue
            comm.append(other.state.c)

        # speaker
        if not agent.movable:
            return np.concatenate([goal_color])
        # listener
        if agent.silent:
            return np.concatenate([agent.state.p_vel] + entity_pos + comm)
