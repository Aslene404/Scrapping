import time
import datetime
import nursing_homes_scrapping
import nursing_bases_scrapping
import support_scrapping
import care_scrapping

if __name__ == '__main__':
    start_time = time.time()
    nursing_bases_scrapping.scrape()
    nursing_homes_scrapping.scrape()
    support_scrapping.scrape()
    care_scrapping.scrape()
    exc_time = (time.time() - start_time)  # exc time
    str(datetime.timedelta(seconds=exc_time))

    print("--- %s exc_time ---" % str(datetime.timedelta(seconds=exc_time)))
