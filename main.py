"""
Point of this is to find the investments made by the big Crypto Firms and see if there is anything intereting
This is a program to Scrape that and put it all in one place.
"""
import json

import requests
from bs4 import BeautifulSoup
import cloudscraper
import tldextract
from Levenshtein import distance as levenshtein_distance
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class CryptoPortfolioScraper():
    def __init__(self):
        self._funds = [
            ("MultiCoin", "https://multicoin.capital/portfolio/", self.scrape_multicoin),
            ("Binance", "https://labs.binance.com/", self.scrape_binance),
            ("Coinbase", "https://www.coinbase.com/ventures", self.scrape_coinbase),
            ("1Confirmation", "https://www.1confirmation.com/portfolio", self.scrape_1confirmation),
            ("a16z", "https://a16z.com/portfolio/", self.scrape_a16z),
            ("Arrington XRP Capital", "https://arringtonxrpcapital.com/companies/", self.scrape_arrington),
            ("Blockchain Capital", "https://blockchain.capital/portfolio/", self.scrape_blockchain_cap)
            # ("BoostVC"),
            # ("Digial Currency Group"),
            # ("Dragonfly Capital"),
            # ("Electric Capital"),
            # ("Fabric Ventures"),
            # ("Huobi Capital/Exchange"),
            # ("Pantera Capital"),
            # ("Placeholder Ventures"),
            # ("Polychain Capital"),
            # ("Three Arrows Capital"),
            # ("Union Square Ventures"),
            # ("Winklevoss Capital")
        ]
        self._cloud_scraper = cloudscraper.create_scraper()
        self.assets = dict()
    
    def run(self):
        crypto_portfolio = dict()
        for fund in self._funds:
            if not len(fund) == 3:
                print(f"Issue with the Funds set values. Skipping {fund[0]}")
                continue
            print(fund)
            fund_portfolio = fund[2](fund[1])
            crypto_portfolio[fund[0]] = fund_portfolio
        for key in crypto_portfolio:
            print(f"{key} : {crypto_portfolio[key][0:2]}")
        self.assets = crypto_portfolio
        return crypto_portfolio

    def scrape_blockchain_cap(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        unordered_list = soup.find("ul", {"class": "filter-content"})
        list_items = unordered_list.find_all("li")
        for list_item in list_items:
            project_website = list_item.find("a", href=True)
            if project_website:
                parsed_url = tldextract.extract(project_website['href'])
                # print(parsed_url.domain)
                assets.append({
                    "name": parsed_url.domain,       
                    "website": project_website['href']
                }) 
        return assets

    def scrape_arrington(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        table_rows = soup.find_all("td")
        for table_row in table_rows:
            project_website = table_row.find("a", href=True)
            name = table_row.find("strong")
            if project_website:
                if "arringtonxrpcapital" in project_website['href']:
                    project_website = None
            if name:
                assets.append({
                    "name": name.text,
                    "website": project_website['href'] if project_website else None
                }) 
        return assets

    def scrape_a16z(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all("div", {"class": "company company-type--crypto company--single-company"})
        divs.extend(soup.find_all("div", {"class": "company company-stage--seed company-type--crypto company--single-company"}))
        for div in divs:
            project_website = div.find("a", href=True)
            if project_website:
                parsed_url = tldextract.extract(project_website['href'])
                assets.append({
                    "name": parsed_url.domain,
                    "website": project_website['href']
                })
        return assets
        
    def scrape_1confirmation(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all("div", {"class": "project gallery-project"})
        for div in divs:
            name = div.find("h2", {"class": "project-title"})
            website = div.find("a", href=True)
            if name and website:
                assets.append({
                    "name": name.text,
                    "website": website.text
                })
        return assets

    def scrape_multicoin(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all("div", {"class": "no-js-visibility Project__PosedProject-sc-1vpvqcu-0 AFcnR"})
        for div in divs:
            project_website = div.find("a", {"class": "project-link btn outline small"})
            if not project_website:
                continue
            info = div.find("p", {"class": "short-description"}).text
            parsed_url = tldextract.extract(project_website['href'])
            assets.append({
                "name": parsed_url.domain,
                "website": project_website['href'],
                "info": info
            })
        return assets

    def scrape_binance(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all("div", {"class": "flex-fill p-3"})
        for div in divs:
            project_website = div.find("a", href=True)['href']
            # print(project_website)
            parsed_url = tldextract.extract(project_website)
            # print(parsed_url.domain)
            assets.append({
                "name": parsed_url.domain,
                "website": project_website
            })
        return assets

    def scrape_coinbase(self, fund_site):
        assets = []
        r = self._cloud_scraper.get(fund_site)
        # with open("coinbase.txt", "w") as tmp:
        #     tmp.write(r.text)
        soup = BeautifulSoup(r.text, features="html.parser")
        a_tags = soup.find_all("a", {"class": "LogoCard__Link-m4u6vn-0 bIsJm"})
        for a_tag in a_tags:
            div = a_tag.find("div", {"class": "cds-flex-fytym9g cds-column-cygaqsr"})
            header = div.find("h3")
            info = div.find("p")
            if header and info:
                # We got an asset probably so return it 
                assets.append({
                    "name": header.text,
                    "website": a_tag['href'],
                    "info": info.text
                })
        return assets

    @staticmethod
    def website_is_a_match(asset1, asset2):
        asset1_site = tldextract.extract(asset1.get("website"))
        asset2_site = tldextract.extract(asset2.get("website"))
        return asset1_site.domain == asset2_site.domain and asset1_site.suffix == asset2_site.suffix

    def fuzzy_matching_assets(self, assets=dict()):
        """
        For each fund, check if the website is the same, if that fails then levenstein
        It checks the assets against the other funds until all funds have been checked and merged
        This is CPU intensive and I might need to take some time to make faster
        """
        merged_assets = dict()
        assets = assets if assets else self.assets
        for fund in assets.keys():
            ## For each fund, go through their assets
            for asset in assets[fund]:
                # For each asset in a fund, check it against processed assets to see if there is a match
                # print(f"Currently Processing {fund}, asset {asset}")
                asset_name = asset.get("name")
                # if merged_assets hasn't been set yet then add the first asset
                if len(merged_assets) == 0:
                    print(f"Merged Assets is empty so adding first item and fund.. {asset_name}..")
                    merged_assets[asset_name] = dict({
                        "website": asset.get("website"),
                        "funds": [fund]
                    })
                    continue
                matched = False
                ## Levenstein doesn't work very well for small strings, so for that case we just append it
                for processed_asset_name, processed_asset_data in merged_assets.items():
                    # print(f"{processed_asset_name} : {processed_asset_data}")
                    # Check if the websites are the same as any in the merged_assets
                    if self.website_is_a_match(asset, processed_asset_data):
                        merged_assets[processed_asset_name]['funds'].append(fund)
                        matched = True
                        print(f"Matched {asset_name} and {processed_asset_name} for {fund} via Website Match")
                        continue
                    ## Again Levenstein is bad if asset name is short so add in
                    if len(processed_asset_name) <= 4 and len(asset_name) <= 4:
                        continue
                    else:
                        distance = levenshtein_distance(asset_name, processed_asset_name)
                        # print(f"Comparsed {asset_name} and {processed_asset_name}: Distance {distance}")
                        if distance < 2:
                            #Already been processed with a similar name so add the fund as being an investor
                            merged_assets[processed_asset_name]['funds'].append(fund)
                            matched = True
                            print(f"Matched {asset_name} and {processed_asset_name} for {fund} via Levenstein {distance}")
                if not matched:
                    ## It's an asset that hasn't been seen and processed yet so add to list with fund
                    merged_assets[asset_name] = dict({
                        "website": asset.get("website"),
                        "funds": [fund]
                    })
                    # print(f"Found no match for {asset_name} invested by {fund} - Added to processed")
        return merged_assets       


if __name__ == "__main__":
    cps = CryptoPortfolioScraper()
    assets = cps.run()
    with open("assets.json", "w") as assets_all:
        json.dump(assets, assets_all, indent=4)
    fuzz = cps.fuzzy_matching_assets()
    for asset_name, asset_data in fuzz.items():
        if len(asset_data.get("funds")) >= 2:
            print(f"{asset_name} has {len(asset_data.get('funds'))} invested.. {asset_data.get('funds')}")

    # cps.scrape_coinbase("https://www.coinbase.com/ventures")
    # cps.scrape_binance("Binance", "https://labs.binance.com/")