import quest
import geojson
from pprint import pprint
import json

# get settings and api etc
settings = quest.api.get_settings()
for k, v in settings.items():
    print('%s: %s' % (k, v))

print('\nQUEST version %s' % quest.api.get_quest_version())
print('\nQUEST API version %s' % quest.api.get_api_version())

# get list of providers
providers = quest.api.get_providers(expand=True)
print('\n%s QUEST providers are available:' % len(providers))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
for k, v in providers.items():
    print('{: <20} {: <20}'.format(k, v['display_name']))

# get list of providers
services = quest.api.get_services(expand=True)
print('\n%s QUEST providers are available:' % len(services))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
for k, v in services.items():
    print('{: <50} {: <20}'.format(k, v['display_name']))


# get list of mapped parameters
mapped_parameters = quest.api.get_mapped_parameters()
print('\n%s QUEST mapped parameters are available:' % len(mapped_parameters))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
for p in mapped_parameters:
    print('{:}'.format(p))


# filter providers by parameter
print('\n--------------------------------------------------')
print('      Filter Services by Parameter')
print('--------------------------------------------------')

print('\nChoose a QUEST Mapped Parameter:')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
for i, p in enumerate(sorted(mapped_parameters)):
    print('{: >2}. {:}'.format(i, p))

choice = input('\nEnter parameter number (default=7, elevation):')
if not choice:
    choice = '7'
choice = int(choice)

# get list of providers
services = quest.api.get_services(expand=True, parameter=mapped_parameters[choice])
print('\n%s QUEST providers contain the %s parameter:' % (len(services), mapped_parameters[choice]))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
for k, v in services.items():
    print('{: <50} {: <20}'.format(k, v['display_name']))

# get features from service
print('\n--------------------------------------------------')
print('      Get Features from Service')
print('--------------------------------------------------')

services = quest.api.get_services(expand=True)
print('\nChoose a QUEST Service(s):')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
svcs = {}
for i, (k, v) in enumerate(sorted(services.items())):
    svcs[i] = k
    print('{: >2}. {: <50} {: <20}'.format(i, k, v['display_name']))

choice = input('\nEnter providers to include (comma seperated) (default=6,8)')
while ('14' not in choice) and ('4' in choice or '5' in choice):
    print('NOAA providers are not currently available/n')
    choice=input('Choose another service ')
if not choice:
    choice = '6, 8'
uris = [svcs[int(c)] for c in choice.split(',')]
print('\n%d QUEST Service(s) were selected:' % (len(uris),))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\n'.join(uris))

print('\nSpecify additional filters:')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
bbox = input('Enter bounding_box (e.g. -180,-90,180,90) (default:None)')
if not bbox:
    bbox = None

parameter = input('Enter parameter number (0-%d) (default:None)' % (len(mapped_parameters) - 1,))
if not parameter:
    parameter = None
else:
    parameter = mapped_parameters[int(parameter)]

geom_type = input('Enter geometry type (Point/Polygon) (default: None):')
if not geom_type:
    geom_type = None

update_cache = input('Update cached metadata (y/n) (default: n):')
if update_cache.lower() == 'y':
    update_cache = True
else:
    update_cache = False

filters = {}
for filter_name in ['parameter', 'geom_type', 'bbox']:
    filter_value = locals()[filter_name]
    if filter_value is not None:
        filters[filter_name] = filter_value

# get features as pandas dataframe using as_dataframe=True kwarg
# this is useful when writing a python script
features_df = quest.api.get_features(services=uris,
                                   filters=filters,
                                   update_cache=update_cache,
                                   as_dataframe=True)

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('      %s features found' % len(features_df))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# get features in geojson format, useful for mapping
# this should just read the cached data generated by the above line
features_geojson = quest.api.get_features(services=uris, filters=filters, as_geojson=True)
output_features = input('Print features (y/n):')
if output_features == 'y':
    pprint(dict(features_geojson))
filename = input('Enter geojson filename (default: file not saved):')
if filename:
    with open(filename, 'w') as f:
        f.write(geojson.dumps(features_geojson))
