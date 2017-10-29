import pandas as pd
import pickle
import quandl
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

api_key = open('quandl.txt', 'r').read()


def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')

    return fiddy_states[0][0][1:]


def grab_initial_state_data():
    states = state_list()
    main_df = pd.DataFrame()

    for abbr in states:
        query = "FMAC/HPI_" + str(abbr)
        df = quandl.get(query, authtoken=api_key)
        # df = df.pct_change()
        df[abbr] = (df[abbr] - df[abbr][0]) / df[abbr][0] * 100.0

        if main_df.empty:
            main_df = df

        else:
            main_df = main_df.join(df)
    print(main_df.head())

    pickle_out = open('fiddy_states.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()


def HPI_benchmark():
    df = quandl.get('FMAC/HPI_USA', authtoken=api_key)
    df["United States"] = (df["United States"] - df["United States"][0]) / df["United States"][0] * 100.0
    return df


# grab_initial_state_data()
fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))
HPI_data = pd.read_pickle('fiddy_states3.pickle')
# benchmark = HPI_benchmark()
#
# HPI_data.plot(ax=ax1)
# benchmark.plot(ax=ax1, color='k', linewidth=10)

# # pickle_in = open('fiddy_states.pickle', 'rb')
# #
# # HPI_data = pickle.load(pickle_in)
# #
# # print(HPI_data)
# #
# HPI_data.to_pickle('data.pickle')
# # HPI_data2 = pd.read_pickle('data.pickle')
# # print(HPI_data2)
#
# HPI_data['TX'] = HPI_data['TX'] * 2
#
# print(HPI_data['TX'])

# HPI_data.plot()
# plt.legend().remove()
# plt.show()

HPI_state_correlation = HPI_data.corr()
print(HPI_state_correlation)
print(HPI_state_correlation.describe())
