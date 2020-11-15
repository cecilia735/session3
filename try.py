from psychopy import visual, sound, event, core
import pandas as pd

window = visual.Window((400, 400), color=(1, 1, 1))
fixation = visual.TextStim(window, text='+', color=(-1, -1, -1))

# fixation.draw()
# window.flip()
# core.wait(1.0)

# gabor = visual.GratingStim(window, tex='sin', mask='gauss', sf=10, name='gabor')
# gabor.draw()
# window.flip()
# core.wait(2.0)
#
# image = visual.ImageStim(window, image='session3/images/car.png')
# image.draw()
# window.flip()
# core.wait(2.0)
#
# audio = sound.Sound('session3/sounds/HF/auto.wav')
# fixation.draw()
# window.flip()
# audio.play()
# core.wait(audio.getDuration()) # plays for duration of the sound file
#
# # Different timing methods
# clock = core.Clock()
# while clock.getTime() < 2:
#     fixation.draw()
#     window.flip()
# print(clock.getTime()) # In seconds

# # For really precise timing don't scericy the timing in seconds but in frames
# window.flip()
# clock = core.Clock()
# for i in range(100):
#     fixation.draw()
#     window.flip()
# print(clock.getTime()) # In seconds

# # User imput
# clock = core.Clock()
# keys = event.waitKeys(maxWait=5, keyList=['z', 'm'], timeStamped=clock)
# if keys is not None:
#     key, reaction_time = keys[0]
# else:
#     key = None
#     reaction_time = 5
# print(f'{key} was pressed after {reaction_time} seconds')

stimuli = pd.read_csv('/Users/Cecilia/Desktop/python/session_3/session3/picture_verification_stimuli.csv')
print(stimuli)

images = []
for image in stimuli['image_file']:
    images.append(visual.ImageStim(window,image=image))

for image in images:
    fixation.draw()
    window.flip()
    core.wait(0.5)

    image.draw()
    window.flip()
    core.wait(1.0)