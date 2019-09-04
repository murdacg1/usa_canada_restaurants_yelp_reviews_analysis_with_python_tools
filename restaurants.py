import pandas as pd
from pandas.plotting import scatter_matrix
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import warnings
warnings.filterwarnings("ignore")
#%matplotlib inline 

def read_csv_file(csvfile, message):
    '''
    Reading in the dataframe from a csv file
    '''
    print()
    print(message)
    print('csvfile: ', csvfile)
    print()
    df = pd.read_csv(csvfile)
    return df

def inspect_data(df, message, head_lines=3, tail_lines=3):
    '''
    Inspecting the (geo)dataframe
    '''
    print()
    print(message); print()
    print('df.shape:')
    print(df.shape); print()
    print('df.info():')
    print(df.info()); print()
    if head_lines > 0:
        print('df.head(head_lines):')
        print(df.head(head_lines)); print()
    if tail_lines > 0:
        print('df.tail(tail_lines):')
        print(df.tail(tail_lines)); print()
    print()

def stats_on_columns(df, message, columns):
    '''
    Obtain simple statistics on selected columns in the (geo)dataframe
    '''
    print()
    print(message); print()
    print(df[columns].describe()); print()

def plot_histogram(df, message, column):
    '''
    Plot histograms on one selected column in the (geo)dataframe
    '''
    print()
    print(message); print()
    print("column: ", column)
    df[column].hist(label = column, bins = 50, figsize=(10,6), alpha=0.5)
#    plt.xlabel('column')
#    plt.ylabel('counts')
    plt.legend()
    plt.show()
    plt.clf()
    plt.cla()
    plt.close()

def plot_kde(df, message, column):
    '''
    Plot kde (analogous to an optimized histogram with an automatic bin size) on one selected column in the (geo)dataframe
    '''
    print()
    print(message); print()
    print("column: ", column)
    df[column].plot.kde(figsize=(10,6), alpha=0.5)
#    plt.xlabel('column')
#    plt.ylabel('counts')
    plt.legend()
    plt.show()
    plt.clf()
    plt.cla()
    plt.close()

def get_scatter_matrix(df, message, columns):
    '''
    Use scatter_matrix to see if there are correlations between the columns in the (geo)dataframe
    '''
    print()
    print(message); print()
    scatter_matrix(df[columns], figsize=(10,10), alpha=0.5)
    plt.show()
    plt.clf()
    plt.cla()
    plt.close()
    
def get_freq(thelist, message): 
    '''
    Construct a dictionary to count occurences for each unique key; thelist is a column of a (geo)dataframe
    ''' 
    print()
    print(message); print()
    freq_dict = {} 
    for item in thelist: 
        if item in freq_dict: 
            freq_dict[item] += 1
        else: 
            freq_dict[item] = 1
    return freq_dict

def apply_thresholds(df, message, dict):
    '''
    Apply thresholds to the (geo)dataframe
    '''
    print()
    print(message); print()
    stars = dict.get('stars', 0.0)
    review_count = dict.get('review_count', 0)
#   if df['state'] != 'AR':
    df = df[df['stars'] >= stars]
    df = df[df['review_count'] >= review_count]
    return df

def do_cycle(gdf, cycle, thresh_dict, message):
    '''
    A cycle of doing steps of looking at the data after applying threshold(s)
    '''
    head_lines=0
    tail_lines=0

    print()
    print(message); print()
    print('cycle: ', cycle)
    message = 'Inspect the data before applying the thresholds:'
    inspect_data(gdf, message, head_lines, tail_lines)

    message = 'Apply the thresholds:'
    gdf = apply_thresholds(gdf, message, thresh_dict)

    message = 'Re-inspect the data after applying the thresholds:'
    inspect_data(gdf, message, head_lines, tail_lines)

    columns = ['review_count', 'stars']
    message = 'Statistics for some columns:'
    stats_on_columns(gdf, message, columns)

    message = 'Use scatter_matrix to see the histograms and also to see if there are correlations between the columns:'
    get_scatter_matrix(gdf, message, columns)
    message = 'Get some simple statistics and plot histograms for some columns:'
    columns = ['review_count', 'stars']

    message = 'Construct a dictionary to count number restaurants in each unique state/province'
#   gdf.sort_values(by=['state'])
    states_dict = get_freq(gdf['state'], message)
    print(states_dict)
    print()

    message = 'Geographical distribution:'
    print(message)
    ax = usa1_can1.plot(color='white', edgecolor='black', figsize=(20,12))
    gdf.plot(ax=ax, color='red', markersize=50)
    plt.show()
    plt.clf()
    plt.cla()
    plt.close()
    print()
    return gdf


'''
main routine
'''

print()
print()
print('---Start the analysis---')
print()

http_address = 'https://www.kaggle.com/yelp-dataset/yelp-dataset/version/6#yelp_business.csv'
csvfile = 'business.csv'
message = '''
The purpose of this python tools programming exercise is to extract the restaurant-only
data from  the yelp data for USA and Canadian businesses and then analyze it.
The initial data is obtained from
https://www.kaggle.com/yelp-dataset/yelp-dataset/version/6#yelp_business.csv
and saved in a local direcory as
business.csv
'''
print(message)

message = 'Initial read of the csv file:'
business_df = read_csv_file(csvfile, message)

message = 'Initial inspection of the dataframe:'
inspect_data(business_df, message)

print()
print()
print('---Start removing unecessary data---')
message = '''
In this process we will reduce the size of the data
from a (192 609 x 15) table (22 MB)
to a (34 392 x 13) table (3.7 MB)
'''
print(message)
print()

head_lines=5
tail_lines=5

message = 'Re-inspect the dataframe after dropping unecessary column:'
business_df.drop(['Unnamed: 0'], axis=1, inplace=True)
inspect_data(business_df, message, head_lines, tail_lines)

message = 'Inspect the new dataframe containing only restaurants:'
restaurant_df = business_df[business_df['categories'].str.contains('Restaurants') == True]
inspect_data(restaurant_df, message, head_lines, tail_lines)

message = 'Inspect the dataframe containing only restaurants that are still open:'
restaurant_df = restaurant_df[restaurant_df.is_open != 0]
inspect_data(restaurant_df, message, head_lines, tail_lines)

message = 'Inspect the dataframe after dropping the now unnecessary column is_open:'
restaurant_df.drop(['is_open'], axis=1, inplace=True)
inspect_data(restaurant_df, message, head_lines, tail_lines)

head_lines=0
tail_lines=0

message = 'Inspect the dataframe containing only restaurants that have a valid address:'
restaurant_df = restaurant_df[restaurant_df['address'].str.contains('NaN') == False]
inspect_data(restaurant_df, message, head_lines, tail_lines)

message = 'Inspect the dataframe containing only restaurants that have valid hours:'
restaurant_df = restaurant_df[restaurant_df['hours'].str.contains('NaN') == False]
inspect_data(restaurant_df, message, head_lines, tail_lines)

message = 'Construct a dictionary to count number restaurants in each unique state/province'
#restaurant_df.sort_values(by=['state'])
states_dict = get_freq(restaurant_df['state'], message)
print(states_dict)
print()

print()
print()
print('---Finished removing unecessary data---')
print()

print()
print()
print('---Analyze some columns and see the geographic distribution of the data---')
cycle = 0
thresh_dict = {'stars': 0.0, 'review_count': 0, 'exclude_states': []}
print('stars >= ', thresh_dict.get('stars', 0.0))
print('review_count >= ', thresh_dict.get('review_count', 0))
print('exclude_states: ',  thresh_dict.get('exclude_states', []))
print()

columns = ['review_count', 'stars']
message = 'Statistics for some columns:'
stats_on_columns(restaurant_df, message, columns)

message = 'Histogram for a column:'
for column in columns:
    print('column: ', column)
    plot_histogram(restaurant_df, message, column)
    
'''
message = 'kde for a column:'
for column in columns:
    print('column: ', column)
    plot_kde(restaurant_df, message, column)

'''

message = 'Use scatter_matrix to see the histograms and also to see if there are correlations between the columns:'
get_scatter_matrix(restaurant_df, message, columns)

message = 'Create a geoDataFrame of the restaurant data and use it to'
print(message)

# https://medium.com/@shakasom/how-to-convert-latitude-longtitude-columns-in-csv-to-geometry-column-using-python-4219d2106dea
# creating a geometry column 
geometry = [Point(xy) for xy in zip(restaurant_df['longitude'], restaurant_df['latitude'])]
# Coordinate reference system : WGS84
crs = {'init': 'epsg:4326'}
# Creating a Geographic data frame
restaurant_gdf = gpd.GeoDataFrame(restaurant_df, crs=crs, geometry=geometry)

print('restaurant_gdf.head():')
print(restaurant_gdf.head()); print()

restaurant_gdf.drop(['longitude', 'latitude'], axis=1, inplace=True)
print('restaurant_gdf.head():')
print(restaurant_gdf.head()); print()

print('restaurant_df.head():')
print(restaurant_df.head()); print()

restaurant_df.drop(['geometry'], axis=1, inplace=True)
print('restaurant_df.head():')
print(restaurant_df.head()); print()

message = 'From now on will deal with the restaurant data only in the form of the geoDataFrame and not the original DataFrame'
print(message)
print()

message = 'Plot the geographic distibution of the restaurants:'
print(message)
#http://geopandas.org/gallery/create_geopandas_from_pandas.html
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# restrict to North America
ax = world[world.continent == 'North America'].plot(color='white', edgecolor='black', figsize=(20,12))
#cities[cities.continent == 'North America'].plot(ax=ax, color='black')
# now plot the GeoDataFrame
restaurant_gdf.plot(ax=ax, color='red')
plt.show()
print()

message = 'It can be seen that restaurant data only exist for the continental USA (i.e., no Alaska or Hawaii) and a few bordering provinces of Canada'
print(message)
message = 'Thus restrict the map to get a better picture'
print(message)
print()

# downloaded maps in the form of shape files from https://gadm.org/download_country_v3.html
# these are the level 1 (_1) files which show the state or province boundaries

# usa
usa1 = gpd.read_file('gadm36_USA_1.shp')
print('usa1.head():')
print(usa1.head()); print
usa1 = usa1[['NAME_1', 'geometry']]
# changing columns using .columns() 
usa1.columns = ['state_or_province', 'geometry'] 
# remove uneeded states
usa1 = usa1[usa1['state_or_province'] != 'Alaska']
usa1 = usa1[usa1['state_or_province'] != 'Hawaii']
print('usa1:')
print(usa1); print

# canada
can1 = gpd.read_file('gadm36_CAN_1.shp')
print('can1.head(3):')
print(can1.head(3)); print
can1 = can1[['NAME_1', 'geometry']]
# changing columns using .columns() 
can1.columns = ['state_or_province', 'geometry']
# remove uneeded provinces
can1 = can1[can1['state_or_province'] != 'Northwest Territories']
can1 = can1[can1['state_or_province'] != 'Nunavut']
can1 = can1[can1['state_or_province'] != 'Nova Scotia']
can1 = can1[can1['state_or_province'] != 'Yukon']
can1 = can1[can1['state_or_province'] != 'Prince Edward Island']
can1 = can1[can1['state_or_province'] != 'Newfoundland and Labrador']
print('can1:')
print(can1); print
# concatenate
usa1_can1 = usa1.append(can1)
print('usa1_can1:')
print(usa1_can1); print

message = 'Construct a dictionary to count number restaurants in each unique state/province'
#restaurant_df.sort_values(by=['state'])
states_dict = get_freq(restaurant_df['state'], message)
print(states_dict)
print()

ax = usa1_can1.plot(color='white', edgecolor='black', figsize=(20,12))
restaurant_gdf.plot(ax=ax, color='red', markersize=50)
plt.show()
print()

'''
for state in states_dict:
    print('state: ', state)
    ax = usa1_can1.plot(color='white', edgecolor='black', figsize=(20,12))
    restaurant_gdf[restaurant_gdf['state']==state].plot(ax=ax, color='red', markersize=50)
    plt.show()
    plt.clf()
    plt.cla()
    plt.close()
    print()
'''

print()
print()
print('---It can be seen that about 8k restaurants got very few reviews. Make a decision to recommend based on some thresholds which are:---')
print('Also note that there are locations in 11 states or provinces. Try to retain at least 1 in each.')

cycle = 1
thresh_dict = {'stars': 4.5, 'review_count': 100, 'exclude_states': []}
print('stars >= ', thresh_dict.get('stars', 0.0))
print('review_count >= ', thresh_dict.get('review_count', 0))
print('exclude_states: ',  thresh_dict.get('exclude_states', []))
message = 'Doing a cycle of applying thresholds'
restaurant_gdf = do_cycle(restaurant_gdf, cycle, thresh_dict, message)
print()

cycle = 2
thresh_dict = {'stars': 5.0, 'review_count': 200, 'exclude_states': []}
print('stars >= ', thresh_dict.get('stars', 0.0))
print('review_count >= ', thresh_dict.get('review_count', 0))
print('exclude_states: ',  thresh_dict.get('exclude_states', []))
message = 'Doing a cycle of applying thresholds'
restaurant_gdf = do_cycle(restaurant_gdf, cycle, thresh_dict, message)
print()

message = '''
Thus by tightening thresholds we reduced the data to only 19 restaurants in 4 states/provinces:
{'AZ': 9, 'NV': 8, 'QC': 1, 'ON': 1}
The user can then select the appropriate restauirant based on cuisine, etc.
'''
print(message)
print()

print('restaurant_gdf:')
print(restaurant_gdf)
print()
