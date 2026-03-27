from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(filename, text, width=600, height=400):
    """
    生成一个带有边框和提示文字的占位图片，用于表示用户需要手动截取的功能界面
    """
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([0, 0, width-1, height-1], outline='#CCCCCC', width=2)
    
    # Draw cross (optional, standard placeholder style)
    draw.line([0, 0, width, height], fill='#EEEEEE', width=2)
    draw.line([0, height, width, 0], fill='#EEEEEE', width=2)
    
    # Draw text
    try:
        # Try to load a nice font
        font = ImageFont.truetype("msyh.ttc", 24)
    except:
        font = ImageFont.load_default()
        
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    
    # Draw text background
    draw.rectangle(
        [(width-text_w)/2 - 10, (height-text_h)/2 - 10, (width+text_w)/2 + 10, (height+text_h)/2 + 10],
        fill='white', outline='#999999'
    )
    
    draw.text(((width-text_w)/2, (height-text_h)/2), text, fill='#666666', font=font)
    
    img.save(filename)
    print(f"Generated placeholder: {filename}")
