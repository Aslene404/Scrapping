import time
import datetime

import nursing_bases_scrapping

if __name__ == '__main__':
    start_time = time.time()
    nursing_bases_scrapping.scrape()
    

    exc_time = (time.time() - start_time)  # exc time
    str(datetime.timedelta(seconds=exc_time))

    print("--- %s exc_time ---" % str(datetime.timedelta(seconds=exc_time)))
