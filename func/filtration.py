from func.geoloc import distance_calc

global all_activities, user_info, demands

''' 
примерный ввод данных
all_activities = [{'name': '', 'category': '', 'price': int(), 'posX': int(), 'posY': int()},
                  {'name': '', 'category': '', 'price': int(), 'posX': int(), 'posY': int()}]

user_info = {'posX': int(),
             'posY': int(),
             'categories': []}

demands = {'max_price': int(),
           'max_distance': int()}
'''


def filters():
    bls = [True if act[0] in user_info['categories'] and
                   demands['max_price'] >= act[1] and
                   demands['max_distance'] >= distance_calc(user_info['posX'],
                                                            user_info['posY'], act['posX'], act['posY'])
           else False for act in all_activities.values()]
    result = [list(all_activities.keys())[x] for x, y in zip(range(len(bls)), bls) if y]
    return result
