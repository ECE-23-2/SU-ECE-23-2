# https://towardsdatascience.com/read-and-edit-image-metadata-with-python-f635398cd991
from exif import Image

# folder_path = 'imagesFolder'
# img_filename = 'Test1-0_Fixed.JPEG'
# img_path = f'{folder_path}/{img_filename}'
#
#
# copyrightData = "Jessica 2023"
# dateTimeData = "2023-02-07 13:04"
# coordinateData = "0, -14"
def writeData(dateTimeData, coordinateData, folder_path, img_filename):
    img_path = f'{folder_path}/{img_filename}'

    # Open image
    with open(img_path, 'rb') as img_file:
        img = Image(img_file)

    print("\nWriting Data...")

    # Add new attribute (Copyright)
    # img.copyright = copyrightData

    # Add new attribute (Datetime)
    img.datetime = dateTimeData

    # Add new attribute (ImageID)
    img.image_unique_id = coordinateData

    # Add new attribute (ExifTag)
    # img.flash = 1

    with open(f'{folder_path}/{img_filename}', 'wb') as new_image_file:
        new_image_file.write(img.get_file())

    print("Done writing\n")