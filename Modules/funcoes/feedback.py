from subprocess import call
from Modules.constants import LINK_FEEDBACK_FORM


__all__ = ['abre_feedback']


def abre_feedback():
    call(f'start {LINK_FEEDBACK_FORM}', shell=True, stdout=False)
    return None
