import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        tyime = time.time()-start_time
        tyime_in_min = int(tyime//60)
        tyime -= tyime_in_min*60
        tyime_in_sec:int = int(tyime)
        tyime -= tyime_in_sec
        tyime_in_mil = int(round(tyime, 2)*100)
        print(func.__name__,'takes ->', str(tyime_in_min)+':'+str(tyime_in_sec)+':'+str(tyime_in_mil))
        return result
    return wrapper