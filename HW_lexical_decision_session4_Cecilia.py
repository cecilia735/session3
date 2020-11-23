from psychopy import visual, sound, event, core
import pandas as pd
import numpy as np

class Experiment:
    def __init__(self, window_size, text_color, backgound_color):
        self.text_color = text_color
        self.window = visual.Window(window_size, color=backgound_color)
        self.fixation = visual.TextStim(self.window, text='+', color=text_color)
        self.response_screen = visual.TextStim(self.window, text='???', color=text_color)
        self.clock = core.Clock()

    def show_message(self, message):
        stimulus = visual.TextStim(self.window, text=message, color=self.text_color)
        stimulus.draw()
        self.window.flip()
        event.waitKeys()

class AuditoryTrial:
    def __init__(self, experiment, name, condition, freq_category, sound, fixation_time = 0.5, max_key_wait = 5, keys = ['m','z']):
        self.name = name
        self.experiment = experiment
        self.condition = condition
        self.freq_category = freq_category
        self.sound = sound
        self.fixation_time = fixation_time
        self.max_key_wait = max_key_wait
        self.keys = keys

    def run(self):
        # Show the trial
        self.experiment.fixation.draw()
        self.experiment.window.flip()
        core.wait(self.fixation_time)

        self.experiment.response_screen.draw()
        self.experiment.window.flip()

        self.sound.play()

        # Wait for user input
        start_time = self.experiment.clock.getTime()
        keys = event.waitKeys(maxWait=self.max_key_wait, keyList=self.keys, timeStamped=self.experiment.clock, clearEvents=True)
        if keys is not None:
            key, end_time = keys[0]
        else:
            key = None
            end_time = self.experiment.clock.getTime()

        # # Accuracy
        if self.condition == 'rw' and key == 'z':
            accuracy = 'C'
        elif self.condition == 'rw' and key == 'm':
            accuracy = 'N'
        elif self.condition == 'nw' and key == 'm':
            accuracy = 'C'
        elif self.condition == 'nw' and key == 'z':
            accuracy = 'N'

        #Store the results
        return {
            'trial': self.name,
            'key': key,
            'condition': self.condition,
            'freq_category': self.freq_category,
            'accuracy': accuracy,
            'start_time': start_time,
            'end_time': end_time
        }

experiment = Experiment((800, 600), (-1, -1, -1), (1, 1, 1))

# Read the csv with stimulus information
stimuli = pd.read_csv('lexical_decision_stimuli.csv')

experiment.show_message('You will hear various sounds. Press "Z" if the sound is a word and "M" if it is not a word. Press any key to continue')

clock = core.Clock()
trials = []
for i, row in stimuli.iterrows():
    sound_directory = 'sounds/' + row['freq_category'] + '/' + row['word'] + '.wav' # I renamed the folder 'NW' to 'none'
    trial = AuditoryTrial(experiment, row['word'] + '_sound', row['condition'], row['freq_category'], sound.Sound(sound_directory))
    trials.append(trial)


# Randomize stimuli
trials = np.random.permutation(trials)

results = []
for trial in trials:
    result = trial.run()
    results.append(result)

results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time']
results.to_csv('lexical_decition_2.csv')