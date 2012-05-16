# coding=utf8
# Пример запуска:
# TARGET_DIR= gimp -idf --batch-interpreter python-fu-eval -b "execfile('convert.py')"
# Подставьте в TARGET_DIR адрес директории с картинками. Внутри должна быть создана поддиректория converted.

from os import environ, listdir
import os.path

from gimpfu import pdb


def get_images(target_dir):
    '''
    Возвращает список картинок для обработки.
    @param target_dir: string
    @return: list
    '''
    images = [filename.lower().endswith('jpg') for filename in listdir(target_dir)]
    images.sort()
    return images


def get_image_new_dimensions(image):
    '''
    Возвращает новые размеры картинки с сохранением пропорций.
    @param image: object
    @return: int, int
    '''
    width = pdb.gimp_image_width(image)
    height = pdb.gimp_image_height(image)
    if width > height:
        new_width = 1920
        new_height = new_width * height / width
    else:
        new_height = 1280
        new_width = new_height * width / height
    return new_width, new_height


def convert_image(target_dir, output_dir, image_name):
    '''
    Обрабатывает картинку.
    @param target_dir: string
    @param output_dir: string
    @param image_name: string
    '''
    image = pdb.file_jpeg_load('%s/%s'%(target_dir, image_name), image_name)
    layer = image.layers[0]
    # Выравниваем уровни:
    # pdb.gimp_levels_stretch(layer)
    # Добавляем нерезкую маску:
    # pdb.plug_in_unsharp_mask(image, layer, 5, 0.5, 0)
    # Изменяем размер картинки:
    width, height = get_image_new_dimensions(image)
    pdb.gimp_image_scale(image, width, height)
    # Автоматически увеличиваем контраст:
    pdb.plug_in_c_astretch(image, layer)
    # Повышаем резкость:
    pdb.plug_in_sharpen(image, layer, 50)
    pdb.gimp_file_save(image, layer, '%s/%s'%(output_dir, image_name), image_name)
    pdb.gimp_image_delete(image)


def convert_images(target_dir, output_dir, images):
    '''
    Обрабатывает картинки.
    @param target_dir: string
    @param output_dir: string
    @param images: list
    '''
    count = len(images)
    for i, image_name in enumerate(images):
        print 'converting %s (%s/%s)'%(image_name, i + 1, count)
        convert_image(target_dir, output_dir, image_name)
        
        
def check_dirs(target_dir, output_dir):
    '''
    Возвращает, корректно ли указаны директории.
    @param target_dir: string
    @param output_dir: string
    @return: bool
    '''
    if target_dir is None:
        print '!!! please specify the target directory via the environment variable $TARGET_DIR'
        return False
    if not os.path.exists(target_dir):
        print '!!! looks like the target directory %s does not exist'%target_dir
        return False
    if not os.path.exists(output_dir):
        print '!!! looks like the ouput directory %s does not exist'%output_dir
        return False
    return True


def run():
    '''
    Запускает обработку.
    '''
    target_dir = environ.get('TARGET_DIR')
    output_dir = '%s/converted/'%target_dir
    if check_dirs(target_dir, output_dir):
        print 'converting images from %s to %s'%(target_dir, output_dir)
        images = get_images(target_dir)
        convert_images(target_dir, output_dir, images)
    pdb.gimp_quit(1)


run()
