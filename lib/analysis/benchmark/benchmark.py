from lib.analysis.benchmark.evaluate import get_performance_new

MOTOR_THRESHOLD = 0.8
TRAINING_1_THRESHOLD = 0.94
TRAINING_2_THRESHOLD = 0.65

def benchmark(stage, choices, leftP):
    perf = get_performance_new(choices=choices, leftP=leftP, mode=stage)
    print(f'performance: {perf}')

    if 'motor_training' in stage:
        if perf > MOTOR_THRESHOLD:
            return True
    
    if 'training_1' in stage:
        if perf > TRAINING_1_THRESHOLD:
            return True

    if 'training_2' in stage:
        if perf > TRAINING_2_THRESHOLD:
            return True

    return False