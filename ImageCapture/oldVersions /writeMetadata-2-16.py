# https://towardsdatascience.com/read-and-edit-image-metadata-with-python-f635398cd991
from exif import Image

folder_path = 'imagesFolder'
img_filename = 'MetaTest-0.JPEG'
img_path = f'{folder_path}/{img_filename}'

copyrightData = "Jessica 2022"
dateTimeData = "2023-02-07 13:04"
coordinateData = "5, 7"
def writeData():
    # Open image
    with open(img_path, 'rb') as img_file:
        img = Image(img_file)

    print("\nWriting Data...")

    # Add new attribute (Copyright)
    img.copyright = copyrightData

    # Add new attribute (Datetime)
    img.datetime = dateTimeData

    # Add new attribute (ImageID)
    img.image_unique_id = coordinateData

    # Add new attribute (ExifTag)
    img.flash = 1

    with open(f'{folder_path}/{img_filename}', 'wb') as new_image_file:
        new_image_file.write(img.get_file())

    print("Done writing\n")
