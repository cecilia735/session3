import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotnine as gg
from plotnine import ggplot

# Task was done by a beginner Dutch speaker
participants = [1, 2] # create list with participants

trials = pd.DataFrame()
for participant in participants:
    trials_per_participant = pd.read_csv(f'lexical_decition_{participant}.csv')
    trials_per_participant['participant_id'] = participant

    trials_per_participant['accuracy'] = trials_per_participant['accuracy'].str.replace('C', '1')
    trials_per_participant['accuracy'] = trials_per_participant['accuracy'].str.replace('N', '0')
    trials_per_participant['accuracy'] = trials_per_participant['accuracy'].astype(int)

    trials = trials.append(trials_per_participant)


trials.rename(columns={'Unnamed: 0': 'trial_order'}, inplace=True)
trials.to_csv('lexical_decision_merged.csv')

summary = trials.groupby(by=['condition', 'freq_category']).aggregate(
    mean_RT = pd.NamedAgg('reaction_time', np.mean),
    std_RT = pd.NamedAgg('reaction_time', np.std),
    mean_accuracy = pd.NamedAgg('accuracy', np.mean),
    std_accuracy = pd.NamedAgg('accuracy', np.std),
)
summary.reset_index(inplace=True)
print('Summary for all participants')
print(summary)

summary_per_participant = trials.groupby(by=['participant_id', 'freq_category']).agg(np.mean)
summary_per_participant .reset_index(inplace=True)
print('Summary per participant')
print(summary_per_participant )

plot = (ggplot(gg.aes(x='freq_category', y='reaction_time'), data=trials) +
        gg.geom_boxplot(gg.aes(fill='freq_category')) + # of jitter
        gg.facet_wrap('participant_id')
        )
plot.draw()
plt.show()

plot = (ggplot(gg.aes(x="freq_category", weight='accuracy'), summary_per_participant ) +
        gg.geom_bar() +
        gg.facet_wrap(['participant_id'])
        )
plot.draw()
plt.show()

plot = (ggplot(gg.aes(x='freq_category', y='reaction_time'), data=trials) +
        gg.geom_boxplot(gg.aes(fill='freq_category')) # of jitter
        )
plot.draw()
plt.show()


plot = (ggplot(gg.aes(x="freq_category", weight='accuracy'), summary_per_participant ) +
        gg.geom_bar()
        )
plot.draw()
plt.show()