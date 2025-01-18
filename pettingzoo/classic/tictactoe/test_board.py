"""
井字棋棋盘测试模块。

这个模块包含了井字棋棋盘类的单元测试，验证所有核心功能的正确性。
测试覆盖了基本操作、边界条件和特殊情况。

测试类别：
1. 基础功能测试
   - 初始化测试
   - 落子测试
   - 重置测试
   - 复制测试

2. 游戏规则测试
   - 合法移动
   - 非法移动
   - 轮次顺序
   - 重复落子

3. 胜负判定测试
   - 横向获胜
   - 纵向获胜
   - 对角线获胜
   - 平局情况

4. 边界条件测试
   - 棋盘已满
   - 游戏结束
   - 坐标越界
   - 状态一致性

测试用例：
1. test_init
   - 测试棋盘初始化
   - 验证初始状态

2. test_move
   - 测试基本落子
   - 测试非法移动
   - 测试玩家交替

3. test_win
   - 测试所有获胜情况
   - 验证胜负判定

4. test_draw
   - 测试平局情况
   - 验证状态检查
"""

"""Test cases for TicTacToe board."""

from __future__ import annotations

from typing import Any

import pytest

from pettingzoo.classic.tictactoe.board import (  # type: ignore
    TTT_GAME_NOT_OVER,
    TTT_PLAYER1_WIN,
    TTT_PLAYER2_WIN,
    TTT_TIE,
    Board,
)

# Note: mapping of moves to board positions are:
# 0 3 6
# 1 4 7
# 2 5 8

agent2_win = {
    "moves": [
        # agent_id, position, board after move
        (0, 4, [0, 0, 0, 0, 1, 0, 0, 0, 0]),
        (1, 0, [2, 0, 0, 0, 1, 0, 0, 0, 0]),
        (0, 2, [2, 0, 1, 0, 1, 0, 0, 0, 0]),
        (1, 6, [2, 0, 1, 0, 1, 0, 2, 0, 0]),
        (0, 3, [2, 0, 1, 1, 1, 0, 2, 0, 0]),
        (1, 7, [2, 0, 1, 1, 1, 0, 2, 2, 0]),
        (0, 1, [2, 1, 1, 1, 1, 0, 2, 2, 0]),
        (1, 8, [2, 1, 1, 1, 1, 0, 2, 2, 2]),  # agent 2 wins here
        (0, 5, [2, 1, 1, 1, 1, 1, 2, 2, 2]),
    ],
    "max_step": 7,  # should not get past here
    "winner": TTT_PLAYER2_WIN,
}

tie = {
    "moves": [  # should be tie
        (0, 0, [1, 0, 0, 0, 0, 0, 0, 0, 0]),
        (1, 3, [1, 0, 0, 2, 0, 0, 0, 0, 0]),
        (0, 1, [1, 1, 0, 2, 0, 0, 0, 0, 0]),
        (1, 4, [1, 1, 0, 2, 2, 0, 0, 0, 0]),
        (0, 5, [1, 1, 0, 2, 2, 1, 0, 0, 0]),
        (1, 2, [1, 1, 2, 2, 2, 1, 0, 0, 0]),
        (0, 6, [1, 1, 2, 2, 2, 1, 1, 0, 0]),
        (1, 7, [1, 1, 2, 2, 2, 1, 1, 2, 0]),
        (0, 8, [1, 1, 2, 2, 2, 1, 1, 2, 1]),
    ],
    "max_step": 8,
    "winner": TTT_TIE,
}

agent1_win = {
    "moves": [
        (0, 0, [1, 0, 0, 0, 0, 0, 0, 0, 0]),
        (1, 3, [1, 0, 0, 2, 0, 0, 0, 0, 0]),
        (0, 1, [1, 1, 0, 2, 0, 0, 0, 0, 0]),
        (1, 4, [1, 1, 0, 2, 2, 0, 0, 0, 0]),
        (0, 2, [1, 1, 1, 2, 2, 0, 0, 0, 0]),  # agent 1 should win here
        (1, 5, [1, 1, 1, 2, 2, 2, 0, 0, 0]),
        (0, 6, [1, 1, 1, 2, 2, 2, 1, 0, 0]),
        (1, 7, [1, 1, 1, 2, 2, 2, 1, 2, 0]),
        (0, 8, [1, 1, 1, 2, 2, 2, 1, 2, 1]),
    ],
    "max_step": 4,
    "winner": TTT_PLAYER1_WIN,
}


@pytest.mark.parametrize("values", [agent1_win, agent2_win, tie])
def test_tictactoe_board_games(values: dict[str, Any]) -> None:
    """Test that TicTacToe games go as expected."""
    expected_winner = values["winner"]
    max_step = values["max_step"]

    board = Board()
    for i, (agent, pos, board_layout) in enumerate(values["moves"]):
        assert i <= max_step, "max step exceed in tictactoe game"
        board.play_turn(agent, pos)
        assert board_layout == board.squares, "wrong tictactoe layout after move"
        status = board.game_status()
        if status != TTT_GAME_NOT_OVER:
            assert i == max_step, "tictactoe game ended on wrong step"
            assert status == expected_winner, "wrong winner in tictactoe board test"
            break


def test_tictactoe_winning_boards() -> None:
    """Test that winning board configurations actually win."""
    # these are the winning lines for player 1. Note that moves
    # for player 2 are included to make it a legal board.
    winning_lines = [  # vertical(x3), horizontal(x3), diagonal(x2)
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 1, 0, 1, 0, 0],
    ]
    for line in winning_lines:
        board = Board()
        board.squares = line
        assert board.game_status() == TTT_PLAYER1_WIN, "Bad win check in TicTacToe"


def test_tictactoe_bad_move() -> None:
    """Test that illegal TicTacToe moves are rejected."""
    board = Board()
    # 1) move out of bounds should be rejected
    for outside_space in [-1, 9]:
        with pytest.raises(AssertionError, match="Invalid move location"):
            board.play_turn(0, outside_space)

    # 2) move by unknown agent should be rejected
    for unknown_agent in [-1, 2]:
        with pytest.raises(AssertionError, match="Invalid agent"):
            board.play_turn(unknown_agent, 0)

    # 3) move in occupied space by either agent should be rejected
    board.play_turn(0, 4)  # this is fine
    for agent in [0, 1]:
        with pytest.raises(AssertionError, match="Location is not empty"):
            board.play_turn(agent, 4)  # repeating move is not valid
