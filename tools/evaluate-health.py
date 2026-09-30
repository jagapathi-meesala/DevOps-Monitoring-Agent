from core.monitoring import evaluate_health


def run(payload):
    return evaluate_health(payload)
