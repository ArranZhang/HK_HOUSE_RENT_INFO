#######################################
#	Name: Hong Kong house rent scraper core
#	Version: v0p00
#	Create Date: 2024/06/19
#	Author: Ningyuan Zhang
#	Description: 
#       - core function definition for house rent scraper
#	Pre-Requisition: 
#######################################
import re
import requests
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import random
import time
import datetime
import openpyxl

#######################################
# common tools
class COMMON():
    def __init__(self) -> None:
        pass

    def GET_URL(self, url_link, url_heads="", url_params=""):

        while True:
            try:
                rslt = requests.get(url_link, headers=url_heads, params=url_params)
                break
            except requests.exceptions.ConnectionError:
                print("Connection Error")
                time.sleep(10*random.random())
            except requests.exceptions.ChunkedEncodingError:
                print("Chunked Encoding Error")
                time.sleep(10*random.random())
            except:
                print("Unknown Error Occurred")
                time.sleep(10*random.random())
        return(rslt)

class SCRAP_28HSE():
    def __init__(self) -> None:
        self.hse28_common = COMMON()

    def GET_HOME_LINKS(self, home_url, headers="", params=""):  
        hse28_home_results  = self.hse28_common.GET_URL(home_url, url_heads=headers, url_params=params)
        hse28_home_html     = etree.HTML(hse28_home_results.content)
        # parse target
        # item link: //*[@id="search_results_div"]/div/div[*]/div[2]/div[2]/a
        try:
            item_title  = hse28_home_html.xpath('//*[@id="search_results_div"]/div/div[*]/div[2]/div[2]/a/text()')
            item_link   = hse28_home_html.xpath('//*[@id="search_results_div"]/div/div[*]/div[2]/div[2]/a/@href')
            item_img    = hse28_home_html.xpath('//*[@id="search_results_div"]/div/div[*]/div[1]/a/img/@src')
            item_area   = hse28_home_html.xpath('//*[@id="search_results_div"]/div/div[*]/div[2]/div[3]/div[2]/div[2]/text()')
            item_fee    = hse28_home_html.xpath('//*[@id="search_results_div"]/div/div[*]/div[2]/div[4]/div/div[1]/text()')
            item_info_dict  = {
                "title":    [item_title     ],
                "link":     [item_link      ],
                "img":      [item_img       ],
                "area":     [item_area      ],
                "fee":      [item_fee       ]
            }
        except IndexError:
            print("Home Item not found")
            
        
        return(item_info_dict)

    def GET_HOME_INFO(self, home_link, home_title, home_img, home_img_href, headers="", params=""):
        home_detail = self.hse28_common.GET_URL(home_link, url_heads=headers, url_params=params)
        home_detail_html = etree.HTML(home_detail.content)
        # parse target
        label   =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[*]/div/div[*]/text()'
        tele    =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[2]/img/@src'
        fee     =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr[2]/td[2]/div/text()'
        include =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr[3]/td[2]/div/text()'
        area    =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr[4]/td[2]/div[1]/text()'
        tax     =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr[4]/td[2]/div[3]/text()'
        block   =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr[5]/td[2]/*/text()'
        floor_lvl   =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr[6]/td[2]/div/text()'
        type    =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr[7]/td[2]/div/text()'
        prop    =   '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr[10]/td[2]/div/text()'
        try:
            home_detail_label = home_detail_html.xpath(label)
            home_detail_label = [x.strip() for x in home_detail_label]
            home_detail_label = list(set(home_detail_label))

            home_detail_tele = home_detail_html.xpath(tele)[0]

            home_detail_fee = home_detail_html.xpath(fee)[0].strip()

            home_detail_include = home_detail_html.xpath(include)[0].strip()

            home_detail_area = home_detail_html.xpath(area)[0].strip()

            home_detail_tax = home_detail_html.xpath(tax)[0].strip()

            home_detail_block = home_detail_html.xpath(block)
            home_detail_block = [x.strip() for x in home_detail_block]
            home_detail_block = list(set(home_detail_block))

            home_detail_floor = home_detail_html.xpath(floor_lvl)[0].strip()

            home_detail_type = home_detail_html.xpath(type)[0].strip()

            home_detail_prop = home_detail_html.xpath(prop)[0].strip()

            home_detail_dict = {
                "title":        home_title,
                "link":         home_link,
                "img":          home_img_href,
                "img_link":     home_img,
                "label":        home_detail_label,
                "tele":         home_detail_tele,
                "fee":          home_detail_fee,
                "include":      home_detail_include,
                "area":         home_detail_area,
                "tax":          home_detail_tax,
                "block":        home_detail_block,
                "floor":        home_detail_floor,
                "type":         home_detail_type,
                "prop":         home_detail_prop
            }
        except IndexError:
            print("Detail Not Found")
            home_detail_dict = {
                "title":        ["NULL"],
                "link":         ["NULL"],
                "img":          ["NULL"],
                "img_link":     ["NULL"],
                "label":        ["NULL"],
                "tele":         ["NULL"],
                "fee":          ["NULL"],
                "include":      ["NULL"],
                "area":         ["NULL"],
                "tax":          ["NULL"],
                "block":        ["NULL"],
                "floor":        ["NULL"],
                "type":         ["NULL"],
                "prop":         ["NULL"]
            }
        return(home_detail_dict)
            
#######################################
# debug
def main():
    tb_scraper  = SCRAP_28HSE()
    pg_num      = 1
    # test_link   = "https://www.28hse.com/rent/residential/a2/dg31/page-%d"%pg_num
    test_link   = "https://www.28hse.com/rent/residential/property-3080693"
    test_heads = {
        "host": "www.28hse.com",
        "referer": "https://www.28hse.com/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    # results = tb_common.GET_URL(test_link, url_heads=test_heads)
    # results = tb_scraper.GET_HOME_LINKS(test_link, headers=test_heads)
    results = tb_scraper.GET_HOME_INFO(home_link=test_link, headers=test_heads, home_title="", home_img="", home_img_href="")
    print(results)
    # img_list = []
    # for img in results["img"][0]:
    #     img_href = "<img src=\"%s\">"%img
    #     # img_href = img
    #     img_list.append(img_href)

    results_pd = pd.DataFrame()
    results_pd["titles"]    = results["title"]
    results_pd["links"]     = results["link"]
    results_pd["fee"]       = results["fee"] 
    results_pd["label"]     = results["label"][0]
        
    # print(results_pd)
    results_pd.to_csv("search_result.csv", mode='w', encoding='utf-8')
    results_pd.to_html("search_result.html", justify='left', render_links=True, escape=False)
    print("Finish")


if (__name__=="__main__"):
    main()
