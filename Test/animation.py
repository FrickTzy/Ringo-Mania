from time import sleep


def smooth_in_animation(seconds_time: float):
    if seconds_time <= .5:
        return 2 * seconds_time * seconds_time
    seconds_time -= .5
    return 2 * seconds_time * (1 - seconds_time) + .5


seconds = 0
total_output = 255

while seconds < 1.01:
    print(format(smooth_in_animation(seconds_time=seconds) * total_output, ".2f"))
    seconds += .02
