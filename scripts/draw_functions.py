from luma.core.render import canvas
from PIL import ImageFont, Image

def drawPauseSymbol(device):
    with canvas(device) as draw:
        rectangle1 = (-13 + device.width // 2,
                      -22 + device.height // 2,
                      -5 + device.width // 2,
                      22 + device.height // 2)
        rectangle2 = (5 + device.width // 2,
                      -22 + device.height // 2,
                      13 + device.width // 2,
                      22 + device.height // 2)
        draw.rectangle(rectangle1, outline="white", fill="white")
        draw.rectangle(rectangle2, outline="white", fill="white")

def drawPlaySymbol(device):
    with canvas(device) as draw:
        triangle = [(-19, - 24), (25, 0), (-19, 24)]
        triangle = [(x[0] + device.width // 2, x[1] + device.height // 2) for x in triangle]
        draw.polygon(triangle, outline="white", fill="white")

def drawImage(device, img_path):
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)
    background = Image.new("RGBA", device.size, "black")
    posn = ((device.width - logo.width) // 2, (device.height - logo.height) // 2)
    img = Image.composite(logo, fff, logo)
    background.paste(img, posn)
    device.display(background.convert(device.mode))

def drawCover(device, img_path):
    # basewidth = device.width
    cover = Image.open(img_path).convert("RGBA")
    # background = Image.new("RGBA", device.size, "black")
    # wpercent = (basewidth / float(cover.size[0]))
    # hsize = int((float(cover.size[1]) * float(wpercent)))
    # cover = cover.resize((basewidth, hsize), Image.ANTIALIAS)
    cover.thumbnail(device.size, Image.ANTIALIAS)
    background = Image.new("RGBA", device.size, "black")
    posn = ((device.width - cover.width) // 2, (device.height - cover.height) // 2)
    background.paste(cover, posn)
    device.display(background.convert(device.mode))