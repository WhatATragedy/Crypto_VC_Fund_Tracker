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

class CryptoPortfolioScraper():
    def __init__(self):
        self._funds = [
            ("MultiCoin", "https://multicoin.capital/portfolio/", self.scrape_multicoin),
            ("Binance", "https://labs.binance.com/", self.scrape_binance),
            ("Coinbase", "https://www.coinbase.com/ventures", self.scrape_coinbase),
            ("1Confirmation", "https://www.1confirmation.com/portfolio", self.scrape_1confirmation),
            ("a16z", "https://a16z.com/portfolio/", self.scrape_a16z),
            ("Arrington XRP Capital", "https://arringtonxrpcapital.com/companies/", self.scrape_arrington),
            ("Blockchain Capital", "https://blockchain.capital/portfolio/", self.scrape_blockchain_cap),
            ("Digital Currency Group", "https://dcg.co/portfolio/", self.scrape_dcg),
            ("Dragonfly Capital", "https://www.dcp.capital/portfolio", self.scrape_dcp),
            ("Fabric Ventures", "https://www.fabric.vc/", self.scrape_fabric),
            ("Placeholder Ventures", "https://www.placeholder.vc/", self.scrape_placeholder_vc),
            ("Three Arrows Capital", "https://www.threearrowscap.com/select-investments/", self.scrape_three_arrows),
            ("Winklevoss Capital", "https://winklevosscapital.com/portfolio/?category=crypto-blockchain", self.scrape_winklevoss)
            # ("BoostVC", "https://www.boost.vc/portfolio#cryptolink", self.scrape_boostvc) # Hard because style sheet is grim
            # ("Electric Capital"), Hard because they're images on the site
            # ("Huobi Capital/Exchange"), No english
            # ("Pantera Capital", "https://panteracapital.com/portfolio/", self.scrape_pantera) # this is the same, images hosted on the site with no links
            # ("Polychain Capital", "https://jobs.polychain.capital/companies", self.scrape_polychain), #Doesn't render properly with requests, need selenium
            # ("Union Square Ventures", "https://www.usv.com/idea/blockchains-crypto/", self.scrape_usv), # Currently broken sadly
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
            print(f"{key} currently has {len(crypto_portfolio[key])} investments")
            # print(f"{key} : {crypto_portfolio[key][0:2]}")
        self.assets = crypto_portfolio
        return crypto_portfolio

    def scrape_winklevoss(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all("div", {"class": "portfolio-item-container"})
        for div in divs:
            project_website = div.find("a", {"class": "portfolio-item-link"}, href=True)
            project_name = div.find("h2")
            if project_website and project_name:
                assets.append({
                    "name": project_name.text,       
                    "website": project_website['href']
                }) 
        return assets
    
    def scrape_usv(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all("div", {"class": "m__list-items m__list-items--small"})
        for div in divs:
            h4 = div.find("h4", {"class": "a__lh_36"})
            print(h4.text)
            if h4:
                if h4.text == "Selected Companies":
                    ## Got the Div we want, now enumerate
                    print("Found the write Div!")
                    items = div.find_all("div", {"class": "m__list-items__list-item"})
                    print(items)
                    for item in items:
                        print(item)
                        project_website = item.find("a")
                        if project_website:
                            assets.append({
                                "name": project_website.text,       
                            })
        return assets

    def scrape_three_arrows(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all("div", {"class": "investment-logo"})
        for div in divs:
            project_website = div.find("a", href=True)
            if project_website:
                parsed_url = tldextract.extract(project_website['href'])
                # print(parsed_url.domain)
                assets.append({
                    "name": parsed_url.domain,       
                    "website": project_website['href']
                }) 
        return assets

    def scrape_polychain(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.select('div.sc-bdvvtL.sc-gsDKAQ.izDKYq.hIxhWw') # this div has multiple classes so there are spaces so we have to use select here
        print(divs)
        for div in divs:
            print(div)
            project_name = div.find("a")
            if project_name:
                assets.append({
                    "name": project_name,       
                }) 
        return assets

    def scrape_placeholder_vc(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        a_tags = soup.find_all("a", {"class": "portfolio-link"}, href=True)
        for a_tag in a_tags:
            project_website = a_tag['href']
            project_name = a_tag.text
            if project_website:
                assets.append({
                    "name": project_name,       
                    "website": project_website
                }) 
        return assets

    def scrape_pantera(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        print(r.text)
        divs = soup.find_all("div", {"class": "cell large-4 post-item"})
        for div in divs:
            print(div)
            project_website = div.find("img")
            if project_website:
                parsed_url = tldextract.extract(project_website['src'])
                # print(parsed_url.domain)
                assets.append({
                    "name": parsed_url.domain,       
                    "website": '.'.join([parsed_url.domain, parsed_url.suffix])
                }) 
        return assets

    def scrape_fabric(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        main_div = soup.find("div", {"id": "projects"})
        divs = main_div.find_all("div", {"role": "listitem"})
        for div in divs:
            project_website = div.find("a", href=True)
            if project_website:
                parsed_url = tldextract.extract(project_website['href'])
                # print(parsed_url.domain)
                assets.append({
                    "name": parsed_url.domain,       
                    "website": project_website['href']
                }) 
        return assets

    def scrape_dcp(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all("div", {"role": "listitem"})
        for div in divs:
            project_website = div.find("a", href=True)
            if project_website:
                parsed_url = tldextract.extract(project_website['href'])
                # print(parsed_url.domain)
                assets.append({
                    "name": parsed_url.domain,       
                    "website": project_website['href']
                }) 
        return assets

    def scrape_dcg(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.find_all("div", {"class": "company-info"})
        for div in divs:
            project_website = div.find("a", href=True)
            name = div.find("h6")
            if name and project_website:
                assets.append({
                    "name": name.text,       
                    "website": project_website['href']
                }) 
        return assets

    def scrape_boostvc(self, fund_site):
        assets = list()
        r = self._cloud_scraper.get(fund_site)
        soup = BeautifulSoup(r.text, features="html.parser")
        divs = soup.select('div[data-block-json*="Crypto"]')
        print(divs)
        # unordered_list = soup.find("ul", {"class": "filter-content"})
        # list_items = unordered_list.find_all("li")
        # for list_item in list_items:
        #     project_website = list_item.find("a", href=True)
        #     if project_website:
        #         parsed_url = tldextract.extract(project_website['href'])
        #         # print(parsed_url.domain)
        #         assets.append({
        #             "name": parsed_url.domain,       
        #             "website": project_website['href']
        #         }) 
        # return assets

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
    def is_fund_already_invested(fund, processed_item):
        ## There is an issue where sometimes funds get added twice - this is probably because the scraping is bad
        ## i.e the website is the same for two investments because they overwrote the company website or something
        return True if fund in processed_item.get("funds") else False

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

        #TODO - Vectorize this.
        """
        merged_assets = dict()
        assets = assets if assets else self.assets
        for fund in assets.keys():
            ## For each fund, go through their assets
            for asset in assets[fund]:
                # For each asset in a fund, check it against processed assets to see if there is a match
                asset_name = asset.get("name")
                # print(f"Currently Processing {fund} - {asset_name}")
                # if merged_assets hasn't been set yet then add the first asset
                if len(merged_assets) == 0:
                    print(f"Merged Assets is empty so adding first item and fund.. {asset_name}..")
                    merged_assets[asset_name] = dict({
                        "website": asset.get("website"),
                        "funds": [fund]
                    })
                    continue
                matched = False
                for processed_asset_name, processed_asset_data in merged_assets.items():
                    # print(f"Currently checking processed list for {asset_name} with {fund}")
                    # print(f"{processed_asset_name} : {processed_asset_data}")

                    # Check if the websites are the same as any in the merged_assets
                    if self.website_is_a_match(asset, processed_asset_data):
                        if not self.is_fund_already_invested(fund, processed_asset_data):
                            merged_assets[processed_asset_name]['funds'].append(fund)
                            # print(f"Matched {asset_name} and {processed_asset_name} for {fund} via Website Match")
                        matched = True
                        # Want to break as the asset has now been added to the processed list so no more additions are needed.
                        break

                    # If there is no website match, then try levenstein, but only if the sizes are about right
                    elif (len(processed_asset_name) >= 4 and len(asset_name) >= 4):
                        distance = levenshtein_distance(asset_name, processed_asset_name)
                        # print(f"Comparsed {asset_name} and {processed_asset_name}: Distance {distance}")
                        if distance < 2:
                            if not self.is_fund_already_invested(fund, processed_asset_data):
                                #Already been processed with a similar name so add the fund as being an investor
                                merged_assets[processed_asset_name]['funds'].append(fund)
                                # print(f"Matched {asset_name} and {processed_asset_name} for {fund} via Levenstein {distance}")
                            matched = True
                            # Want to break as the asset has now been added to the processed list so no more additions are needed.
                            break  
                    else:
                        ## Was unable to match with anything so add it to the list with the fund
                        # Set the not_matched = True then we can add it to the dict after processing
                        matched = False
                if not matched:
                    # print(f"Unable to match {asset_name} with {fund} so adding to processed list as it's a new asset")
                    merged_assets[asset_name] = dict({
                        "website": asset.get("website"),
                        "funds": [fund]
                    })                  
        return merged_assets       


if __name__ == "__main__":
    cps = CryptoPortfolioScraper()
    assets = cps.run()
    with open("assets.json", "w") as assets_all:
        json.dump(assets, assets_all, indent=4)
    
    fuzz = cps.fuzzy_matching_assets()
    for asset_name, asset_data in fuzz.items():
        if len(asset_data.get("funds")) >= 4:
            print(f"{asset_name} has {len(asset_data.get('funds'))} invested.. {asset_data.get('funds')}")

    # cps.scrape_coinbase("https://www.coinbase.com/ventures")
    # cps.scrape_binance("Binance", "https://labs.binance.com/")
    # cps.scrape_boostvc("https://www.boost.vc/portfolio#cryptolink")