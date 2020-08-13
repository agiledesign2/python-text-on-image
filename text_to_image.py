# How to Wrap Text on Image using Python

# I will be using the extension library pillow to draw text on an image.  
# I used the following classes from pillow:
#	Image : to create an image object for our text
#   ImageDraw: to create a drawing context
#   ImageFont: font of the text we will be drawing on the image

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import randint

#create image object from the input image path
try:
    image = Image.open('./eyong.jpg')
 
    
except IOError as e:
    print(e)

# Resize the image 
width = 500
img_w = image.size[0]
img_h = image.size[1]
wpercent = (width/float(img_w))
hsize = int((float(img_h)*float(wpercent)))
rmg = image.resize((width,hsize), Image.ANTIALIAS)
print( rmg.size)

# Set x boundry
# Take 8% to the left for min and 50% to the left for max
x_min = (rmg.size[0] * 8) // 100
x_max = (rmg.size[0] * 50) // 100
print(x_min, x_max)

# Generate the random positioning
ran_x = randint(x_min, x_max)
print(ran_x)

# Create font object with the font file and specify desired size
# Font style is `arial` and font size is 20
font_path = 'font/arialbd.ttf'
font = ImageFont.truetype(font=font_path, size=20)


#Spliting text to multiple line captioning

#    If text is shorter than the maximum width, then it can fit in one line. Return without splitting
#    Split the text using spaces to get each words
#    Create short texts by appending words while the width is smaller than the maximum width.
def text_wrap(text, font, max_width):
    """ Split text and find line height """
    lines = []
    
    # If the text width is smaller than the image width, then no need to split
    # just add it to the line list and return
    if font.getsize(text)[0]  <= max_width:
        lines.append(text)
    else:
        #split the line by spaces to get words
        words = text.split(' ')
        i = 0
        # append every word to a line while its width is shorter than the image width
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i]+ " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines


def draw_text(text):
    """ Draw text """   
    # open the background file
    img = Image.open('./xander_1.jpg')
    
    # size() returns a tuple of (width, height) 
    image_size = img.size 
 
    # create the ImageFont instance
    font_file_path = 'font/arialbd.ttf'
    font = ImageFont.truetype(font_file_path, size=50, encoding="unic")
 
    # get shorter lines
    lines = text_wrap(text, font, image_size[0])
    print(lines) # ['This could be a single line text ', 'but its too long to fit in one. ']

#print(draw_text("This could be a single line text but its too long to fit in one."))
 
# Caption
text = "This could be a single line text but its too long to fit in one."
lines = text_wrap(text, font, rmg.size[0]-ran_x)
line_height = font.getsize('hg')[1]

y_min = (rmg.size[1] * 4) // 100   # 4% from the top
y_max = (rmg.size[1] * 90) //100   # 90% to the bottom
y_max -= (len(lines)*line_height)  # Adjust base on lines and height
ran_y = randint(y_min, y_max)      # Generate random point

rmg = rmg.filter(ImageFilter.SMOOTH_MORE)

#Create draw object
draw = ImageDraw.Draw(rmg)

color = 'rgb(255,0,0)'  # Red color
x = ran_x
y = y_max

for line in lines:
    draw.text((x,y), line, fill=color, font=font)
    
    y = y + line_height

author = "- Eyong Kevin"
y += 5                        # Add some line space
x += 20                       # Indent a bit to the right
draw.text((x,y), author, fill=color, font=font)
rmg.show()

# Save captioned image
rmg.save('./eyong_kevin.jpg')
