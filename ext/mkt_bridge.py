from ext.amzengine import Review_extract as amz
from ext.flipkartengine import Review_extract as flipkart

def build_bridge(mkt,product_url):
    if mkt =="amazon.in":
       data,p_name,pimg,error=amz(product_url)
       return data,p_name,pimg,error
    elif mkt=="flipkart.com":
       data,p_name,error=flipkart(product_url)
       return data,p_name,error

       
    
