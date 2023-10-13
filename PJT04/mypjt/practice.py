events_set = {'Fog , Rain , Thunderstorm', 'Fog', ' ', 'Fog , Rain', 'Thunderstorm', 'Rain , Thunderstorm', 'Fog , Thunderstorm', 'Rain', 'Rain , Snow'}
new_set = set()
for e in events_set:
    if ',' in e:
        new_set | set(e.split(' , '))
    else:
        new_set.add(e)
print(new_set)