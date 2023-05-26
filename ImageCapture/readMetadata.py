# https://towardsdatascience.com/read-and-edit-image-metadata-with-python-f635398cd991
from exif import Image

# # Assumes all images are being saved to imagesFolder with in project folder
# folder_path = 'imagesFolder'
# # Change  filename to photo to read
# img_filename = 'MetaTest-0.JPEG'
# img_path = f'{folder_path}/{img_filename}'

def checkForData(folder_path, img_filename):
    img_path = f'{folder_path}/{img_filename}'
    # Open image
    with open(img_path, 'rb') as img_file:
        img = Image(img_file)

    # Print if Image has exif (metadata) data
    if img.has_exif == False:
        print(img_filename +" does not have metadata")
    else:
        print(img_filename +" has metadata")

    # print(img.has_exif)

    # https://exif.readthedocs.io/en/latest/api_reference.html#image-attributes list of image attributes
    # Print all exif data tiles
    for item in sorted(img.list_all()):
        print(item)

def printTags(folder_path, img_filename):
    img_path = f'{folder_path}/{img_filename}'
    # Open image
    with open(img_path, 'rb') as img_file:
        img = Image(img_file)

    # https://exiv2.org/tags.html tag formats
    # Can use DateTime
    # Localization ImageID

    # Check updated metadata
    # print(f'Copyright: {img.get("copyright")}')
    print(f'DateTime: {img.get("datetime")}')
    print(f'ImageID (Coordinates): {img.get("image_unique_id")}')
    # print(f'Flash: {img.get("flash")}')

    print("Done\n")











