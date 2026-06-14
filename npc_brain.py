import numpy as np
import config

DIRS = ["UP", "DOWN", "LEFT", "RIGHT"]

class NPCBrain:
    def __init__(self):
        # 4 LIF neurons — one per direction
        self.membrane  = np.zeros(4, dtype=np.float32)
        self.weights   = np.ones(4,  dtype=np.float32) * 0.1
        self.history   = []
        self.stage     = 1
        self.fired     = np.zeros(4, dtype=np.float32)
        self.spike_log = []

    def record_move(self, direction):
        self.history.append(direction)
        self._update_stage()
        self._stdp_update(direction)

    def _update_stage(self):
        n = len(self.history)
        if n >= config.SPIKE_WINDOW * 2:
            self.stage = 3
        elif n >= config.SPIKE_WINDOW:
            self.stage = 2
        else:
            self.stage = 1

    def _stdp_update(self, direction):
        if direction in DIRS:
            idx = DIRS.index(direction)
            self.weights[idx] = min(1.0, self.weights[idx] + 0.08)

    def predict_player_move(self):
        if self.stage == 1 or not self.history:
            return None

        # Build spike input from move frequency
        spike_input = np.zeros(4, dtype=np.float32)
        recent = self.history[-20:]
        for d in recent:
            if d in DIRS:
                spike_input[DIRS.index(d)] += 1.0
        spike_input /= (max(spike_input.sum(), 1))

        # Leak
        self.membrane *= (1.0 - 1.0 / config.LIF_TAU)

        # Accumulate with learned weights
        self.membrane += spike_input * self.weights

        # Fire
        self.fired = (self.membrane >= config.LIF_THRESHOLD).astype(np.float32)
        self.membrane[self.fired > 0] = 0.0

        self.spike_log.append(self.fired.copy())
        if len(self.spike_log) > 50:
            self.spike_log.pop(0)

        best = int(np.argmax(self.membrane + self.fired * 2))
        return DIRS[best]

    def get_stage(self):
        return self.stage

    def get_spike_rate(self):
        if not self.spike_log:
            return 0
        return int(np.sum(self.spike_log))

    def get_confidence(self):
        if self.membrane.sum() == 0:
            return 0
        return min(100, int(np.max(self.membrane) * 40))

    def get_membrane(self):
        return self.membrane.copy()

    def get_weights(self):
        return self.weights.copy()