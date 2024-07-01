#######################################
#	Name: scraper for 28HSE.com
#	Version: v0p00
#	Create Date: 2024/06/19
#	Author: Ningyuan Zhang
#	Description: 
#	Pre-Requisition: 
#######################################
from CORE_HK_RENT_SCRAPER import *
import re
import os
import openpyxl
import datetime
import time
import pandas as pd
import numpy as np

#######################################
def HOME_INFO_SCRAP():
    # url list
    # page number format: page-*
    # 红磡：https://www.28hse.com/rent/residential/a2/dg31
    # 1-42
    # 何文田：https://www.28hse.com/rent/residential/a2/dg118
    # 1-9
    # 黄埔：https://www.28hse.com/rent/residential/a2/dg115
    # 1-7
    # 土瓜湾：https://www.28hse.com/rent/office/a2/dg24
    # 1-4
    save_file_name  = "TuGuaWan_28HSE"
    url_link_prefix = "https://www.28hse.com/rent/residential/a2/dg24"
    page_start      = 1
    page_stop       = 4

    heads_28hse = {
            "host": "www.28hse.com",
            "referer": "https://www.28hse.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

    scraper_op = SCRAP_28HSE()
    page_num_list = np.arange(page_start, page_stop+1, step=1)

    home_title_list = []
    home_link_list  = []
    home_img_list   = []
    home_area_list  = []
    home_fee_list   = []

    for page_num in page_num_list:
        print("Scrap Page %d / %d"%(page_num, page_stop))
        url_link = "%s/page-%d"%(url_link_prefix, page_num)
        home_info = scraper_op.GET_HOME_LINKS(url_link, headers=heads_28hse)
        home_title_list = home_title_list + home_info["title"][0]
        home_link_list  = home_link_list + home_info["link"][0]
        home_img_list   = home_img_list + home_info["img"][0]
        home_area_list  = home_area_list + home_info["area"][0]
        home_fee_list   = home_fee_list + home_info["fee"][0]
    
    home_img_href_list = []
    for img in home_img_list:
        img_href = "<img src=\"%s\">"%img
        home_img_href_list.append(img_href)

    home_info_pd = pd.DataFrame()
    home_info_pd["TITLE"]   = home_title_list
    home_info_pd["LINK"]    = home_link_list
    home_info_pd["IMG"]     = home_img_href_list
    home_info_pd["FEE"]     = home_fee_list
    home_info_pd["IMG_LINK"]= home_img_list
    # home_info_pd["AREA"]    = home_area_list


    home_info_pd.to_csv("%s.csv"%save_file_name, mode='w', encoding='utf-8')
    home_info_pd.to_html("%s.html"%save_file_name, encoding='utf-8', justify='left', render_links=True, escape=False)
    print("Finish Scrap")

def HOME_DETAIL_SCRAP():
    read_file_name = "TuGuaWan_28HSE.csv"
    save_file_name = "TuGuaWan_28HSE_Detail"
    home_info_pd = pd.read_csv(read_file_name)

    scraper_op = SCRAP_28HSE()
    heads_28hse = {
            "host": "www.28hse.com",
            "referer": "https://www.28hse.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
    
    home_detail_title_list      = home_info_pd["TITLE"]
    home_detail_link_list       = home_info_pd["LINK"]
    home_detail_img_list        = home_info_pd["IMG_LINK"]
    home_detail_img_href_list   = home_info_pd["IMG"]

    num_len = len(home_detail_link_list)

    # home_detail_title_list      = []
    # home_detail_link_list       = []
    # home_detail_img_list        = []
    # home_detail_img_link_list   = []
    home_detail_label_list      = []
    home_detail_tele_list       = []
    home_detail_fee_list        = []
    home_detail_include_list    = []
    home_detail_area_list       = []
    home_detail_tax_list        = []
    home_detail_block_list      = []
    home_detail_floor_list      = []
    home_detail_type_list       = []
    home_detail_prop_list       = []

    for i in range(0,num_len):
        print("Scrap House %d / %d"%(i, num_len))
        home_detail_dict = scraper_op.GET_HOME_INFO(home_link=home_detail_link_list[i], home_title=home_detail_title_list[i], home_img=home_detail_img_list[i], home_img_href=home_detail_img_href_list[i], headers=heads_28hse)
        # home_detail_title_list.append(home_detail_dict["title"])
        # home_detail_link_list.append(home_detail_dict["link"])
        # home_detail_img_list.append(home_detail_dict["img"])
        # home_detail_img_link_list.append(home_detail_dict["img_link"])
        home_detail_label_list.append(home_detail_dict["label"])
        home_detail_tele_list.append(home_detail_dict["tele"])
        home_detail_fee_list.append(home_detail_dict["fee"])
        home_detail_include_list.append(home_detail_dict["include"])
        home_detail_area_list.append(home_detail_dict["area"])
        home_detail_tax_list.append(home_detail_dict["tax"])
        home_detail_block_list.append(home_detail_dict["block"])
        home_detail_floor_list.append(home_detail_dict["floor"])
        home_detail_type_list.append(home_detail_dict["type"])
        home_detail_prop_list.append(home_detail_dict["prop"])

    home_detail_pd = pd.DataFrame()
    home_detail_pd["title"]     = home_detail_title_list
    home_detail_pd["link"]      = home_detail_link_list
    home_detail_pd["img"]       = home_detail_img_list
    home_detail_pd["img_link"]  = home_detail_img_href_list
    home_detail_pd["label"]     = home_detail_label_list
    home_detail_pd["fee"]       = home_detail_fee_list
    home_detail_pd["include"]   = home_detail_include_list
    home_detail_pd["area"]      = home_detail_area_list
    home_detail_pd["tax"]       = home_detail_tax_list
    home_detail_pd["block"]     = home_detail_block_list
    home_detail_pd["floor"]     = home_detail_floor_list
    home_detail_pd["type"]      = home_detail_type_list
    home_detail_pd["prop"]      = home_detail_prop_list

    home_detail_pd.to_csv("%s.csv"%save_file_name, mode='w', encoding='utf-8')
    home_detail_pd.to_html("%s.html"%save_file_name, justify='left', encoding='utf-8', render_links=True, escape=False)
    print("Finish Home Detail Scrap")
#######################################
# execute
if (__name__ == "__main__"):
    # HOME_INFO_SCRAP()
    HOME_DETAIL_SCRAP()