#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
import tkinter.ttk as ttk

from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingInfo
from oandapyV20.exceptions import V20Error

import settings


def currency_calc():
    # 為替のAPI取得 OANDA
    accountID = settings.ACCOUNTID
    access_token = settings.ACCESS_TOKEN
    api = API(access_token=access_token, environment="practice")
    
    # 取得する通貨ペア
    params = { "instruments": "USD_JPY,GBP_JPY,EUR_JPY," }
    pricing_info = PricingInfo(accountID=accountID, params=params)
    
    try:
        api.request(pricing_info)
        response = pricing_info.response
        currency_lis = []
        # 現在の売値のレートを指定通貨ペアの数だけ取得する
        for i in range(3):
            currency_lis.append(response["prices"][i]["bids"][0]["price"])
        
        dollar = float(currency_lis[0])
        pound = float(currency_lis[1])
        euro = float(currency_lis[2])
        return [dollar, pound, euro]

    except V20Error as e:
        print("Error: {}".format(e))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        ## 基本設定

        self.title('通貨計算機-1.0')
        self.geometry('450x130')
        self.option_add('*font', ('FixedSys', 14))
        self.wm_attributes('-topmost', True)
        
        self.s = ttk.Style()
        self.s.configure('My.TFrame')
        
        self.iframe = ttk.Frame(self, style='My.TFrame')
        self.iframe.pack(expand=True, fill=tk.BOTH, padx=16, pady=16)
        
        ## コンテンツ設定
        
        self.progress = tk.LabelFrame(self.iframe, text='通貨レート', width=400, height=90, labelanchor=tk.NW)
        self.progress.propagate(False)
        self.progress.pack(fill=tk.X)
        
        ### 円
        self.jpy_rate = tk.IntVar()
        self.jpy_rate.set(100)
        self.jpy = tk.Entry(self.progress, width=7, textvariable=self.jpy_rate)
        self.jpy.grid(column=0, row=0, ipadx=3, ipady=3, padx=(22, 14), pady=(10, 4), sticky=tk.W + tk.E)     
        self.jpy.bind("<Return>", self.jpy_func)
        
        self.jpy_lb = tk.Label(self.progress, text="円", width=7)
        self.jpy_lb.grid(column=0, row=1, sticky=tk.W + tk.E)
        
        ### ドル
        self.usd_rate = tk.StringVar()
        self.usd = tk.Entry(self.progress, width=7, textvariable=self.usd_rate)
        self.usd.grid(column=1, row=0, ipadx=3, ipady=3, padx=14, pady=(10, 4), sticky=tk.W + tk.E)     
        self.usd.bind("<Return>", self.usd_func)
        
        self.usd_lb = tk.Label(self.progress, text="ドル", width=7)
        self.usd_lb.grid(column=1, row=1, sticky=tk.W + tk.E)

        ### ポンド
        self.gbp_rate = tk.StringVar()
        self.gbp = tk.Entry(self.progress, width=7, textvariable=self.gbp_rate)
        self.gbp.grid(column=2, row=0, ipadx=3, ipady=3, padx=14, pady=(10, 4), sticky=tk.W + tk.E)     
        self.gbp.bind("<Return>", self.gbp_func)
        
        self.gbp_lb = tk.Label(self.progress, text="ポンド", width=7)
        self.gbp_lb.grid(column=2, row=1, sticky=tk.W + tk.E)
        
        ### ユーロ
        self.eur_rate = tk.StringVar()
        self.eur = tk.Entry(self.progress, width=7, textvariable=self.eur_rate)
        self.eur.grid(column=3, row=0, ipadx=3, ipady=3, padx=14, pady=(10, 4), sticky=tk.W + tk.E)     
        self.eur.bind("<Return>", self.eur_func)
        
        self.eur_lb = tk.Label(self.progress, text="ユーロ", width=7)
        self.eur_lb.grid(column=3, row=1, sticky=tk.W + tk.E)
    
    ## 関数定義
    
    def jpy_func(self, event):
        jpy = self.jpy.get()
        currency_price = currency_calc()
        total = []
        for i in range(3):
            total.append(1 * ((float(jpy) - currency_price[i])/currency_price[i]) + 1)
            
        self.usd_rate.set('{:.2f}'.format(total[0]))
        self.eur_rate.set('{:.2f}'.format(total[1]))
        self.gbp_rate.set('{:.2f}'.format(total[2]))
    
    
    def usd_func(self, event):
        usd = self.usd.get()
        currency_price = currency_calc()
        currency_price[0] *=  float(usd) 
        
        self.jpy_rate.set('{:.2f}'.format(currency_price[0]))
        self.eur_rate.set('{:.2f}'.format(currency_price[0] / currency_price[2]))
        self.gbp_rate.set('{:.2f}'.format(currency_price[0] / currency_price[1]))
        
        
    def gbp_func(self, event):
        gbp = self.gbp.get()
        currency_price = currency_calc()
        currency_price[1] *=  float(gbp) 
        
        self.jpy_rate.set('{:.2f}'.format(currency_price[1]))
        self.usd_rate.set('{:.2f}'.format(currency_price[1] / currency_price[0]))
        self.eur_rate.set('{:.2f}'.format(currency_price[1] / currency_price[2]))
    
    def eur_func(self, event):
        eur = self.eur.get()
        currency_price = currency_calc()
        currency_price[2] *=  float(eur) 
        
        self.jpy_rate.set(str('{:.2f}'.format(currency_price[2])))
        self.usd_rate.set('{:.2f}'.format(currency_price[2] / currency_price[0]))
        self.gbp_rate.set('{:.2f}'.format(currency_price[2] / currency_price[1]))
        
        
def main():
    app = App()    
    app.mainloop()
    
if __name__ == "__main__":
    main()