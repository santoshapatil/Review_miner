from PIL import Image,ImageDraw
import streamlit as st

def template(pimg,p_name,mkt):
    image=pimg
    # if image.format =="JPEG":
        

# The pixel format used by the image. Typical values are "1", "L", "RGB", or "CMYK."
    
    
    st.image(pimg)
    image.thumbnail((400, 400)) 
    print(image.size)
    img = Image.new('RGB', (400, 700), (242, 242, 240))
    img.paste(image,(0,700-image.size[1]))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0),(400,700)],width=2,outline=(0, 0, 0))
    
    st.info("go")
    with st.beta_container():
           st.image(img)

    

    

    







image = Image.open('img.jpg')
p_name="Mcovid® Anti Pollution, Reusable, Non-woven Protective Layer Face Mask CE and ISO Certified"
mkt="amazon"
template(image,p_name,mkt)