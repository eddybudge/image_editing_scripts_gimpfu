from gimpfu import *

L=256#intensity levels

def mynormalization(img, layer, min, max):#new [min] and new [max] intensities are the arguments that are passed by the user

	#Define what should be "undone" - even if it doesn't sem to work
	pdb.gimp_image_undo_group_start(img)
	#progress bar
	gimp.progress_init("Normalizing " + layer.name + "...")
	#We can work on an RGB image too: we will convert it to a grayscale image ->
	if(not pdb.gimp_drawable_is_gray(layer)):
		pdb.gimp_image_convert_grayscale(img)

	#normalization step: if pixel value is less or equal to [min] then set it to 0, otherwise if it's
	#greater or equal to [max], then set it to L-1. In all other cases compute the normalised value
	for x in range(layer.width):
		gimp.progress_update(float(x) / float(layer.width))#some special effects: the update of the progress bar ^_^
		for y in range(layer.height):
			pixel=layer.get_pixel(x,y)[0]
			if(pixel<=min):
				layer.set_pixel(x,y,(0,))
			else:
				if(pixel>=max):
					layer.set_pixel(x,y,(L-1,))
				else:
					new_value = int(round((pixel-min)*(L-1)/(max-min)))#normalization formula
					layer.set_pixel(x,y,(new_value,))

	# Update the layer
	layer.update(0, 0, layer.width, layer.height)
	pdb.gimp_image_undo_group_end(img)
	# End progress.
	pdb.gimp_progress_end()
	return True

register(
         "python-fu-mynormalization",
         N_("Normalizzazione"),
         "A variant of normalization.",
         "Yana",
         "Yana",
         "16/04/2020",
         N_("_My normalization"),
         "GRAY, RGB",
         [
          (PF_IMAGE, "image",       "Input RGB or GRAYSCALE image", None),
          (PF_DRAWABLE, "drawable", "Input RGB or GRAYSCALE drawable", None),
          (PF_INT8, "min", "Min Intensity", 0),
          (PF_INT8, "max", "Max Intensity", L-1)
          ],
         [],
         mynormalization,
         menu="<Image>/Filters/My plug in menu",
         domain=("gimp20-python", gimp.locale_directory)
         )
main()
