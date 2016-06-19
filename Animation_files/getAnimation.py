import bpy
import os

filename = os.path.join(os.path.basename(bpy.data.filepath), "C:\FAPSA18\JDPR\TUM\Second_Semester\Sofware_Lab\BMW\Animation_files\main.py")
exec(compile(open(filename).read(), filename, 'exec'))