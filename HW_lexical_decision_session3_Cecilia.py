from psychopy import visual, sound, event, core
import pandas as pd
import numpy as np

# Read the csv with stimulus information

stimuli = pd.read_csv('lexical_decision_stimuli.csv')
print(stimuli)

# Randomize stimuli
stimuli = stimuli.iloc[np.random.permutation(len(stimuli))]
print(stimuli)

# Set up for experiment
window = visual.Window((400, 400), color=(1, 1, 1))
fixation = visual.TextStim(window, text='+', color=(-1, -1, -1))
response_screen = visual.TextStim(window, text='? ? ?', color=(-1, -1, -1))

# Present instructions
instructions = visual.TextStim(window, text='You will hear various sounds. Press "Z" if the sound is a word and "M" if it is not a word. Press any key to continue', color=(-1, -1, -1))
instructions.draw()
window.flip()
keys = event.waitKeys()

# Load sound files
sounds = []
for i, row in stimuli.iterrows():
    sound_directory = 'sounds/' + row['freq_category'] + '/' + row['word'] + '.wav' # I renamed the folder 'NW' to 'none'
    sounds.append(sound.Sound(sound_directory))
print(sounds)

# Present trials
results = []
i = 0
for sound in sounds[:20]: # use 'sounds[:5]' to test
    # Show trial
    fixation.draw()
    window.flip()
    core.wait(0.5)

    response_screen.draw()
    window.flip()

    sound.play()

    # Record a response
    clock = core.Clock()
    keys = event.waitKeys(maxWait=5, keyList=['z', 'm'], timeStamped=clock)
    if keys is not None:
        key, reaction_time = keys[0]
    else:
        key = None
        reaction_time = 5

    # Accuracy
    if stimuli["condition"].iloc[i] == 'rw' and key == 'z':
        accuracy = 'C'
    elif stimuli["condition"].iloc[i] == 'rw' and key == 'm':
        accuracy = 'N'
    elif stimuli["condition"].iloc[i] == 'nw' and key == 'm':
        accuracy = 'C'
    elif stimuli["condition"].iloc[i] == 'nw' and key == 'z':
        accuracy = 'N'

    # Store the results
    results.append({
        'sound': stimuli["word"].iloc[i],
        'condition': stimuli["condition"].iloc[i],
        'accuracy': accuracy,
        'key': key,
        'reaction_time': reaction_time
    })

    i = i + 1

# Convert results to df
results = pd.DataFrame(results)
print(results)

# Save results
results.to_csv('results.csv')