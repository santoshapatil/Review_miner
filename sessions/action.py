#action
import pandas as pd
def action_log(session_id,marketplace,product_url,ext_time):
    #action=pd.DataFrame(columns={"session_id","marketplace","product_url"},index=None)
    action=pd.read_csv(r'action.csv',index_col=False)
    act={"session_id":[session_id],"marketplace":[marketplace],"product_url":[product_url],"extraction_time":[ext_time]}
    action.loc[len(action["session_id"])]=act

    action.to_csv("action.csv",index=False)
