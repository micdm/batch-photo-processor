# coding=utf8
# TARGET_DIR= gimp -idf --batch-interpreter python-fu-eval -b "execfile('convert.py')"

from os import environ, listdir

from gimpfu import pdb

def get_images(target_dir):
	'''
	Возвращает список картинок для обработки.
	'''
	all_files = listdir(target_dir)
	images = filter(lambda filename: filename.lower().endswith('jpg'), all_files)
	images.sort()
	return images

def convert_image(target_dir, output_dir, image_name):
	image = pdb.file_jpeg_load('%s/%s'%(target_dir, image_name), image_name)
	layer = image.layers[0]
	#pdb.gimp_levels_stretch(layer)
	#pdb.plug_in_unsharp_mask(image, layer, 5, 0.5, 0)
	width = pdb.gimp_image_width(image)
	height = pdb.gimp_image_height(image)
	if width > height:
	    new_width = 1920
	    new_height = new_width * height / width
	else:
	    new_height = 1280
	    new_width = new_height * width / height
	pdb.gimp_image_scale(image, new_width, new_height)
	pdb.plug_in_c_astretch(image, layer)
	pdb.plug_in_sharpen(image, layer, 50)
	pdb.gimp_file_save(image, layer, '%s/%s'%(output_dir, image_name), image_name)
	pdb.gimp_image_delete(image)

def convert_images(target_dir, output_dir, images):
	'''
	Обрабатывает картинки.
	'''
	count = len(images)
	for i, image_name in zip(range(count), images):
		print 'Converting %s (%s/%s)'%(image_name, i + 1, count)
		convert_image(target_dir, output_dir, image_name)

def run():
	target_dir = environ.get('TARGET_DIR')
	if target_dir is None:
		print 'Please specify the target directory via the environment variable $TARGET_DIR'
		return
	print 'Converting images from %s'%target_dir
	images = get_images(target_dir)
	output_dir = '%s/converted/'%target_dir
	convert_images(target_dir, output_dir, images)
	pdb.gimp_quit(1)

run()
