from analysis.benchmark.evaluate import get_performance_new

MOTOR_THRESHOLD = 0.8
TRAINING_1_THRESHOLD = 0.4
TRAINING_2_THRESHOLD = 0.3

def benchmark(stage, choices, leftP):
    perf = get_performance_new(choices=choices, leftP=leftP, mode=stage)

    if 'motor' in stage:
        if perf > MOTOR_THRESHOLD:
            return True
    
    if '1' in stage:
        if perf > TRAINING_1_THRESHOLD:
            return True

    if '2' in stage:
        if perf > TRAINING_2_THRESHOLD:
            return True

    return False