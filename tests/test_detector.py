from src.detector import ZScoreDetector


def test_flat_then_spike_is_flagged():
    det = ZScoreDetector()
    for i in range(30):
        det.score(40.0 + (i % 3) * 0.5)      
    z, flagged, sev = det.score(80.0)
    assert flagged is True
    assert sev is not None


def test_normal_reading_not_flagged():
    det = ZScoreDetector()
    for i in range(30):
        det.score(40.0 + (i % 3) * 0.5)
    z, flagged, sev = det.score(40.5)
    assert flagged is False