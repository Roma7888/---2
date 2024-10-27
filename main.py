from tkinter import image_types

from rasterio.rio.options import output_opt

from show_channels import display_all_channels
from data_visualiation import plot_data
from devide_big_data_into_tile_dataset import split_image
from segmantation import detect_water_from_single_file

image_path = "train/images/4.tif"
mask_path = "train/masks/4.tif"
output_folder = "data/"


input_path = 'train/images/4.tif'
output_path = 'segmentated_masks/4.tif'

# Пример использования функции

# Пример использования функции
detect_water_from_single_file(
    input_tif=input_path,
    output_path=output_path
)
plot_data(input_path, output_path)

"""plot_data(image_path, mask_path)
split_image(
    image_path=image_path,
    mask_path=mask_path,
    output_folder=output_folder,
    tile_size=256,
    overlap=32,
    image_id=2
    )

tile_image_path = 'data/images/tile_2_0.tif'
tile_mask_path = 'data/masks/tile_2_0.tif'
plot_data(tile_image_path, tile_mask_path)"""
