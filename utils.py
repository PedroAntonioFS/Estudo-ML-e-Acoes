from facade import *
from time import sleep
import pandas as pd
import time
import os

class MarketDataMiner:

    def setup(self):
        SeleniumFacade.get(self._driver, self._url)

    def mine(self):
        pass

    def get_data(self, stock_type, ticker, from_date, to_date, interval):
        pass

    def close(self):
        SeleniumFacade.close(self._driver)

    @property
    def url(self):
        return self._url

class StatusInvestScraper(MarketDataMiner):
    def __init__(self):
        self._driver = SeleniumFacade.open_with_firefox()
        self._wait = WebDriverWaitFacade.setup(self._driver, 15)

    def setup(self):
        super().setup()

        try:
            WebDriverWaitFacade.wait_until_visible(self._wait, "//button[@class='btn-close']")
            SeleniumFacade.click_button(self._driver, "//button[@class='btn-close']")
            sleep(1)
        except:
            pass
        
        try:
            WebDriverWaitFacade.wait_until_visible(self._wait, "//div[@id='statusinvest_desktop_anchor']/a")
            SeleniumFacade.click_button(self._driver, "//div[@id='statusinvest_desktop_anchor']/a")
        except:
            pass

        SeleniumFacade.click_button(self._driver, "//div[@id='indicators-section']/div[1]/div[2]/button[2]")

    def mine(self):
        WebDriverWaitFacade.wait_until_visible(self._wait, "//div[@class='indicator-historical-container']/div[@class='indicators'][1]/div[1]/div[2]/div[1]")

        data = {'Ano': [], 'D.Y': [], 'P/L': [], 'PEG RATIO': [], 'P/VP': [], 'EV/EBITDA': [], 'EV/EBIT': [], 'P/EBITDA': [], 'P/EBIT': [], 'VPA': [], 'P/ATIVO': [], 'LPA': [], 'P/SR': [], 'P/CAP.GIRO': [], 'P/ATIVO CIRC. LIQ.': [], 'Dív. líquida/PL': [], 'Dív. líquida/EBITDA': [], 'Dív. líquida/EBIT': [], 'PL/Ativos': [], 'Passivos/Ativos': [], 'Liq. corrente': [], 'M. Bruta': [], 'M. EBITDA': [], 'M. EBIT': [], 'M. Líquida': [], 'ROE': [], 'ROA': [], 'ROIC': [], 'Giro ativos': [], 'CAGR Receitas 5 anos': [], 'CAGR Lucros 5 anos': []}

        keys = list(data.keys())

        idx_counter = 0
        for i in range(1,6):
            grandparent = LocatingFacade.find_element(self._driver, "//div[@class='indicator-historical-container']/div[@class='indicators'][{}]/div[1]/div[2]/div[1]".format(i))

            first_flag = True
            for parent in LocatingFacade.get_children(grandparent):
                if i == 1 or not first_flag:
                    for children in LocatingFacade.get_children(parent):
                        data[keys[idx_counter]].append(children.text)
                    
                    idx_counter += 1
                first_flag = False

        return data

    def convert(self, data):
        return pd.DataFrame(data)

    def get_data(self, stock_type, ticker, from_date, to_date, interval):
        self._url = "https://statusinvest.com.br/{}/{}".format(stock_type, ticker)
        self.setup()

        data = self.mine()
        dataframe = self.convert(data)

        return dataframe

class YahooFinanceScraper(MarketDataMiner):
    def __init__(self, downloads_path='C:\\Users\\panto\\Downloads\\'):
        self._driver = SeleniumFacade.open_with_firefox()
        self._wait = WebDriverWaitFacade.setup(self._driver, 15)
        self.__downloads_path = downloads_path

    def setup(self):
        super().setup()
        
        try:
            DriverFacade.switch_to_frame(self._driver, "//iframe[@id='guce-inline-consent-iframe']")
            cookies_btn = LocatingFacade.find_element(self._driver, "//form[@id='nonReg-consent-form']/button")
            cookies_btn.click()
            DriverFacade.switch_to_parent(self._driver)
        except ExceptionsFacade.get_NoSuchElementException():
            pass

    def mine(self):
        
        try:
            WebDriverWaitFacade.wait_until_clickable(self._wait, "//div[@id='Col1-1-HistoricalDataTable-Proxy']/section[1]/div[1]/div[2]/span[2]")
        except ExceptionsFacade.get_TimeoutException():
            pass
        download_btn = LocatingFacade.find_element(self._driver, "//div[@id='Col1-1-HistoricalDataTable-Proxy']/section[1]/div[1]/div[2]/span[2]")
        download_btn.click()
        
    def read_archive(self, ticker):
        return pd.read_csv(self.__downloads_path + "{}.SA.csv".format(ticker))

    def delete_archive(self, ticker):
        os.remove(self.__downloads_path + "{}.SA.csv".format(ticker))

    def get_data(self, stock_type, ticker, from_date, to_date, interval):
        from_timestamp = int(time.mktime(from_date.timetuple()) + from_date.microsecond/1e6)
        to_timestamp = int(time.mktime(to_date.timetuple()) + to_date.microsecond/1e6)

        self._url = "https://br.financas.yahoo.com/quote/{}.SA/history?period1={}&period2={}&interval={}&filter=history&frequency={}&includeAdjustedClose=true".format(ticker, from_timestamp, to_timestamp, interval, interval)
        self.setup()

        self.mine()
        data = self.read_archive(ticker)
        self.delete_archive(ticker)

        return data