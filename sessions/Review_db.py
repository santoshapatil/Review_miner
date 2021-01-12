import pandas as pd
import sqlite3 as sql
def rev_warehouse(lid,product_url,l_date_time,Reviews):
    #Rev_warehouse = sql.connect('Rev_warehouse.db')
    #c=Rev_warehouse.cursor()
    #c.execute('''CREATE TABLE Review_box
             #([log_id] INTEGER PRIMARY KEY,[product_url] text, [l_date_time] date)''')
    # this line after file is ready
    # rev_warehouse=pd.DataFrame(index=None)
    rev_warehouse=pd.read_csv(r"rev_warehouse.csv",index_col=False)
    
    Reviews["l_date_time"]=l_date_time
    Reviews["Product_url"]=product_url
    Reviews["session_id"]=lid

    #new_db={"product_url":[product_url],"log_id":[log_id],"l_date_time":[l_date_time]}

    rev_warehouse=rev_warehouse.append(Reviews,ignore_index=True)
    rev_warehouse.to_csv("rev_warehouse.csv",index=False)
