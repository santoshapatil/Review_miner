import pandas as pd
import sqlite3 as sql

def rev_warehouse(Reviews) :
    #def __init__(self, product_url, l_date_time,Reviews):
        #self.product_url = product_url
		#self.l_date_time = l_date_time
        #self.Reviews = Reviews

    #def warehouse_reviews(self):
        #rev=Reviews.copy()
        #rev["l_date_time"]=l_date_time
        #rev["Product_url"]=product_url
    rev_warehouse=pd.DataFrame(index=None)
        #rev_warehouse=pd.read_csv(r"rev_warehouse.csv",index_col=False)

    rev_warehouse=rev_warehouse.append(Reviews,ignore_index=True)
    rev_warehouse.to_csv("rev_warehouse.csv",index=False)




    #Rev_warehouse = sql.connect('Rev_warehouse.db')
    #c=Rev_warehouse.cursor()
    #c.execute('''CREATE TABLE Review_box
             #([log_id] INTEGER PRIMARY KEY,[product_url] text, [l_date_time] date)''')

    #new_db={"product_url":[product_url],"log_id":[log_id],"l_date_time":[l_date_time]}
    #rev_warehouse=pd.read_csv(r'rev_warehouse.csv')
