from geopy import distance


def distance_calc(myshirota, mydolgota, clubshirota, clubdolgota):
    mylocation = (myshirota, mydolgota)
    clublocation = (clubshirota, clubdolgota)
    dist = distance.distance(mylocation, clublocation).km
    return round(dist,2)