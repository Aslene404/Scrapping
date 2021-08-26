import time
import datetime
import support_scrapping

if __name__ == '__main__':
    start_time = time.time()

    support_scrapping.scrape()
    exc_time = (time.time() - start_time)  # exc time
    str(datetime.timedelta(seconds=exc_time))

    print("--- %s exc_time ---" % str(datetime.timedelta(seconds=exc_time)))
