import os.path
import platform
from shutil import rmtree
from pathlib import Path

# Menu principal del sistema
opc_menu_principal = ['Leer Receta', 'Crear Receta', 'Crear Categoría', 'Eliminar Receta',
                      'Eliminar Categoría', 'Finalizar Programa']

# Variables globales
home_path = os.path.dirname(os.path.abspath(__file__))
name_dir = 'Recetas'
run = True


def clear_screen():
    """
    Limpia la pantalla
    :return: none
    """
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def asteriscos():
    """
    Imprime 88 asteriscos en línea
    :return: none
    """
    print('*' * 88)


def txt_files_elements():
    """
    Almacena en una lista el nombre de los archivos con extensión txt que se encuentran en los
    subdirectorios de Recetas.
    :return: Devuelve la ruta absoluta del directorio de recetas,
    El total de archivos en el directorio de Recetas,
    El nombre de los archivos almacenados en los subdirectorios
    """
    ruta = Path(home_path, name_dir)
    txt_files = Path(name_dir).glob('**/*.txt')
    txt_files_count = 0
    txt_recipe_names = set()

    for txt_file in txt_files:
        txt_files_count += 1
        txt_recipe_names.add(txt_file.parent.stem)

    return txt_recipe_names, ruta, txt_files_count


def leer_categories():
    """
    Retorna una lista con los nombres de los subdirectorios - Categorías
    :return:
    """
    list_categories = []

    for child in Path(home_path, name_dir).iterdir():
        list_categories.append(child.stem)

    return list_categories


def leer_recipes_of_category(category, action):
    """
    Almacena en una lista las recetas "archivos txt" por categoría
    :param category: Nombre de la categoría
    :param action: r = read or d = delete
    :return:
    """
    category_path = Path(name_dir, category)
    recipe_list = []

    clear_screen()

    print(f'Usted ha seleccionado la categoría de: {category_path.stem}')
    asteriscos()

    for index, recipe in enumerate(category_path.glob('**/*')):
        recipe_list.append(recipe)
        print(f"[{index + 1}] - {recipe.stem}")

    print('[r] - Menú Anterior')
    asteriscos()

    recipe_choice: str = input('Elige una categoría de receta: ')

    if recipe_choice.isnumeric() and int(recipe_choice) not in range(1, len(recipe_list) + 1):
        print('Opción no válida, ingrese una opción nuevamente.')
        input('Presiona la tecla enter para continuar')
        leer_recipes_of_category(category, action)
    elif recipe_choice == 'r' and action == 'r':
        leer_recipe()
    elif recipe_choice == 'r' and action == 'd':
        eliminar_recipe()
    elif action == 'd':
        eliminar_file_recipe(recipe_list[int(recipe_choice) - 1])
    else:
        mostrar_recipe(recipe_list[int(recipe_choice) - 1])


def mostrar_recipe(recipe):
    """
    Abre el archivo correspondiente a la categoría y la receta para mostrar su contenido en pantalla
    :param recipe: Nombre de la receta
    :return:
    """
    recipe_path = Path(recipe)
    recipe_read = recipe_path.read_text()

    clear_screen()
    print(f"La receta que esta leyendo es: {recipe}")
    asteriscos()
    print(recipe_read)
    asteriscos()
    print('\n')
    input('Presiona la tecla enter para continuar')


def leer_recipe():
    """
    Muestra en pantalla el menu de categorías
    :return:
    """
    categories_list = leer_categories()
    clear_screen()

    print('Menú de Categorías')
    asteriscos()

    for index, category in enumerate(categories_list):
        print(f"[{index + 1}] - {category}")

    print('[r] - Menú Principal')
    asteriscos()

    category_choice = input('Elige una categoría: ')

    if category_choice.isnumeric() and int(category_choice) not in range(1, len(categories_list) + 1):
        print('Opción no válida, ingrese una opción nuevamente.')
        input('Presiona la tecla enter para continuar')
        leer_recipe()
    elif category_choice == "r":
        print('Menu Principal')
    else:
        leer_recipes_of_category(categories_list[int(category_choice) - 1], 'r')


def create_new_category(category):
    """
    Crea una nueva categoría
    :param category: Nombre de la Categoría
    :return:
    """
    new_category = Path(home_path, name_dir, category)

    if not os.path.exists(new_category):
        os.makedirs(new_category)
        print(f'Se ha creado la categoría de {category}')
        input('Presiona la tecla enter para continuar')
    else:
        print('La categoría ya existe')
        input('Presiona la tecla enter para continuar')


def create_category():
    """
    Recibe el nombre de una categoría para crearla
    :return:
    """
    clear_screen()
    print('Crear Categoría')
    asteriscos()
    category_name = input('Ingrese el nombre de la categoría: ')
    category_name = category_name.capitalize()
    create_new_category(category_name)


def eliminar_category():
    """
    Elimina una categoría
    :return:
    """
    clear_screen()

    print('Eliminar Categoría')
    asteriscos()

    categories_list = leer_categories()

    print('Las categorías que actualmente existen son:')

    for index, category in enumerate(categories_list):
        print(f"[{index + 1}] - {category}")

    print('[r] - Menú Principal')
    asteriscos()
    category_choice = input('Elige una categoría: ')

    if category_choice.isnumeric() and int(category_choice) not in range(1, len(categories_list) + 1):
        print('Opción no válida, ingrese una opción nuevamente.')
        input('Presiona la tecla enter para continuar')
        eliminar_category()
    elif category_choice == 'r':
        print('Menu Principal')
    else:
        eliminar_dir_category(categories_list[int(category_choice) - 1])


def eliminar_dir_category(category):
    """
    Elimina el directorio con todo su contenido dentro
    :param category: Nombre de la categoría a eliminar
    :return:
    """
    clear_screen()
    print(f"Eliminar la categoría de: {category}")
    asteriscos()

    category_check, category_path = category_check_exists(category)

    if category_check:
        rmtree(category_path)
        categories_list = leer_categories()

        for index, category in enumerate(categories_list):
            print(f"[{index + 1}] - {category}")

        asteriscos()
        print(f'La categoría {category} ha sido eliminada con éxito con todo su contenido')
        input('Presione la tecla enter para continuar')
    else:
        print('La categoría no existe')
        input('Presione la tecla enter para continuar')


def category_check_exists(category):
    """
    Revisa si la categoría existe
    :param category: Nombre de la categoría
    :return: El path de la categoría
    """
    category_check = Path(home_path, name_dir, category)
    if os.path.exists(category_check):
        return True, category_check
    else:
        return False, category_check


def recipe_check_exist(category, recipe_name):
    """
    Comprueba que la receta existe en la categoría
    :param category: Nombre de la categoría
    :param recipe_name: Nombre de la receta
    :return: true or false
    """
    ruta_files = Path(name_dir, category)
    txt_files = ruta_files.glob('*.txt')
    for txt_file in txt_files:
        if txt_file.stem == recipe_name:
            return True
        else:
            return False


def recipe_create_file(category_path, recipe_name):
    """
    Crea el archivo de la receta en la categoría seleccionada
    :param category_path: El path de la categoría
    :param recipe_name: El nombre de la receta
    :return: true or false
    """
    print(recipe_name)
    recipe_file_name = open(f'{Path(category_path, recipe_name)}.txt', 'x')
    recipe_file_name.close()
    files_on_dir = os.listdir(category_path)

    if recipe_name + '.txt' in files_on_dir:
        return True
    else:
        return False


def recipe_write_file(category_path, recipe_name, content):
    """
    Escribe el contenido de un input en el archivo de la receta de la categoría seleccionada
    :param category_path: Path de la categoría
    :param recipe_name: Nombre de la receta
    :param content: Contenido del archivo
    :return:
    """
    print(f"Receta de {recipe_name}")
    recipe_file_name = open(f'{Path(category_path, recipe_name)}.txt', 'a')
    recipe_file_name.write(f'{recipe_name}\n')
    recipe_file_name.write(content)
    recipe_file_name.close()


def recipe_create():
    """
    Crea una receta en relación con la categoría seleccionada
    :return:
    """
    clear_screen()
    print('Crear una receta')
    print('Las categorías existentes son:')
    asteriscos()

    categories_list = leer_categories()
    recipe_name = ''

    for index, category in enumerate(categories_list):
        print(f"[{index + 1}] - {category}")

    print(f'[r] - Menú Principal')
    asteriscos()
    category = input('Elige una categoría para la receta: ')

    if category.isnumeric() and int(category) not in range(1, len(categories_list) + 1):
        print('Opción no válida, ingrese una opción nuevamente.')
        input('Presiona la tecla enter para continuar')
        recipe_create()
    elif category == 'r':
        print('Menu Principal')
    else:
        category_check, category_path = category_check_exists(categories_list[int(category) - 1])

        if category_check:
            clear_screen()
            print(f'La receta será creada en la categoría de: {categories_list[int(category) - 1]}')
            print(f'En la siguiente ruta: {category_path}')
            asteriscos()
            recipe_name = input('Ingrese el nombre de la receta: ')
            recipe_name = recipe_name.capitalize()
        else:
            print('La categoría ingresada no existe')
            input('Presione la tecla enter para continuar')

        recipe_exist = recipe_check_exist(categories_list[int(category) - 1], recipe_name)

        if recipe_exist:
            print(f'La receta {recipe_name} ya existe, por favor ingrese otro nombre')
            input('Presione la tecla enter para continuar')

        if recipe_create_file(category_path, recipe_name):
            print(f'El archivo de la receta {recipe_name} fue creado exitosamente')
            print('Ahora escribe a continuación la receta para que sea grabada en el archivo')
            input('Presione la tecla enter para continuar')
            clear_screen()
            recipe_content = input('Escribe la receta a continuación: ')
            recipe_write_file(category_path, recipe_name, recipe_content)
            print('La receta ha sido escrita correctamente')
            input('Presione la tecla enter para continuar')

        else:
            print('Algo ha salido mal, intentalo nuevamente')
            input('Presione la tecla enter para continuar')


def eliminar_recipe():
    """
    Elimina una receta
    :return:
    """
    clear_screen()
    print('Eliminar Receta')
    asteriscos()

    categories_list = leer_categories()
    print('Las categorías que actualmente existen son:')

    for index, category in enumerate(categories_list):
        print(f'[{index + 1}] - {category}')

    print('[r] - Menú Principal')
    asteriscos()
    category_choice = input('Elige una categoría: ')

    if category_choice.isnumeric() and int(category_choice) not in range(1, len(categories_list) + 1):
        print('Opción no válida, ingrese una opción nuevamente.')
        input('Presiona la tecla enter para continuar')
        eliminar_recipe()
    elif category_choice == 'r':
        print('Menu Principal')
    else:
        leer_recipes_of_category(categories_list[int(category_choice) - 1], 'd')


def eliminar_file_recipe(recipe):
    """
    Elimina el archivo de una receta
    :param recipe: Nombre de la receta
    :return:
    """
    recipe_path = Path(recipe)
    clear_screen()
    print(f"La receta que esta a punto de eliminar es: {recipe}")
    asteriscos()
    response = input('Esta seguro de realizar está acción: S/N: ')

    response = response.lower()

    if response == 's':
        os.remove(recipe_path)
        print('La receta ha sido eliminada correctamente')
        input('Presiona la tecla enter para continuar')
    elif response == 'n':
        print('Menu Principal')
    elif response.isnumeric() or response != 's' or response != 'n':
        print('Opción no válida, ingrese una opción nuevamente.')
        input('Presiona la tecla enter para continuar')


def menu_principal():
    """
    Menu Principal del sistema
    :return: 
    """
    clear_screen()
    recipes_categories, recipes_directory, recipes_count = txt_files_elements()
    print(f"Este recetario cuenta con {recipes_count} receta(s)")
    print(f"El directorio en donde se encuentran las recetas es: {recipes_directory}")

    print('Menú Principal')
    asteriscos()

    for index, opc in enumerate(opc_menu_principal):
        print(f'[{index + 1}] - {opc}')

    asteriscos()
    opc_choicer: str = input('Elige una opción listada en el menú: ')

    return opc_choicer


while run:
    opc_choice = menu_principal()
    opc_choice = int(opc_choice)
    if opc_choice == 1:
        leer_recipe()
    elif opc_choice == 2:
        recipe_create()
    elif opc_choice == 3:
        create_category()
    elif opc_choice == 4:
        eliminar_recipe()
    elif opc_choice == 5:
        eliminar_category()

    if opc_choice == 6:
        run = False
else:
    print('Que tengas un excelente día!')
