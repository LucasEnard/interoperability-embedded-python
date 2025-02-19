import iris
import os
import ast

def raise_on_error(sc):
    """
    If the status code is an error, raise an exception
    
    :param sc: The status code returned by the Iris API
    """
    if iris.system.Status.IsError(sc):
        raise RuntimeError(iris.system.Status.GetOneStatusText(sc))

def register_component(module:str,classname:str,path:str,overwrite:int,iris_classname:str):
    """
    It registers a component in the Iris database.
    
    :param module: The name of the module that contains the class
    :type module: str
    :param classname: The name of the class you want to register
    :type classname: str
    :param path: The path to the component
    :type path: str
    :param overwrite: 0 = no, 1 = yes
    :type overwrite: int
    :param iris_classname: The name of the class in the Iris class hierarchy
    :type iris_classname: str
    :return: The return value is a string.
    """

    return iris.cls('Grongier.PEX.Utils').dispatchRegisterComponent(module,classname,path,overwrite,iris_classname)

def register_folder(path:str,overwrite:int,iris_package_name:str):
    """
    > This function takes a path to a folder, and registers all the Python files in that folder as IRIS
    classes
    
    :param path: the path to the folder containing the files you want to register
    :type path: str
    :param overwrite: 
    :type overwrite: int
    :param iris_package_name: The name of the iris package you want to register the file to
    :type iris_package_name: str
    """
    for filename in os.listdir(path):
        if filename.endswith(".py"): 
            register_file(filename, path, overwrite, iris_package_name)
        else:
            continue


def register_file(filename:str,path:str,overwrite:int,iris_package_name:str):
    """
    It takes a file name, a path, a boolean to overwrite existing components, and the name of the Iris
    package that the file is in. It then opens the file, parses it, and looks for classes that extend
    BusinessOperation, BusinessProcess, or BusinessService. If it finds one, it calls register_component
    with the module name, class name, path, overwrite boolean, and the full Iris package name
    
    :param filename: the name of the file containing the component
    :type filename: str
    :param path: the path to the directory containing the files to be registered
    :type path: str
    :param overwrite: if the component already exists, overwrite it
    :type overwrite: int
    :param iris_package_name: the name of the iris package that you want to register the components to
    :type iris_package_name: str
    """
    #pour chaque classe dans le module, appeler register_component
    f = path+filename
    with open(f) as file:
        node = ast.parse(file.read())
        #list of class in the file
        classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
        for klass in classes:
            extend = ''
            if len(klass.bases) == 1:
                if hasattr(klass.bases[0],'id'):
                    extend = klass.bases[0].id
                else:
                    extend = klass.bases[0].attr
            #if extends BusinessOperation,BusinessProcess,BusinessService
            if  extend in ('BusinessOperation','BusinessProcess','BusinessService'):
                module = filename_to_module(filename)
                register_component(module, klass.name, path, overwrite, f"{iris_package_name}.{module}.{klass.name}")

def register_package(package:str,path:str,overwrite:int,iris_package_name:str):
    """
    It takes a package name, a path to the package, a flag to overwrite existing files, and the name of
    the iris package to register the files to. It then loops through all the files in the package and
    registers them to the iris package
    
    :param package: the name of the package you want to register
    :type package: str
    :param path: the path to the directory containing the package
    :type path: str
    :param overwrite: 0 = don't overwrite, 1 = overwrite
    :type overwrite: int
    :param iris_package_name: The name of the package in the Iris package manager
    :type iris_package_name: str
    """
    for filename in os.listdir(os.path.join(path,package)):
        if filename.endswith(".py"): 
            register_file(os.path.join(package,filename), path, overwrite, iris_package_name)
        else:
            continue

def filename_to_module(filename) -> str:
    """
    It takes a filename and returns the module name
    
    :param filename: The name of the file to be imported
    :return: The module name
    """
    module = ''

    path,file = os.path.split(filename)
    mod = file.split('.')[0]
    packages = path.replace(os.sep, ('.'))
    if len(packages) >1:
        module = packages+'.'+mod
    else:
        module = mod

    return module
