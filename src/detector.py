from collections import deque
import statistics


class ZScoreDetector:
    """Streaming anomaly detector: compares each reading with the previous `window` readings."""

    def __init__(self, window=12, threshold=5.0, high=30.0, medium=10.0):
        self.window = window
        self.threshold = threshold
        self.medium = medium   
        self.high = high          
        self.history = deque(maxlen=window)

    def score(self, value):
        """Return (zscore, is_anomaly, severity) for one new reading."""
        if len(self.history) < self.window:
            self.history.append(value)
            return 0.0, False, None

        mean = statistics.fmean(self.history)
        std = statistics.stdev(self.history)
        z = 0.0 if std == 0 else (value - mean) / std
        self.history.append(value)

        if abs(z) <= self.threshold:
            return z, False, None
        if abs(z) >= self.high:
            return z, True, "HIGH"
        if abs(z) >= self.medium:
            return z, True, "MEDIUM"
        return z, True, "LOW"