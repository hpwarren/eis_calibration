import pandas as pd
import datetime, glob, os
from dateutil.parser import parse
from hinode_launch_date import hinode_launch_date

opf = 'ints_full_ccd.pickle'

# --- get the full ccd intensities, one file for each raster

filenames = glob.glob('ints_full_ccd/*')
filenames = sorted(filenames)

# --- read each intensity file and append to data frame

names = ['instrument', 'element', 'ion', 'wave', 'intensity', 'sd']
for f in filenames:
    this_df = pd.read_csv(f, header=None, comment='#', names=names, delim_whitespace=True)

    # --- we need the time for these observations, parse filename and convert
    t_iso = os.path.basename(f)
    format = '%Y%m%d_%H%M%S.%f'
    t_iso = datetime.datetime.strptime(t_iso[7:22]+'.000', format).isoformat('T', 'milliseconds')
    # --- compute the seconds from the start of the mission
    t_mission = (parse(t_iso) - parse(hinode_launch_date)).total_seconds()

    # --- replicate dates and insert into frame
    t_iso = [t_iso for n in range(len(this_df))]
    t_mission = [t_mission for n in range(len(this_df))]
    this_df.insert(0, 'date', t_iso, True)
    this_df.insert(1, 'mission_sec', t_mission, True)

    if 'df' not in locals():
        df = this_df
    else:
        df = df.append(this_df)

print(df)        

# --- output to pickle file
df.to_pickle(opf)
print(' + wrote to ' + opf)


