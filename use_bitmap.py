from PIL import Image
def main():
    try:
        # Relative Path
        img = Image.open("/home/tanuja/Downloads/PHOTOS/BAD_PHOTOS/STSEP191087595_photo_old.jpeg")
        print img.mode
        print img.size
        print dir(img)
        print img.info
        print img._getexif()
        # converting image to bitmap
        print img.tobitmap()

        print type(img.tobitmap(name='b'))
    except IOError as e:
        print e
    except Exception as e:
        print "error"
        print e.message


if __name__ == "__main__":
    main()
