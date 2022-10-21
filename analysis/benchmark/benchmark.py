from analysis.benchmark.evaluate import get_performance_new

MOTOR_THRESHOLD = 0.8
TRAINING_1_THRESHOLD = 0.63
TRAINING_2_THRESHOLD = 0.65

def benchmark(stage, choices, leftP):
    perf = get_performance_new(choices=choices, leftP=leftP, mode=stage)
    print(f'performance: {perf}')

    if stage == 'motor_training':
        if perf > MOTOR_THRESHOLD:
            return True
    
    if stage == 'training_1':
        if perf > TRAINING_1_THRESHOLD:
            return True

    if stage == 'training_2':
        if perf > TRAINING_2_THRESHOLD:
            return True

    return False