import pandas as pd
import glob, os
from dateutil.parser import parse
from hinode_launch_date import hinode_launch_date
from int_to_roman import int_to_roman

opf = 'ints_synop.pickle'

# --- get JTM's synop intensities, one file for each line

filenames = glob.glob('ints_synop/*')
filenames = sorted(filenames)

# --- read all of the data into a data frame

names = ['date', 'intensity', 'sd', 'samples', 'max_samples', 'source']
for f in filenames:
    this_df = pd.read_csv(f, header=None, comment='#', names=names, delim_whitespace=True)

    # --- convert the dates to seconds from launch
    t_mission = [(parse(t)-parse(hinode_launch_date)).total_seconds() for t in this_df['date']]
    this_df.insert(1, 'mission_sec', t_mission, True)

    # --- for consistency add instrument 
    instrument = ['EIS' for n in range(len(this_df))]
    this_df.insert(2, 'instrument', instrument, True)

    # --- for consistency add element, ion, wave
    id = os.path.basename(f).split('_')
    element = id[0].capitalize()
    element = [element for n in range(len(this_df))]
    this_df.insert(3, 'element', element, True)
    ion = int_to_roman(id[1])
    ion = [ion for n in range(len(this_df))]
    this_df.insert(4, 'ion', ion, True)    
    wave = float(id[2] + '.' + id[3])
    wave = [wave]*len(this_df)
    this_df.insert(5, 'wave', wave, True)    

    if 'df' not in locals():
        df = this_df
    else:
        df = df.append(this_df)

print(df)

# --- output to pickle file
df.to_pickle(opf)
print(' + wrote to ' + opf)
