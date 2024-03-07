from dotenv import load_dotenv
load_dotenv()

from api import generate_cogview_image


def cogview_example():
    image_prompt = "国画，孤舟，蓑笠翁，独钓，寒江雪，静谧的氛围，江水，古风情怀，精细的细节。"
    image_url = generate_cogview_image(image_prompt)
    
    print("image_prompt:")
    print(image_prompt)
    print("image_url:")
    print(image_url)

if __name__ == "__main__":
    cogview_example()
