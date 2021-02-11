"""
@Author: Maro Okegbero
@Date: July 19, 2020
"""
import pkgutil
from abc import ABC
import sys
from django.core.management.base import BaseCommand, CommandError
from munch import munchify
from app.management import commands
from app.utils import populate_obj

thismodule = sys.modules[__name__]
print(thismodule)


class Command(BaseCommand, ABC):
    help = "load all static objects into the database"

    def handle(self, *args, **options):
        all_modules = []
        importer = None

        #  get all the module files containing the different categories
        for imp, mod_name, ispkg in pkgutil.iter_modules(commands.__path__):
            importer = imp
            all_modules.append(mod_name)

        # exclude this module if among the files specified as it is an execution file
        if all_modules.count(thismodule.__name__.split('.')[-1]) > 0:
            all_modules.remove(thismodule.__name__.split('.')[-1])

        for name in all_modules:
            print(name, f"{name} has been loaded")
            module = importer.find_module(name).load_module(name)
            print(module, f"this module is included=====")
            if module:
                model = module.obj.get("model")
                model.objects.all().delete()
                data = module.obj.get("data")
                for d in data:
                    b = munchify(d)
                    try:
                        obj = model()
                        obj = populate_obj(obj, d)
                        obj.save()
                        # model.objects.create(name=b.name, description=b.description)
                        print(f'{model} instance created')
                    except Exception as e:
                        print(f"There was an exception for {name}=====>>>>>> {e}")
                        continue
                    self.stdout.write(self.style.SUCCESS('Entities were created successfully'))



