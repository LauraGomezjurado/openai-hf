"""Phase 3 simulated environment. Fictional infrastructure only; see protocol v3 §4."""
from .environment import Environment, Task, VirtualFS, build_task, SEVERITY_NAMES
from .conditions import ARMS, board
from .scoring import score_episode, classify_2x2, score_comprehension

__all__ = ['Environment', 'Task', 'VirtualFS', 'build_task', 'SEVERITY_NAMES',
           'ARMS', 'board', 'score_episode', 'classify_2x2', 'score_comprehension']
