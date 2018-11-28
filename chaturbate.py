from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from multiprocessing import Process, Semaphore
from time import strftime


def monitor(link, s):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
    driver = webdriver.PhantomJS("phantomjs.exe", desired_capabilities=dcap)
    try:
        driver.get(link)
        last = [e.text for e in driver.find_elements_by_id('0')]
        with open(link.split('chaturbate.com/')[1].replace('/', '')+ '.txt', 'a') as F:
            while s.get_value():
                now = [e.text.replace('\n', ' ')+'\n' for e in driver.find_elements_by_id('0')]
                now2 = now.copy()
                for e in last:
                    try:
                        now2.remove(e)
                    except ValueError:
                        pass
                if now2:
                    F.writelines([strftime('%Y/%m/%d %H:%M:%S ') + e for e in now2])
                last = now
                sleep(1)
    finally:
        driver.close()


if __name__ == '__main__':
    with open("links.txt") as F:
        links = [l.strip() for l in F.readlines()]
    procs = []
    s = Semaphore()
    try:
        for link in links:
            p = Process(target=monitor, args=(link, s))
            p.start()
            procs.append(p)
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        s.acquire()
        for p in procs:
            p.join()
        print("Stopped.")



