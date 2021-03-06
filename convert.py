# coding=utf8
# Пример запуска:
# TARGET_DIR= gimp -idf --batch-interpreter python-fu-eval -b "execfile('convert.py')"
# Подставьте в TARGET_DIR адрес директории с картинками. Внутри должна быть создана поддиректория converted.

from os import environ, listdir
import os.path

from gimpfu import pdb


# Максимальные ширина и высота пережатой фотографии:
MAX_WIDTH = 1920
MAX_HEIGHT = 1280


def get_images(target_dir):
    '''
    Возвращает список картинок для обработки.
    @param target_dir: string
    @return: list
    '''
    images = [filename for filename in listdir(target_dir) if filename.lower().endswith('jpg')]
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
    if width <= MAX_WIDTH and height <= MAX_HEIGHT:
        return width, height
    if width > height:
        return MAX_WIDTH, int(MAX_WIDTH * height / width)
    return int(MAX_HEIGHT * width / height), MAX_HEIGHT


def convert_image(target_dir, output_dir, image_name):
    '''
    Обрабатывает картинку.
    @param target_dir: string
    @param output_dir: string
    @param image_name: string
    '''
    output_path = os.path.join(output_dir, image_name)
    if os.path.exists(output_path):
        print '%s already exists, skipping'%image_name
        return
    image = pdb.file_jpeg_load(os.path.join(target_dir, image_name), image_name)
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
    pdb.gimp_file_save(image, layer, output_path, image_name)
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
    output_dir = os.path.join(target_dir, 'converted')
    if check_dirs(target_dir, output_dir):
        print 'converting images from %s to %s'%(target_dir, output_dir)
        images = get_images(target_dir)
        convert_images(target_dir, output_dir, images)
    pdb.gimp_quit(1)


run()
