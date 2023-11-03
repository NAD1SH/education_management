from TeacherApp.models import *
import os
from django import template
register = template.Library()


@register.simple_tag
def material_name(study_material):
    file_name = os.path.basename(study_material)
    return file_name