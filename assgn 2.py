# import libraries
import pandas as pd
import numpy as np

# a function that generates bootstrap replicate of 1d data
def bootstrap_replicate_1d(data, func):
    bs_sample = np.random.choice(data, size=len(data))
    return func(bs_sample)

# define a function that draws bootstrap replicates
def draw_bs_reps(data, func, size=1):
    # initialize array of replicates
    bs_replicates = np.empty(size)
    # generate replicates
    for i in range(size):
        bs_replicates[i] = bootstrap_replicate_1d(data, func)
    return bs_replicates

if __name__ == '__main__':
    # read the file and skip the first 3 rows
    df = pd.read_csv('gandhi_et_al_bouts.csv', skiprows = 3)
    
    # create two empty lists
    bout_lengths_wt = []
    bout_lengths_mut = []
    # append bout lengths of wt and of mut into the lists
    for i in range(len(df)):
        if df.index[i][0] == 'wt':
            bout_lengths_wt.append(float(df.index[i][1]))
        elif df.index[i][0] == 'mut':
            bout_lengths_mut.append(float(df.index[i][1]))

    # convert the lists to arrays using np.array and
    # change the list of strings to numeric type using .astype(np.float)
    bout_lengths_wt = np.array(bout_lengths_wt).astype(np.float)
    bout_lengths_mut = np.array(bout_lengths_mut).astype(np.float)

    # compute the mean active bout lengths using np.mean
    mean_wt = np.mean(bout_lengths_wt)
    mean_mut = np.mean(bout_lengths_mut)

    # draw 10000 boostrap replicates
    bs_reps_wt = draw_bs_reps(bout_lengths_wt, np.mean, size=10000)
    bs_reps_mut = draw_bs_reps(bout_lengths_mut, np.mean, size=10000)

    # compute 95% confidence interval
    conf_int_wt = np.percentile(bs_reps_wt, [2.5, 97.5])
    conf_int_mut = np.percentile(bs_reps_mut, [2.5, 97.5])

    # show the results
    print("""
    wt:  mean = {0:.3f} min., conf. int. = [{1:.1f}, {2:.1f}] min.
    mut: mean = {3:.3f} min., conf. int. = [{4:.1f}, {5:.1f}] min.
    """.format(mean_wt, *conf_int_wt, mean_mut, *conf_int_mut))
