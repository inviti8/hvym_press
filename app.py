import os
import sys
import io
import json
import time
import pickle
import pathlib
import base64
import requests
import threading
import webbrowser
import MarkdownHandler
import ServerHandler
import SiteDataHandler
import PIL.Image
import ColorPicker
import IconPicker
import io
from PIL import Image, ImageDraw, ImageColor
from jinja2 import Environment, FileSystemLoader
import PySimpleGUI as sg
import W3DeployHandler
import TreeData
import jsoneditor
import subprocess
import HVYM

# hvym_theme = {'BACKGROUND': '#31b09c',
#                 'TEXT': '#fff4c9',
#                 'INPUT': '#712d3d',
#                 'TEXT_INPUT': '#fff4c9',
#                 'SCROLL': '#4ed8a7',
#                 'BUTTON': ('#afe8c5', '#cf5270'),
#                 'PROGRESS': ('#01826B', '#D0D0D0'),
#                 'BORDER': 0,
#                 'SLIDER_DEPTH': 0,
#                 'PROGRESS_DEPTH': 0}

hvym_theme = {'BACKGROUND': '#98314a',
                'TEXT': '#fff4c9',
                'INPUT': '#712d3d',
                'TEXT_INPUT': '#fff4c9',
                'SCROLL': '#01826B',
                'BUTTON': ('#712d3d', '#31b09c'),
                'PROGRESS': ('#01826B', '#D0D0D0'),
                'BORDER': 0,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

sg.theme_add_new('hvym', hvym_theme)
sg.theme("hvym")
SCRIPT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
LOGO = os.path.join(SCRIPT_DIR, 'images', 'logo.png')
NAME_SIZE = 15
font = ('Terminal', 9)
ICON_PICKER = IconPicker.IconPicker()
ai_mods = None
article_metadata = ""

icon_none = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAKUlEQVRIie3NMQEAAAjDMMC/52ECvlRA00nqs3m9AwAAAAAAAAAAgMMWx/EDPUopmS0AAAAASUVORK5CYII='

empty_px = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACXBIWXMAAC4jAAAuIwF4pT92AAAADUlEQVQImWP4//8/AwAI/AL+hc2rNAAAAABJRU5ErkJggg=='

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRQLGoug2C4AAAF4SURBVHja7dkxS8NAGMbxf2MR6uBqEByKICjiKEJ2RyGLgyB+ECcdXf0aQj6A6BYdHIQKOnWSajedikjbuNwkLdb2zXm2zw+6lOOueXqX95IDEREREZGZVLHuMGvn0ffv0jjpT3UA7qI3gS2gNqDJG5CncfIaWgBVo372gHNgaUioPeAma+eHaZy0pnEG3AI7PzQrgGtgH3gfdyzr5VQxuPh54AFYG6F5D7gC7lwgv/UJNIDLNE46IS2BUYOcA3bdZ1wd4AQ4s/jh0T+sXAvAwaBq85cBFJ5DqFnNXotOusARsOJpRvWBZzeuhFAFIrcBWi5jZzlkub0ADYuSWDVaRhfAqsc/rglsuLIYxE3Q917fbLxo1u8BCkABKAAFoAAUgAJQAApAAUy2L/f9LFBYjTlxAGmcdIEnzwE03bgmj7IWjoE6sF7ysiqAFnBq1aHZC4ysndeBbWCxxAA+gHvg0ep8wMvZoJWQzxhFRERERERERERERCR8X7s+UdqAI8YZAAAAAElFTkSuQmCC'

folder_icon_off = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA3XAAAN1wFCKJt4AAACkElEQVRYhe2XT0gUURzHP+/tY92NNtyJlswlKsSDkcYGwkKJ/aGIqEMQBFEhWWfDU8qeVkQCy0snvXfbwLNeLPIQSHgQWiMiFMFghBbd1XbmdRgddilxRse2Q1+Yw/zen99nfu/3fu+N0FpTS8maev8XAETuzOnK927gAhAB7IB9SaAEvAXGtozKbdRMouncdmhwegDcAy4DtsSWYMsnaDqRm84qH+F0CzgenUAPgCIKSO6IOgUhAZW7QggA9LoNBcAWIAPbNR3ACyXq1SMEl9CArUH8Hm9xKARKoE0LNE5U9q6fAApLD1aZ/1QXNoCIhIgNpRDo8t5cC0BgOQBQ72mQBnFQoi0Lyuw+CgInn2y5tgWwAYR3HFjWoCTisMBh34MsjV63j6EdAG9ZJXByBCC0adttPiqJiMhrwEO1Y+cKtfRkAFiammBlZtq1x1NpGjquADA3kt15Isslf+4L4MCRBMn0eRrOtTN5/6ZrTz3tI9aYZGH6nZ/pAOK+atzscJaiaRJrTNLWPwRAW/8QscYkRdNkdtjD11drPXT35NFnQJ2X3lZxFfPzPCeu3iB+qgkZT9B03YnE+0wvq18++QbwXeVXZqbJj+cAaL51G4D8eK4qJ/xoV8fM3EiWcqkIQLlU9JZ4QQK09GRQkSgAKhJ1d8dfAYin0m7oP46+ApyliKfS+w8QNhK09w0Azrp/fT3m5kN73wBhI7G/AK29GaKGQWFxwV33uZEshcUFooZBa6//pfBciMJGgrXvy+THcyxNTVS1zbwcdCth2EiwYS57BhBvLp79AcQ8jwhWha2LV60kJV6O4v1TWAL5GgLkJdBVQ4AuBXwAmoHHwHGCunJuLw18A0aBefH/57TWAL8As2q+p/+gTSYAAAAASUVORK5CYII='

file_icon = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACTUlEQVRYheWXy2sTURSHf+fOI69JrVRFixSE0oWgBUEQly7cFFeCi+6lf0Ch0L8gdCO4jK58kJXQRdtFqWIXLbZQFNSVm4LRRJvSptbWkOTe46JNGWdi585koogfZJFz7z3nu/fMIyFmhpv7j+dQq+32SSWniOgmgF4EIKVCKmlLJ+NM9DjZh4MD5yCVajv32vDQL99Nf7LmScXqLQH9QYVbMBgAIZUwHlw43/fj6qXBp7prhTdQb+zfA3M/iHRzHEkkEwl8LG08WX79/nZkAWa+FbZ4C8MwoJTCuw/rz4rlykgkAbRpiy7MDNu2kM2ksLC8Nlv8UrkRRaAeVaAlkbRtGKaBlytvXmzt7F4PK9AxihlOOgmpGHOLK0vfvu9d+aMCAKAUo8dJoyklzS6uvtrbr13smgADICLYlgnbMmEdfgxD4FTvCUgp7fmltdV6oznkXRv5gnNjCIFmU6JYroDo4DpwI4TA56+bzqPpned374wMxC9ABCklNreqh6fhnyNIYP1T+aw3HovAUQts69h5WTNd9YnFIdAJf10gsAWTY6MAgFy+4Iu54+6Yd+w4tE+gXYE41oRuQVDSXL7w29OKRSBuQgmEaYNO/0MLhEFXNpKA7u50iOVJ6Ma78yBZ7ROIsmudNeR9c+XyhQ0Ap0NX06MyOTZ6xh34t27D/0bA7mI9X+52Ao0uCvhy+wWIZg5+48QLM4OYZgIFLDM5DoiS9/bssDpIUMnOpMe9Q74noWUmtqVqXJZSTQHQ+nseQJWZFwxhThgpa9s7+BMoWNGFUVzMQgAAAABJRU5ErkJggg=='

block = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRQfBrEPUzQAAAICSURBVHja7Zm/attQFMZ/lh0ITjAkwSCakCkZSh6gLRpaOnXVCyRDyNI3SCB065SMXdyhW4ZC0doxix4gmboUupRqSbo4sWliucs1GBMXbrlS9Of7LTIGH119Pt+55x6BEEIIIYQQtaThMliUxB6wCiw6XudV6AeDQgsQJXETeA4cAhsO1+gBn4GT0A+GrgVoOYz1BPgIPM3gj9oGfgKfXAf2HMZazujhMZZ6m0Vgj/KwVHcBMqGVwz3SOcW3UQcBroDBjAgjYMHcewzcmevsulaAdtkFuAV2Qz84n7N1NgBCPxibzxNLfgAOqpAB3pwHbxkLpKEfjCYimOwgSuL7B7KilAKsAGemQ/w+5f8u0AHSKIn7xgbTtM13zbILsDjVFq+Z63imCHbzaNMf0wLpA3aozS5Q+F4jawF+Az3gm2XfsAe8ykO8PLbBr/O2wX+cLJ8BL6uQAU2gGyXxuoXnR+ZgVYkiuAa8B24sfjM284RKCLAAbNW5CA6BC+DaMgN2gM08siBrAa6BY+DcsgZMzgKlFyAFhqEf3FnuApU5C6wCR1ESJ5YWeJFXA5W1AG3gTZGLYJlGYo2iC/DHstrbcll0AX4Bp0A/g3V+Ad4VPq2iJO4A+8BrR8MMz/QRPeDHZHpUaF+ZV2Sew9gpMDIjMyGEEEIIIYQQQgghhBBCiP/mL0X3clOfJl9rAAAAAElFTkSuQmCC'

block_thumb = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRQfG9IJP+0AAAHdSURBVHja7ZmxShxRFIa/nVXQJAgqwmDEyhTiA6hMoSRN2nkCC7HxDQwEu1Ra2iSFvSDTWtrMA2hlaSNO46aJcVFXbW4xDIvOwr2717v/Vw134HDnv+ee859dEEIIIYQQYihp2AyWFXkETAFjlvd5k8bJndcCZEXeBFaAHWDO4h4j4AjYS+OkbVuAEYuxZoE/wKKDg/oCXAGHtgNHFmN9cvTxmCu17SJwxPvh47AL4IQRx/H/Ar+Bi9LaE7ABrPtwAK4F+A+cpHFyWukYy0aANnAGtEqvn4ElYN52mx6EAG+13xbwEzgtrXWAA2ArZAHK16GdxslDJUMeTSYQggDPr6xNAT+yIi8q71b7VR9cCzAOfMuKfLZy6gvm+QPwPeQiOGmscTULmr60YNcCNDyoM975gDqFsW8+YSA+oMZkuQyshZABTWAmK/LPPfT0jhmsGiEIMA38Am57bJtzoQgwWmp5Q1kEu3n9OhkQzCzQzevXqQHBzAJdvX6NLhDMLNDN69e5AsHMAgP3+m/xnn4Sa/guwH2P1b5Xzn0X4BrYB/452OcxsOt9WmVFPgFsAl+NDbZxQGdmoLpM46Tj/b0yf5FFFmM/AZ00TvrSFoUQQgghhBBCCCGEEEIIES4v5E1uaUuX9i0AAAAASUVORK5CYII='

block_inset = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRQgBunReQgAAAJbSURBVHja7Zm9ixNBGIefzeWSePh1cMig4h02ynWihTrYqI12A4qFnTYWFhZa2J0gNiIciL2F+FHI/AMiNlMIgsppeaUwgojCGSHmEgtnYTk4ySaTsLv3PjDsB9l3N7995/29k4AgCIIgCIIgbEmSmMGsd3XgILAr8nOuGqW/F1oA610DuALcAXZEfkYHXDBK/4gtQC1irCPAMrAHeArsBHYPMLZvNozSM0ALOAM8GEcG1CPGmgOaYf8j0APODXDdof9k1UvgNPAauARcLbIAWZ4Bq8DCiHHuhwxYBN4XPQNSTgGHI3z5lBPA/LhcYBwCHCuTDdYncI9uGL3MuVbOAtwqqwDrwC2j9PKG4tbMWHA3fC5reyth3pcyA94AN/NcYJTuZw771rv1qkyBKeCe9W4pHG8L2+lsE2a9S3e/he1slWpAIwiRpnt632STXqJyRXAqI0CjaC5Qoxz8LGsG9IG3wOecznFxUnVg3AL0gBcbbXCAleXJqgiQAAesd0dzTLc/GbcovQA14DpwLed1zSq5wHQYW2MtYJT+YL3bnzm1BvzOGWZ2Qi9nImuBu8DDHDWgE9b+i1WZAmtG6XZOF6jUWmDJencjZ+8wXxUB0v5+bsQMem69e1yKVth69wQ4Hylc2yj9znrXJ/J/GOPIgHZI38uANkon1rth3nzWQT5Z736F/a9FF2AFeAWcBRasdw7YO0Qcl3VVYAb4MkQzNXCrGjP99wGPgOORplfCv5/XbwPOKN0ptABBhEbIrFj1pQt0jNI9BEEQBEEQBEEQBEEQBEEQBEEQRuAv3EGGEdIb/IAAAAAASUVORK5CYII='

block_inset_thumb = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRQgJDyxOOwAAAJcSURBVHja7Zm/axRBFMc/e55JDP46CDJqMCEgSjrRQjOkURvtBiIWdtpYWFjY2CnYiRAI9hbij0LmHxCxmUIQVNRGSCmMjSicJ0RzZ+EcLOtp9i6zyd76PjDccnfzbu7t9837zh0IgiAIgiAIwn9JEjOY9a4OzAC7Iq9z2Sj9udQJsN6NABeBm8COyGt0wIJR+kvsBNQixjoCLAJ7gAfATmB3jrH9b8MoPQ6MAaeAO0UooB4x1gQwGq7fAG3gTI55h/6hqifASeAZcB64VOYEpHkILAPT64xzOyhgFnhVdgV0mQcOR/jyXU4AU0V1gSIScCx13QFeAO9Tz60C54BGGdpgveD4beCxUXoxU9tzqQQ0ge+ZeY3M2saKWmBtkxKfpNRwK5TLTBiTwIdhVsBz4Fof728apVsZhaxWpQS6ZZClEx63ADesd1czr01VJQE1YMF6dzCzCe7N+IeJqm6CSWiL82U9DNUYDr4OqwJ6+YC12FCfsCk+IMfJcq4qCUiAA9a7o32U2w9gW5W6wBXgcp/zRqvkA7aGUUqiJ8Ao/dp6N5l2ej28/lo0NujmFP4hXa+/1McesBLO/rNVKYE/vH6OLlCZs0Avr5/HO1TmLBDD6zeN0o+sd/eGwgpb7+4DZyOFaxmlX1rvOkT+D6MIBbSCfC8A2iidWO8GufPpDvLOevctXH8qewLeAk+B08C09c4B+waI49JdFRgHPg5gpnJb1Zjy3w/cBY5HKq+E3z+vXwecUXql1AkISRgJyoq1v/wEVozSbQRBEARBEARBEARBEARBEARBENbBL9TmjFti3SiJAAAAAElFTkSuQmCC'

expandable = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRQjEDYon5oAAAGLSURBVHja7dg9S8NAAMbxf2OpBfGlUDXgoDi6uIgIWfwKmQRXFxfB1UkHV13Ez5HJzTXgIDg4d1RTlCoopZaauqRQpEpTL+Wqz2/KNcn18uRekoCIiIiIiIjIv5OzsVFBFDqA8+Xn2He9WLdMLB4CQRTmgWVg2nA7K77r1awOIIjCIrADHAKT3xzWHrB9V8C273oPpgPIG6xrFTgBxjO4UZvAcRKwUY7BusoZXXzHVhaVmuwBz8BLV/l+gDoef9hXtT2Aa2At2W4Ar0Arxfmx73qNkV0FkhVgPikWgKVkWPSrmBw/kZTnuvbNAk++6+3Z3APWgYuu8hQQAzWg3mcdnYsv9WjbO2B1ACVgpseydwqcpZhwm8ANsDKMIZAfwn+8+a5XTzmcPoY1B2QdwBhwFEThfopz2sDiXwmg83xQxlIOoyNnewD1AZ7106jaHsAtcJlRCHfA7ii8Di8A58CGoXBzQAU4AELf9ZrWj6sgCgvJ5Gqqd7WApj6HiYiIiIiIiIiIiIiIiIj8widJyEtyI7k9AwAAAABJRU5ErkJggg=='

expandable_thumb = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRQqCYOBjBMAAAGqSURBVHja7dgxS8NAAIbht1VUENFClYCD6CQuQhURsriLQyZBcHJxKbo66eAkODj4OzKIm2vAQaoguHUUUxR1Ei2aulyhSBJRU7nq9yxJeslx9yV3uRRERERERERE/p2cjY3ywyAP5D/8HHmOG+mWicVDwA+DbmACGMy4nVXPce+tDsAPgz5gDdgGBhJOa3yzfafAiue4N1kH0J1hXdPAPtDbhhu1AOyagK0NoNjS+YrnuDMxT0njB/Uv2x7AA/Bo9o9SzrtKKbtNKau1Yw7IMoAzYNbsr8bc/RJwAbgJ10ee4z7/9lsgywAi4LMODAKLCWV9fhgUgX5zPNJSNgzceY5btjmAOeDY7B8knDMO7KXU0ex8IaZtL4DVARSAoeaE5YfBUktZCaiYIVA22yR14ByY6rQh0GrSbN+Ajbg3widrirdOnAPidAE7fhhsfuGaBjD2VwJorg+Ktn4L5P/7p3uWATx9Y63/FTXbA7gETtoUwjWw3gmfw6PAITCfUbg5oApsAYHnuHXrx5UfBj1mcs3q6XoF6vo7TERERERERERERERERETkB94BGANWm40E/joAAAAASUVORK5CYII='

expandable_inset = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRQjLW5A04sAAAG5SURBVHja7di7S8NQGMbhn6FIwUEUL9HFQURwExyELHXqImImpZMggouT/4Krk0vBxam4KYqbKAgFB8FdcBSv1EkotReXTyii9XYaG3yfJeSkfUm+nvMlDYiIiIiIiIj8O20uw3Zu8h7gvRmuhn5Q/YsckYiXgE3fbmDYcexl6AeFOPSAASAHTNpQzdH5nQKZ0A+uXRcg4ThvDUg14YdKWfai62DPcd5cE5drU7Jdz4ADoL/B8d5Pvn/f4NhtLJrgJz0i2WDWVUM/KMb9QWgDWAXmgQkbvrPtE/AAfHSRSaAH6LD9PtueAdvAeugHK61egCLQDWwCGRsuA491RWjk9eK76pZnDlgCCqEfJFu9B7znAhgH2r/4+RJwDoxFsQSiKEAl9IOSXdhXZ1Ilqh7QjAJ0Aid1S2B05yZ/8Y3lVgOG6vZPLDM2BXh+s98OjDjObNkHIc8a3r7DzH3L9OIwAxLW9aeAQWAGGPhh1jWwB4wCVw7+V0RSgGlgFzgGloEtuy3+RAFYALK2BGbjUIBDIA0c2YlnHeWmgXxc3gd41vhcFbcMlPQ6TERERERERERERERERETkF14A2ytguuTfCOkAAAAASUVORK5CYII='

expandable_inset_thumb = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRQqHgBSCdQAAAHVSURBVHja7dg/SBthHMbxb44gBYfWUOrpolAk0NEuwrvo5KAt3iQ4CaXQxamDq0MnoVMXRyfpULhScStVhIMOJQoFB8FRclKwa7E26fJTjmAO1Dcxh89nubz3Xh4uv/dPkgMRERERERGRe6fkMyxOkwAIWk43otA17iJHpMtLwKZvBXjqOfYoCt1pEfaAIWADmLBTTU/39x1YiEJX912Asue8d8BkBwZq0rJf9XoB5u1Yi0L3/IoZ0rxlds8XYAsYBHZyrjnI6fuV03fSiT3AawGi0M3bSK9cMfrjwD7g2ry9EYXuT7e/BbwWIE6TD8DbnEseATNt+h7EafIY6Lf2Ezv+AD4C76PQLfX6EngNLOf0jwKrOf0XH34gc28bwCfL7vkCXG5YcZq8yLTHgZotgSU7tnMG7AHPCrcEMmrAgr3+GYWudM2l9K+Qe4B5COxmClCN0+TwGj+6msBIpr1rmYUpwN+Wdh8w5jnTm6ADeb+BTY+Zm5YZFGEGlIFzYAoYBl4CQzfMqgNfgCpw7OF/RVcKMAt8BraBN8A6ULlh1imwCKzZEpgrQgG+AtPAN7vxNU+500BSlOcBgW18vop7DpzpcZiIiIiIiIiIiIiIiIiIyC38B/WyaOxWSAfbAAAAAElFTkSuQmCC'

form = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhGlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bRSktgnYQ6ZChOlkRFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi7OCk6CIl/i8ptIjx4Lgf7+497t4B/kaFqWbXOKBqlpFOJoRsblXoeUUQYfRjDFGJmfqcKKbgOb7u4ePrXZxneZ/7c4SVvMkAn0A8y3TDIt4gnt60dM77xBFWkhTic+JRgy5I/Mh12eU3zkWH/TwzYmTS88QRYqHYwXIHs5KhEk8RxxRVo3x/1mWF8xZntVJjrXvyF4by2soy12lGkcQiliBCgIwayqjAQpxWjRQTadpPePiHHL9ILplcZTByLKAKFZLjB/+D392ahckJNymUALpfbPtjGOjZBZp12/4+tu3mCRB4Bq60tr/aAGY+Sa+3tdgR0LcNXFy3NXkPuNwBBp90yZAcKUDTXygA72f0TTlg4BYIrrm9tfZx+gBkqKvUDXBwCIwUKXvd4929nb39e6bV3w+TpHK0wvhApQAAAAZiS0dEAM8AUgBwrTtPlwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+gKDRUBOkvjelsAAAIjSURBVHja7Zm/axRBFMc/t5eoiWf8UQ3RxiIYwUoTEJaA5D8YiyBpU2lnqRZqY6WtoCksRBFFVmsbQaZMkVoQG3EatUiIcuESC1+xLHvnijO6u3kfGG5+8e7Nd9/Mm70DRVEURVEURdmTdEIay7xLgGPAgcB+frEm/V5rATLvusB54BpwIqCPCfAcuGtN+iO0AGMBbU0Dq8DpCA9qBvgEPAptOAloqxdp8ciWuhLDcEJzOBjD6FhNFnfHmvTGiPNlN9YXxxLgFfC44tx5YDLzrg+MFwetSTsxlY8lwFfAF/o+lCzOZ95tA+f+V+jFEmABMLn2FnAo196W0J4AjgCHh/mSefdEqkebJMCMlKo8Ba5KfaJwkeoBy02LgD9lucIiv+31NNjqCLhtTXqrTWlwFXgth9vvOCuLHJRFZFPT4HtgrdC3WbK4zcy7jTamwSXgTKFvpyS09wHH5RW6MyT870t1skkCzEmpyjPgeq49VRi/LHeJ1h6Cl6T8czQN1sSPF9akS21Kgy+Bt7n3gJ7UN0rmngRm25YG31iTPqgyMfNuTu4LSZu2wErm3YWS/n4uEvZL/dQoPzLvLjZRgHkpVXkHrAwZm5XP8TYfggtSRhHlLAi57/r8+iUoFmt1F+AzcK/szh8oq9yMIUDov8amZC8vAt1AD2gdeAh8tCYd1FoAEaErjoeyvQMMrEl3URRFURRFURRFURRFURRFURRF+Qt+Aqhcd+FeuKMxAAAAAElFTkSuQmCC'

ignore_file = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACWklEQVRYheWXPW8TQRCG39m9O/suDrKxYyMgCFFQUIBEAYiSgiYikaCi5S9E+D8kESkCEgjS8FEBDYQOuUNCVCjIiI4G2UKO0UVBsbmP3aUKOu6c3IcvIMTb3czOzDM7d3taUkohqMGNOfS+U1U4YoGILgMoI07SByYOiFK51Cw1yg/0cxegHG/kUuPq9d+etfAC11cV6aoPUuOHuZCxtQFA+YAGCafcuK+fOT+0ZmafJAoEwMIGe4uWBWeJi/+CEATdKsJprz+2nz67lhlAKXUlbfEdcc4hpcR2q/Xc+dSeyQSAEWNJKqUUeNECq9Wxsbr6yml/vJQFwM0KsAPBJk1w6Og/etjyO52LaQHGFnkCVJsC91z0VlbeuP1vZ/8oAACQ74LX6lCuT/byrbdiyz61bwBMAEQEmCZgWmAFE6xgAnoBxvEjEEIY9r2779RwcDICGj6IPs/N9gBMpQEgX4IMDVr1ICRpCOdkjMHvfYU+Pf3l6O07x4K+zG98UKKogzwfXrcD5glIFk3LdMLg/fqhsD0XAOYLgAhcLwA6wHdZp1Urm5HYPADG0V8HiB1B7WYTANBfWozYgvagLezbS4l3YFSBPGJSjyAuaX9pcdfdygUgb6UCSDOGJPNPDZBGSWEzASTtLolyOQmDCnceB5t4B7J0nSQml79hCm2cePGyHjT8W5/hfwNg7GO9SO5RAKMvdfkokjsCwCXWBOV+PEApBbJoLRZg0pLzBrxu+PMcR4IzEPRuZZvNh32RVidKzP4xVKd9pS2ARLLr+d7aVEq91kk2TdWww86fjc/a7PX2dcMAAAAASUVORK5CYII='

anon = 'data:image/png;base64,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'

#TOOL-TIPS:
tt_debug_btn = "Renders site, and launches at localhost:8080."

def _subprocess(command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode('utf-8')
        except Exception as e:
            return None

def load_save_data(file_dir):
    result = None
    if os.path.isfile(file_dir) and os.path.basename(file_dir) == 'site.data':
        data = open(file_dir, 'rb')
        result = pickle.load(data)
        
    return result

def fileIsNew(filePath, time_stamp):
    result = False
    t = time.strftime("%b %d %H:%M:%S %Y", time.gmtime(os.path.getmtime(filePath)))

    latest = max((t, time_stamp))
    
    if t == latest and t != time_stamp:
        result = True
    
    return result

def baseFolder(f_path):
    sep = os.path.sep
    arr = f_path.split(sep)
    return(arr[len(arr)-2])

def newFolderData(f, data):
    f_name = os.path.basename(f)
    data.updatePageData(f, {'title':f_name, 'icon':'none', 'use_text':True, 'max_height':800, 'columns':"1", 'footer_height':200})
    data.updateColumnWidths(f, [90])

def newFileData(f_path, f, full_path, data, file_type='.md'):
    f_name = os.path.basename(f)
    f_name.replace('.md', '')
    t = time.strftime("%b %d %H:%M:%S %Y", time.gmtime(os.path.getmtime(full_path)))

    data.updateFile(f_path, f, 'Default', True)
    data.updateArticleData(f_path, f, {'name':f_name, 'column':"1", 'type':"Block", 'style':"default", 'border':"default", 'bg_img_opacity':0.5, 'author':"anonymous", 'use_thumb':False, 'html':"", 'time_stamp':t, 'bg_img':empty_px, 'color':"#FFFFFF", 'rgb':(255, 255, 255), 'use_color':False, 'images':[], 'videos':[], 'nft_start_supply':1024, 'contract':"", 'metadata_link':"",  'metadata':json.dumps(DATA.opensea_metadata), 'file_type': file_type})
    data.updateArticleHTML(f_path, f, full_path)
    data.updateFormData(f_path, f, {'formType':{'name':False, 'email':True, 'address':False, 'phone':False,'eth':False, 'btc':False, 'polygon':False, 'generic':False}, 'customHtml':"", 'btn_txt':"SUBMIT", 'response':"Form Submitted", 'form_id':""})
    data.updateMetaData(f_path, f, {'name':"", 'description':""})

def newMdFile(file, filename, fullpath, data):
    basepath = fullpath.replace(filename, '')
    f_path = baseFolder(basepath)
    data.addMdPath(file, fullpath)
    newFileData(f_path, file, fullpath, data)
    print("newFileData is added@: "" fullpath: " +fullpath+" f: "+ file+" and f_name: "+filename+" is appended")
    data.addAuthor('anonymous', anon)

def moveTreeElement(path, name, move_method):
    if '.md' in name:
        move_method(path, name)
    else:
        move_method(name)

def updateMovedTreeElement(window, data, path, name):
    if '.md' in name:
        folder = data.folderPathList[path]
        article_path = os.path.join(folder, name)
        renderTreedata(data)
        window['-TREE-'].update(treedata)
        tree_select(article_path)
    else:
        page_path = data.folderPathList[name]
        renderTreedata(data)
        window['-TREE-'].update(treedata)
        tree_select(page_path)

    data.saveData()

def moveTreeElementUp(window, data, path, name):
    if '.md' in name:
        moveTreeElement(path, name, data.moveArticleUp)
        updateMovedTreeElement(window, data, path, name)
    else:
        moveTreeElement(path, name, data.movePageUp)
        updateMovedTreeElement(window, data, path, name)

def moveTreeElementDown(window, data, path, name):
    if '.md' in name:
        moveTreeElement(path, name, data.moveArticleDown)
        updateMovedTreeElement(window, data, path, name)
    else:
        moveTreeElement(path, name, data.movePageDown)
        updateMovedTreeElement(window, data, path, name)

def renderTreedata(data):
    #clear the tree
    treedata.delete_tree()

    #render the data
    for page in data.pageList:
        aData = data.articleData[page]
        pagePath = data.folderPathList[page]
        treedata.Insert('', pagePath, page, values=[0], icon=folder_icon )
        if page in data.folderData:
            for article in data.folderData[page]['articleList']:
                d = aData[article]
                articlePath = os.path.join(pagePath, article)
                icon = get_file_icon(d['type'])
                treedata.Insert(pagePath, articlePath, article, values=[0], icon=icon )

def updateFolderData(first_run, data):
    if not first_run:
        return
    
    for page in data.articleData.keys():
        DATA.updateFolderData(page)

def refreshSiteData(data):
    site_data = data.generateSiteData()
    data.refreshDebugMedia()
    data.refreshCss()

    return site_data

def add_files_in_folder(parent, dirname, data):
    files = os.listdir(dirname)
    file_paths = []
    new_folders = []
    first_run = False
    
    if(data.fileExists and not first_run):
        data.pruneFolders()
        for f in files:
            fullpath = os.path.join(dirname, f)
            f_name = os.path.basename(f)
            basepath = fullpath.replace(f_name, '')
            f_path = baseFolder(basepath)

            file_paths.append(fullpath)
            
            if os.path.isdir(fullpath):
                data.pruneFiles()
                if '_resources' not in fullpath:
                    data.addFolderPath(f, fullpath)
                    if data.hasNoFolder(f):
                        newFolderData(f, data)
                    
                    if f_name not in data.pageList and not f_name.startswith("_"):
                        data.pageList.append(f_name)
                        new_folders.append(f_name)

                    add_files_in_folder(fullpath, fullpath, data)
            else:
                file_extension = pathlib.Path(f).suffix           
                if file_extension == '.md':
                    newMdFile(f_path, f, fullpath, data)

        for fd in new_folders:
            fd_path = os.path.join(dirname, fd)
            files = os.listdir(fd_path)
            for f in files:
                fullpath = os.path.join(fd_path, f)
                f_name = os.path.basename(f)
                basepath = fullpath.replace(f_name, '')
                file_extension = pathlib.Path(f).suffix
                                
                if file_extension == '.md':
                    newMdFile(f, f_name, fullpath, data)

            data.updateFolderData(fd)
                        
    else:
        first_run = True
        for f in files:
            fullpath = os.path.join(dirname, f)
            f_name = os.path.basename(f)
            
            if os.path.isdir(fullpath):
                if '_resources' not in fullpath:
                    data.addFolderPath(f, fullpath)
                    newFolderData(f, data)
                    
                    if not f_name.startswith("_"):
                        data.pageList.append(f_name)
                        print("Page: "+f_name+" is appended")

                    add_files_in_folder(fullpath, fullpath, data)
                
            else:
                file_extension = pathlib.Path(f).suffix
                f_icon = block
                f_name = os.path.basename(f)
                basepath = fullpath.replace(f_name, '')
                                
                if file_extension == '.md':
                    newMdFile(f, f_name, fullpath, data)

    if first_run == False:             
        data.deleteOldFiles()

    data.saveData()
    updateFolderData(first_run, data)
    renderTreedata(data)
    
                
def get_file_icon(uiType):
    result = file_icon
    if uiType == 'Block':
        result = block
    elif uiType == 'Block-Thumb':
        result = block_thumb
    elif uiType == 'Block-Inset':
        result = block_inset
    elif uiType == 'Block-Inset-Thumb':
        result = block_inset_thumb
    elif uiType == 'Expandable':
        result = expandable
    elif uiType == 'Expandable-Thumb':
        result = expandable_thumb
    elif uiType == 'Expandable-Inset':
        result = expandable_inset
    elif uiType == 'Expandable-Inset-Thumb':
        result = expandable_inset_thumb
    elif uiType == 'Form':
        result = form
        
    return result

def resize_image(image_path, resize=None): #image_path: "C:User/Image/img.jpg"
    if isinstance(image_path, str):
        img = PIL.Image.open(image_path)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(image_path)))
        except Exception as e:
            data_bytes_io = io.BytesIO(image_path)
            img = PIL.Image.open(data_bytes_io)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()
                
def set_file_icon(event):
    item = tree.Widget.selection()[0]
    key = tree.IdToKey[item]
    f_icon = get_file_icon(event)
        
    tree.update(key=key, icon=f_icon)
        
def tree_key_to_id(key):
    dictionary = {v:k for k, v in tree.IdToKey.items()}
    return dictionary[key] if key in dictionary else None

def tree_select(key):
    id_ = tree_key_to_id(key)
    if id_:
        tree.Widget.see(id_)
        tree.Widget.selection_set(id_)

def tree_expand(key):
    item = tree.Widget.selection()[0]
    tree.item(key, open=True)
   
def double_click(method_arr):
    item = tree.Widget.selection()[0]
    key = tree.IdToKey[item]
    index = treedata.tree_dict[key].values[-1]
    index = (index + 1) % 3
    treedata.tree_dict[key].values[-1] = index
    tree.update(key=key, icon=method_arr[index])

def icon(check):
    png = file_icon
    
    if check == 2:
        png = ignore_file
    return png

def listbox_move(listbox, old_index, new_index):
    limit = listbox.size()
    if not(0<=old_index<limit and 0<=new_index<limit):
        return False
    try:
        item = listbox.get(old_index)        # Get item by index
        listbox.delete(old_index)            # Remove item by index
        listbox.insert(new_index, item)      # insert item by index
        return True
    except:
        return False

def concat_array(arr):
    result = ""
    idx = 0
    for string in arr:
        if string != "":
            if idx == 0:
                result += string
            else:
                result += '-' + string
        idx += 1
        
    return result

def name(name):
    dots = NAME_SIZE-len(name)-2
    return sg.Text(' ' + name + ' ' + ' '*dots, size=(NAME_SIZE,1), justification='l',pad=(0,0),  font=font)

#Window control
def block_focus(window):
    for key in window.key_dict:    # Remove dash box of all Buttons
        element = window[key]
        if isinstance(element, sg.Button):
            element.block_focus()
            
            
def popup_set_column_widths(md_name, data, colData):
    
    columns = int(data['columns'])

    layout = [[sg.Spin([x+1 for x in range(1050)], initial_value=colData[num], key='COL-WIDTH-'+str(num)) for num in range(0, columns)]]
    
    col_layout_btns = [[sg.Button("Save", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DATA-'), sg.Button('Cancel', font=font)]]
    layout = [
        [sg.Text("Set Column Width Percentages")],
        [sg.Column(layout, expand_x=True, element_justification='center')],
        [sg.Column(col_layout_btns, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Column Widths", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    width_arr = []
    
    if event == '-SAVE-DATA-':
        for num in range(0, columns):
            width_arr.append(values['COL-WIDTH-'+str(num)])
            
    return width_arr if event == '-SAVE-DATA-' else None 


def do_open_set_page_data(f_name):
    re_open = False
    data = DATA.pageData[f_name]
    colData = DATA.columnWidths[f_name]
    d = popup_set_page_data(f_name, data)
        
    if(d != None):
        if 're_open' in d.keys():
            re_open = True
            del d['re_open']
            
        columns = int(d['columns'])
        if len(colData) < columns:
            arr = []
            val = round(100/columns, 2)
            for num in range(0, columns):
                arr.append(val)
            DATA.updateColumnWidths(f_name, arr)
                
        DATA.updatePageData(f_name, d)
        DATA.saveData()
        
        if re_open:
            do_open_set_page_data(f_name)
            

def popup_set_page_data(md_name, data):
    icon = ICON_PICKER.icon_map[data['icon']]
    
    columns = ['1', '2', '3', '4']
    
    col_layout_l = [[sg.Text("Title:", font=font)],
                  [sg.Text("Use Text:", font=font)],
                  [sg.Text("Icon:", font=font)],
                  [sg.Text("Max Height:", font=font)],
                  [sg.Text("Columns:", font=font)],
                  [sg.Text("Footer Height:", font=font)]]
    
    col_layout_r = [[sg.Input(data['title'], s=(27,22), k='TITLE', font=font)],
                  [sg.Checkbox('yes', default=data['use_text'], k='USE-TEXT', font=font)],
                  [sg.Input(key='ICON', default_text=data['icon'], visible=False), sg.Button('', image_data=icon, k='-SET-ICON-', font=font)],
                  [sg.Spin([x+1 for x in range(1050)], initial_value=data['max_height'], s=(25,22), key='MAX-HEIGHT', font=font)],
                  [sg.Combo(columns, default_value=data['columns'], s=(25,22), readonly=True, k='COLUMNS', font=font)],
                  [sg.Spin([x+1 for x in range(10)], initial_value=data['footer_height'], s=(25,22), key='FOOTER-HEIGHT', font=font)]]
    
    col_layout = [[sg.Column(col_layout_l, expand_x=True, element_justification='left'), sg.Column(col_layout_r, expand_x=True, element_justification='right')]]
    
    col_layout_btns = [[sg.Button("Save", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DATA-'), sg.Button('Cancel', font=font)]]
    layout = [
        [sg.Text(f"File: {md_name}", font=font)],
        [sg.Column(col_layout, expand_x=True, element_justification='left')],
        [sg.Column(col_layout_btns, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Set Page Data", layout, use_default_focus=False, finalize=True, modal=True, font=font)
    block_focus(window)
    event, values = window.read()
    window.close()
    page_data = None

    if event == '-SAVE-DATA-':
        page_data = {'title':values['TITLE'], 'icon':data['icon'], 'use_text':values['USE-TEXT'], 'max_height':values['MAX-HEIGHT'], 'columns':values['COLUMNS'], 'footer_height':values['FOOTER-HEIGHT']}
        
    elif event == '-SET-ICON-':
        icon_chosen = ICON_PICKER.popup_icon_chooser()
        page_data = None
        
        if icon_chosen != 'none':
            page_data = {'re_open':True, 'title':values['TITLE'], 'icon':icon_chosen, 'use_text':values['USE-TEXT'], 'max_height':values['MAX-HEIGHT'], 'columns':values['COLUMNS'], 'footer_height':values['FOOTER-HEIGHT']}
            
    return page_data if event == '-SAVE-DATA-' or event == '-SET-ICON-' else None


def popup_nft_settings():
    
    col_layout_1 = [[sg.Text("Chain:", font=font)],
                    [sg.Text("Type:", font=font)],
                    [sg.Text("Start Supply:", font=font)],
                  [sg.Text("Metadata:", font=font)]]
    
    col_layout_2 = [[sg.Combo(DATA.nftTypes, default_value=DATA.settings['nft_type'], s=(25,22), readonly=True, k='SETTING-nft_type', font=font)],
                    [sg.Combo(DATA.nftSiteTypes, default_value=DATA.settings['nft_site_type'], s=(25,22), readonly=True, k='SETTING-nft_site_type', font=font)],
                    [sg.Spin([x+1 for x in range(100000)], initial_value=DATA.settings['nft_start_supply'], s=(25,22), k='SETTING-nft_start_supply')],
                  [sg.Input(default_text="", s=20, k='SETTING-metadata', font=font), sg.FileBrowse(file_types=(("JSON", "*.json"),)), sg.Button('Edit', enable_events=True, k='-SET-SITE-METADATA-')],]
    
    col_layout_btns = [[sg.Button("Save", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DATA-'), sg.Button('Cancel', font=font)]]
    
    layout = [
        [sg.Column(col_layout_1, expand_x=True, element_justification='center'), sg.Column(col_layout_2, expand_x=True, element_justification='center')],
        [col_layout_btns]
    ]
    
    def update_site_data(d):
        DATA.updateSetting('site_metadata', d)
        if '.json' in values['SETTING-metadata'] and os.path.isfile(values['SETTING-metadata']):
            with io.open(values['SETTING-metadata'], mode="r", encoding="utf-8") as f:
                with open(values['METADATA-LINK'], 'w', encoding='utf-8') as f:
                    json.dump(d, f, ensure_ascii=False, indent=4)
            
    window = sg.Window("NFT Settings", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    
    if event == '-SAVE-DATA-':
        DATA.updateSetting('nft_site_type', values['SETTING-nft_site_type'])
        DATA.updateSetting('nft_type', values['SETTING-nft_type'])
        DATA.updateSetting('metadata', values['SETTING-metadata'])
        DATA.saveData()
        DATA.deployHandler.updateSettings(DATA.settings)
    if event == '-SET-SITE-METADATA-':
        jsoneditor.editjson(DATA.settings['site_metadata'], update_site_data, None, None, False, True)
        popup_nft_settings()
        

def do_open_set_article_data(f_path, f_name, window):
    re_open = False
    data = DATA.getData(f_path, f_name, DATA.articleData)
    colData = DATA.columnWidths[f_path]
    d = popup_set_article_data(f_path, f_name, data, colData, window)
    
    if(d != None):
        if 're_open' in d.keys():
            re_open = True
            del d['re_open']
            
        DATA.updateArticleData(f_path, f_name, d)
        DATA.updateFile(f_path, f_name, d['type'], True)
        DATA.saveData()
        
        if re_open:
            do_open_set_article_data(f_path, f_name, window)          
            
            
def popup_set_article_data(md_path, md_name, data, colData, window):
    columns = []
    article_types = ['Block', 'Expandable', 'Form']
    article_type = data['type'].split('-')[0]
    border_types = ['noborder', 'inset']
    bg_img = data['bg_img'].replace('data:image/png;base64,', '').encode()
    buffer = io.BytesIO()
    imgdata = base64.b64decode(bg_img)
    image = Image.open(io.BytesIO(imgdata))
    new_img = image.resize((50, 50))
    new_img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue())
    img_vis = False
    nft_data_vis = False

    
    if DATA.settings['nft_type'] != 'None' and DATA.settings['nft_site_type'] == 'Collection-Minter':
        nft_data_vis = True
    
    if data['bg_img'] != empty_px:
        img_vis = True
    
    for n in range(0, len(colData)):
        columns.append(str(n+1))
        
    col_layout_img = [[sg.Text("Background Image:", visible=img_vis, font=font)],
                    [sg.Text("", font=font)],
                    [sg.Text("BG Image Opacity:", font=font, visible=img_vis)]]
    col_layout_imgr = [[sg.Image(img_b64, visible=img_vis, size=(50,50))],
                     [sg.Button("Delete Image", visible=img_vis, font=font)],
                     [sg.Slider(range=(0, 1), resolution=.01,  default_value=data['bg_img_opacity'], orientation='horizontal', s=(10,10), k='IMG-OPACITY', font=font, visible=img_vis)],
                     ]
    
    col_layout_color = [[sg.Text("Color:", font=font)],
                    [sg.Text("Use Color:", font=font)]]
    col_layout_colorr = [[sg.Input(key='COLOR', default_text=data['color'], visible=False, font=font), sg.Button('Color Picker', button_color=data['color'], font=font)],
                     [sg.Checkbox('yes', default=data['use_color'], k='USE-COLOR', font=font)],]
    
    col_layout_l = [[sg.Text("Name:", font=font)],
                  [sg.Text("Column:", font=font)],
                  [sg.Text("Article Type:", font=font)],
                  [sg.Text("Border Type:", font=font)],
                  [sg.Text("Author:", font=font)],
                  [sg.Text("Background Image:", font=font)],
                  [sg.Text("Use Author Name & Thumbnail:", font=font)]
                  ]
    
    col_layout_r = [[sg.Input(data['name'], s=(27,10), k='NAME', font=font)],
                  [sg.Combo(columns, default_value=data['column'], s=(25,22), readonly=True, k='COLUMN', font=font)],
                  [sg.Combo(article_types, default_value=article_type, s=(25,22), readonly=True, k='TYPE', font=font)],
                  [sg.Combo(border_types, default_value=data['border'], s=(25,22), readonly=True, k='BORDER-TYPE', font=font)],
                  [sg.Combo(list(DATA.authors.keys()), default_value=data['author'], s=(25,22), readonly=True, k='AUTHOR', font=font)],
                  [sg.Input(default_text="", s=20, k='BG-IMG', font=font), sg.FileBrowse(file_types=(("PNG", "*.png"),), font=font)],
                  [sg.Checkbox('yes', default=data['use_thumb'], s=(25,22), k='USE-THUMB', font=font)],
                  ]
    
    col_nft_layout = [
                  [sg.Text("Start Supply:", font=font), sg.Spin([x+1 for x in range(100000)], initial_value=data['nft_start_supply'], s=(5,5), key='NFT-START-SUPPLY', font=font),
                   sg.Text("Metadata:", font=font), sg.Input(default_text=data['metadata_link'], s=20, k='METADATA-LINK', font=font), sg.FileBrowse(file_types=(('JSON', '*.json'),), font=font), sg.Button('Edit', enable_events=True, k='-SET-METADATA-', font=font)]
                  ]
    
    col_layout0 = [[sg.Column(col_layout_img, expand_x=True, element_justification='left'), sg.Column(col_layout_imgr, expand_x=True, element_justification='right')]]
    col_layout1 = [[sg.Column(col_layout_color, expand_x=True, element_justification='left'), sg.Column(col_layout_colorr, expand_x=True, element_justification='right')]]
    col_layout2 = [[sg.Column(col_layout_l, expand_x=True, element_justification='left'), sg.Column(col_layout_r, expand_x=True, element_justification='right')]]
    col_layout3 = [[sg.Frame('NFT', col_nft_layout, expand_x=True, visible=nft_data_vis, font=font)]]

    col_layout_btns = [[sg.Button("Save", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DATA-'), sg.Button('Cancel', font=font), sg.Button("Save As Default", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DEFAULT-')]]
    layout = [
        [sg.Text(f"File: {md_name}")],
        [sg.Column(col_layout0, expand_x=True, element_justification='left')],
        [sg.Column(col_layout1, expand_x=True, element_justification='left')],
        [sg.Column(col_layout2, expand_x=True, element_justification='left')],
        [sg.Column(col_layout3, expand_x=True, element_justification='left')],
        [sg.Column(col_layout_btns, expand_x=True, element_justification='right')],
    ]
    
    def update_metadata(d):
        colData = DATA.columnWidths[md_path]
        page_data = {'name':values['NAME'], 'column':values['COLUMN'], 'type':type_string, 'border':values['BORDER-TYPE'], 'bg_img_opacity':values['IMG-OPACITY'], 'author':values['AUTHOR'], 'use_thumb':values['USE-THUMB'], 'html': data['html'], 'bg_img':img, 'time_stamp': data['time_stamp'], 'color':values['COLOR'], 'rgb':rgb, 'use_color':values['USE-COLOR'], 'nft_start_supply':values['NFT-START-SUPPLY'], 'contract':"", 'metadata_link':values['METADATA-LINK'], 'metadata':json.dumps(d)}
        DATA.updateArticleData(f_path, f_name, page_data)
        DATA.updateFile(md_path, md_name, page_data['type'], True)
        DATA.saveData()
        if '.json' in values['METADATA-LINK'] and os.path.isfile(values['METADATA-LINK']):
            with open(values['METADATA-LINK'], 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=4)
        return page_data

    popup = sg.Window("Set Article Data", layout, use_default_focus=False, finalize=True, modal=True, font=font)
    block_focus(popup)
    event, values = popup.read()
    popup.close()
    page_data = None
    type_concat = ""
    thumb_concat = ""
    inset_concat = ""
    img = empty_px
    
    
    if data['bg_img'] != empty_px:
        img = data['bg_img']

    if values != None:
        if 'Form' not in values['TYPE']:
            if values['TYPE'] != None:
                type_concat = values['TYPE']
            if values['BORDER-TYPE'] != None and values['BORDER-TYPE'] == 'inset':
                inset_concat = "Inset"
            if values['USE-THUMB'] != None and  values['USE-THUMB'] == True:
                thumb_concat = "Thumb"
        else:
            if values['TYPE'] != None:
                type_concat = values['TYPE']
                
        if os.path.isfile(values['BG-IMG']):
            with open(values['BG-IMG'], "rb") as img_file:
                img = base64.b64encode(img_file.read()).decode('utf-8')
                img = 'data:image/png;base64,'+img
            
        type_arr = [type_concat, inset_concat, thumb_concat]
        type_string = concat_array(type_arr)
        set_file_icon(type_string)
        rgb = ImageColor.getcolor(values['COLOR'], 'RGB')
        
        if event == '-SAVE-DATA-':
            page_data = {'name':values['NAME'], 'column':values['COLUMN'], 'type':type_string, 'border':values['BORDER-TYPE'], 'bg_img_opacity':values['IMG-OPACITY'], 'author':values['AUTHOR'], 'use_thumb':values['USE-THUMB'], 'html': data['html'], 'bg_img':img, 'time_stamp': data['time_stamp'], 'color':values['COLOR'], 'rgb':rgb, 'use_color':values['USE-COLOR'], 'nft_start_supply':values['NFT-START-SUPPLY'], 'contract':"", 'metadata_link':values['METADATA-LINK'], 'metadata':data['metadata'] }
        elif event == '-SET-METADATA-':
            if '.json' in values['METADATA-LINK'] and os.path.isfile(values['METADATA-LINK']):
                with io.open(values['METADATA-LINK'], mode="r", encoding="utf-8") as f:
                    jsoneditor.editjson(json.load(f), update_metadata, None, None, False, True)
            else:
                jsoneditor.editjson(json.loads(data['metadata']), update_metadata, None, None, False, True)
        elif event == 'Delete Image':
            delete_img = sg.PopupOKCancel("Delete Image?")
            page_data = None
            if delete_img == 'OK':
                page_data = {'re_open':True, 'name':values['NAME'], 'column':values['COLUMN'], 'type':type_string, 'border':values['BORDER-TYPE'], 'bg_img_opacity':values['IMG-OPACITY'], 'author':values['AUTHOR'], 'use_thumb':values['USE-THUMB'], 'html': data['html'], 'time_stamp': data['time_stamp'], 'bg_img':empty_px, 'color':values['COLOR'], 'rgb':rgb, 'use_color':values['USE-COLOR'], 'nft_start_supply':values['NFT-START-SUPPLY'], 'contract':"", 'metadata_link':values['METADATA-LINK'], 'metadata':data['metadata']}
        elif event == 'Color Picker':
            color_chosen = ColorPicker.popup_color_chooser()
            page_data = None
            if color_chosen != None:
                rgb = ImageColor.getcolor(color_chosen, 'RGB')
                page_data = {'re_open':True, 'name':values['NAME'], 'column':values['COLUMN'], 'type':type_string, 'border':values['BORDER-TYPE'], 'bg_img_opacity':values['IMG-OPACITY'], 'author':values['AUTHOR'], 'use_thumb':values['USE-THUMB'], 'html': data['html'], 'time_stamp': data['time_stamp'], 'bg_img':img, 'color':color_chosen, 'rgb':rgb, 'use_color':values['USE-COLOR'], 'nft_start_supply':values['NFT-START-SUPPLY'], 'contract':"", 'metadata_link':values['METADATA-LINK'], 'metadata':data['metadata']}
                
        return page_data if event == '-SAVE-DATA-' or event == 'Delete Image' or event == 'Color Picker' else None
            
def popup_set_meta_data(md_name, data):
    
    col_layout = [[sg.Text("Page Name:", font=font), sg.Input(s=(30,8), default_text=data['name'], k='META-NAME')],
                  [sg.Text("Page Description:", font=font)],[sg.Multiline(s=(30,8), default_text=data['description'], k='META-DESCRIPTION')]]
    
    col_layout_btns = [[sg.Button("Save", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DATA-'), sg.Button('Cancel', font=font)]]
    
    layout = [
        [sg.Text(f"File: {md_name}")],
        [sg.Column(col_layout, expand_x=True, element_justification='center')],
        [sg.Column(col_layout_btns, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Set Description", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    page_data = None
    if event == '-SAVE-DATA-':
        page_data = {'name':values['META-NAME'], 'description':values['META-DESCRIPTION']}
    return page_data if event == '-SAVE-DATA-' else None

def popup_set_form_data(md_name, data):
    
    form_data = data['formType']
    
    elements_layout = [[sg.Frame('Fields', [[sg.Checkbox('Name', default=form_data['name'], k='-NAME-'), sg.Checkbox('Email', default=form_data['email'], k='-EMAIL-'),
                                                    sg.Checkbox('Address', default=form_data['address'], k='-ADDRESS-'), sg.Checkbox('Phone', default=form_data['phone'], k='-PHONE-')],
                                            [sg.Checkbox('Ethereum', default=form_data['eth'], k='-ETH-'), sg.Checkbox('Bitcoin', default=form_data['btc'], k='-BTC-'),
                                             sg.Checkbox('Polygon', default=form_data['polygon'], k='-POLYGON-'), sg.Checkbox('Generic', default=form_data['generic'], k='-GENERIC-')]], expand_y=True, expand_x=True)]]
    
    col_layout_html = [[sg.Text("Custom HTML:", font=font)],[sg.Multiline(s=(30,8), expand_x=True, default_text=data['customHtml'], k='CUSTOM-HTML')]]
    
    col_layout_data_l = [[sg.Text("Submit Button Text:", font=font)],
                         [sg.Text("Form Response Text:", font=font)],
                         [sg.Text("Form Deploy ID:", font=font)]]
    col_layout_data_r = [[sg.Input(key='BTN-TXT', default_text=data['btn_txt'])],
                         [sg.Multiline(s=(20,5), expand_x=True, default_text=data['response'], k='RESPONSE')],
                         [sg.Input(key='FORM-ID', default_text=data['form_id'])]]

    
    col_layout_data = [[sg.Column(col_layout_data_l, expand_x=True, element_justification='left'), sg.Column(col_layout_data_r, expand_x=True, element_justification='right')]]
    
    
    col_layout_btns = [[sg.Button("Save", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DATA-'), sg.Button('Cancel', font=font)]]
    layout = [
        [sg.Text(f"File: {md_name}")],
        [elements_layout],
        [sg.Column(col_layout_html, expand_x=True, element_justification='center')],
        [sg.Column(col_layout_data, expand_x=True, element_justification='center')],
        [sg.Column(col_layout_btns, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Set Form Data", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    
    if values != None:
        page_data = None
        form_type = {'name':values['-NAME-'], 'email':values['-EMAIL-'], 'address':values['-ADDRESS-'], 'phone':values['-PHONE-'],'eth':values['-ETH-'], 'btc':values['-BTC-'], 'polygon':values['-POLYGON-'], 'generic':values['-GENERIC-']}
        if event == '-SAVE-DATA-':
            page_data = {'formType':form_type, 'customHtml':values['CUSTOM-HTML'], 'btn_txt':values['BTN-TXT'], 'response':values['RESPONSE'], 'form_id':values['FORM-ID']}
        return page_data if event == '-SAVE-DATA-' else None
    
def popup_set_page_order(list_values):
    
    col_layout = [
        [sg.Listbox(list_values, size=(10, 5), key="-ITEM-")],
        [sg.Text('Initial list '+repr(list_values), size=(50, 1), key='-LIST-')],
        [sg.Button("Move item 12 to top")],
    ]
    
    col_layout_btns = [[sg.Button("Save", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DATA-'), sg.Button('Cancel', font=font)]]
    
    layout = [
        [sg.Column(col_layout, expand_x=True, element_justification='center')],
        [sg.Column(col_layout_btns, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Add Author", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    
    if values != None and os.path.isfile(values['AUTHOR-IMG']):
        author_data = None
        img = None
        with open(values['AUTHOR-IMG'], "rb") as img_file:
            img = base64.b64encode(img_file.read())
        if event == '-SAVE-DATA-':
            author_data = {'name':values['AUTHOR-NAME'], 'image':img}
        return author_data if event == '-SAVE-DATA-' else None
    
def popup_author():
    
    col_layout = [[sg.Text("Author:", font=font), sg.Input(s=(30,8), k='AUTHOR-NAME')],
                  [sg.Text("Image:", font=font), sg.Input(default_text="", s=20, k='AUTHOR-IMG'), sg.FileBrowse(file_types=(("PNG", "*.png"),))]]
    
    col_layout_btns = [[sg.Button("Save", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DATA-'), sg.Button('Cancel', font=font)]]
    
    layout = [
        [sg.Column(col_layout, expand_x=True, element_justification='center')],
        [sg.Column(col_layout_btns, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Add Author", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    
    if values != None and os.path.isfile(values['AUTHOR-IMG']):
        author_data = None
        img = None
        with open(values['AUTHOR-IMG'], "rb") as img_file:
            buffer = io.BytesIO()
            image = Image.open(values['AUTHOR-IMG'])
            new_img = image.resize((64, 64))  # x, y
            new_img.save(buffer, format="PNG")
            buffer.seek(0)
            img = base64.b64encode(buffer.read()).decode('utf-8')
        if event == '-SAVE-DATA-':
            author_data = {'name':values['AUTHOR-NAME'], 'image':'data:image/png;base64,'+img}
        return author_data if event == '-SAVE-DATA-' else None
    
def popup_uploader():
    
    col_layout = [[sg.Text('Testing progress bar:')],
              [sg.ProgressBar(max_value=10, orientation='h', size=(20, 20), key='progress_1')]]
    
    col_layout_btns = [[sg.Button("Save", font=font, bind_return_key=True, enable_events=True, k='-SAVE-DATA-'), sg.Button('Cancel', font=font)]]
    
    layout = [
        [sg.Column(col_layout, expand_x=True, element_justification='center')]
    ]
    window = sg.Window("Deploying Files", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    

def popup_server_status(start=True):
    layout = [[sg.Text('Server:')],
               [sg.ProgressBar(max_value=10, orientation='h', size=(20, 20), key='progress_1')]]

    ring_gray_segments = b'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'

    layout = [[sg.Image(data=ring_gray_segments, enable_events=True, background_color='white', key='-IMAGE-', right_click_menu=['UNUSED', ['Exit']], pad=0)],]

    window = sg.Window('ServerHandler', layout,
            no_titlebar=True,
            grab_anywhere=False,
            keep_on_top=True,
            #background_color='white',
            transparent_color='white' if sg.running_windows() else None,
            alpha_channel=.8,
            margins=(0,0))
    
    while True:                                     # Event Loop
        event, values = window.read(timeout=10)    # loop every 10 ms to show that the 100 ms value below is used for animation
        if event == 'Exit':
                  break
        if event in (sg.WIN_CLOSED, 'Exit', 'Cancel'):
            break
        # update the animation in the window
        window['-IMAGE-'].update_animation(gif,  time_between_frames=100)
    window.close()
    
def popup_md_link():
    popup_layout = [
        [sg.Text("URL:", size=(15,1)), sg.InputText(key='url')],
        [sg.Text("Display Text:", size=(15,1)), sg.InputText(key='display')],
        [sg.Button("Submit"), sg.Button("Cancel")]
    ]
    popup_window = sg.Window("Media Link", popup_layout)
    event, values = popup_window.read()
    popup_window.close()
    if event == "Submit":
        return values['url'], values['display']
    else:
        return None, None    
    
def create_image_grid_popup(image_array, num_cols):
    """
    Create a popup with a grid of images displayed as buttons.
    :param image_array: List of base64 encoded PNGs
    :param num_cols: Number of columns in the grid
    :return: None
    """
    buttons = []
    imgs = {}
    for i, image in enumerate(image_array):
        imgdata = base64.b64decode(image)
        image = Image.open(io.BytesIO(imgdata))
        new_img = image.resize((100, 100))
        buffer = io.BytesIO()
        new_img.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode()
        buttons.append(sg.Button('', image_data=img_b64, size=(100, 100), key=f'Image_{i}', enable_events=True))
        imgs[f'Image_{i}'] = image_array[i]
    layout = [buttons[i:i+num_cols] for i in range(0, len(buttons), num_cols)]
    layout.append([sg.Button("Refresh", expand_x=True, key="Refresh")])

    # Create the window and show it
    popup_window = sg.Window('Image Grid', layout, default_button_element_size=(12, 1), auto_size_buttons=False)
    event, values = popup_window.read()
    popup_window.close()
    if event == None:
        return None, None
    elif event == "Refresh":
        return None, None
    elif 'Image_' in event:
        idx = event.split('_')[1]
        img = imgs[event]
        return imgs[event], int(idx)
    else:
        return None, None
                
def DoDeploy(data, window, private=False):
    window.disappear()
    media = data.gatherMedia()
    tup = data.deployMedia(False, True, private)
    if tup == None:
        window.reappear()
        return
    
    media_cid = tup[0]
    if media_cid != None:
        sg.popup_no_buttons("Media Deployed, Deploying Site", auto_close=True, auto_close_duration=1.5, non_blocking=False)
        data.updateAllArticleHTML(data.filePath)
        data.refereshDist()
        data.refreshCss()
        data.saveData()
        
    site_data = DATA.generateSiteData()
    data.refreshDebugMedia()
    data.renderStaticPage('template_index.txt', site_data)
    data.refereshDist()
        
    tup = data.deploySite(False, False, private)
    site_cid = tup[0]
    url = tup[1]
    
    if url != None:
        webbrowser.open_new_tab(url)
    
    data.deleteDist()
    window.reappear()
    

def StartServer(path=SCRIPT_DIR, port=8000):
    '''
    Starts a Simple HTTP Server on port 8000.

    '''
    ServerHandler.Server(ServerHandler.ServerHandler)

    #server_path = os.path.join(SCRIPT_DIR, 'serve', 'heavymeta_simple_server.py')
    #subprocess.Popen([str(sys.executable), server_path])
    
def StopServer():
    '''
    Stops the running server.

    '''
    requests.post('http://localhost:8000/shutdown/', data={})
    
def LaunchStaticSite(route):
    url = os.path.join('http://localhost:8000', route)
    webbrowser.open_new_tab(url)
           

check = [icon(0), icon(1), icon(2)]

starting_path = sg.popup_get_folder('Site Directory', font=font, icon=LOGO)

if not starting_path:
    sys.exit(0)
    
DATA = SiteDataHandler.SiteDataHandler(starting_path, MarkdownHandler, W3DeployHandler, HVYM)
SERVER_STATUS = ServerHandler.ServerStatusHandler()

command = ['---', 'Move Up', 'Move Down', '---','Set-Column-Widths', '---','Set-Meta-Data', 'Set-Form-Data', '---', 'Close Menu']
author_dropdown = ['Add-Author', 'Update-Author', 'Delete-Author']
css_input_dropdown = ['Reset-Css']
treedata = TreeData.TreeData()
add_files_in_folder('', starting_path, DATA)


ui_settings_layout = [[sg.Frame('UI Settings', [
                                                [name('Navigation'), sg.Combo(DATA.navigation, default_value=DATA.settings['pageType'], s=(15,22), enable_events=True, readonly=True, k='SETTING-pageType', font=font)],
                                                [name('Style'), sg.Combo(DATA.styles, default_value=DATA.settings['style'], s=(15,22), enable_events=True, readonly=True, k='SETTING-style', font=font)],
                                                [name('Row Padding'), sg.Spin(values=[i for i in range(1, 100)], initial_value=DATA.settings['row_pad'], enable_events=True, s=(25,22), k='SETTING-row_pad', font=font)],
               [name('Theme'), sg.Combo(DATA.themes, default_value=DATA.settings['theme'], s=(15,22), enable_events=True, readonly=True, k='SETTING-theme', font=font)],
               [name('Custom CSS'), sg.Input(default_text=DATA.settings['customTheme'], s=20, right_click_menu=['&Right', css_input_dropdown], enable_events=True, k='SETTING-customTheme', font=font), sg.FolderBrowse(font=font)]
               ], relief='sunken', expand_y=True, expand_x=True, font=font)]]

site_settings_layout = [[sg.Frame('Site Settings', [[name('Site Name'), sg.Input(default_text=DATA.settings['siteName'], s=20, enable_events=True, k='SETTING-siteName', font=font)],
               [name('Media Folder'), sg.Input(default_text=DATA.settings['mediaDir'], s=20, enable_events=True, k='SETTING-mediaDir', font=font)],
               [name('Description'), sg.Multiline(default_text=DATA.settings['description'],s=(20,8), enable_events=True, k='SETTING-description', font=font)],
               [name('Site ID'), sg.Input(default_text=DATA.settings['siteID'], s=20, enable_events=True, k='SETTING-siteID', font=font)],
               ], relief='sunken', expand_y=True, expand_x=True, font=font)]]

author_settings_layout = [[sg.Frame('Author Settings', [
    [sg.Frame('Authors', [
        [sg.Listbox(DATA.authors.keys(), right_click_menu=['&Right', author_dropdown], no_scrollbar=True, expand_x=True, size=(15,8), k='AUTHOR-LIST', font=font)]
        ], border_width=0, expand_x=True, font=font)],
    ],  size=(15,10), relief='sunken', expand_y=True, expand_x=True, font=font)]]

deployment_settings_layout = [[sg.Frame('Deployment Settings', [
    [name('Project Name:'), sg.Input(default_text=DATA.settings['project_name'], s=20, enable_events=True, expand_x=True, k='SETTING-project_name', font=font)],
    [name('Deployment:'), sg.Combo(['local', 'Internet Computer'], default_value=DATA.settings['deploy_type'], s=(22,22), enable_events=True, readonly=True, k='SETTING-deploy_type', font=font)],                               
               [sg.Frame('Pintheon', [[name('JWT'), sg.Input(default_text=DATA.settings['backend_auth_key'], s=20, enable_events=True, expand_x=True, k='SETTING-backend_auth_key', font=font)],
                                    [name('Gateway URL'), sg.Input(default_text=DATA.settings['backend_end_point'], s=20, enable_events=True, expand_x=True, k='SETTING-backend_end_point', font=font)],
                                    [name('Meta-Data'), sg.Multiline(default_text=DATA.settings['backend_meta_data'], s=(10,4), enable_events=True, expand_x=True, k='SETTING-backend_meta_data', font=font)]
               ], border_width=0, expand_x=True, k='PINTHEON-GRP', font=font, visible=(DATA.settings['deploy_type']=='Pintheon'))],
               [sg.Frame('Internet Computer', [[name('Canister ID'), sg.Input(default_text=DATA.settings['canister_id'], s=20, enable_events=True, expand_x=True, k='SETTING-canister_id', font=font)],
               ], border_width=0, expand_x=True, k='ICP-GRP', font=font, visible=(DATA.settings['deploy_type']=='Internet Computer'))],
               ], relief='sunken', expand_y=True, expand_x=True, font=font)]]

nft_settings_layout = [[sg.Frame('NFT Settings', [
    [sg.Frame('NFT Type:', [
        [sg.Combo(['None', 'NFT', 'Minter'], default_value='None', s=(15,22), enable_events=True, readonly=True, k='SETTING-nft-type')]
        ], expand_x=True)],
    ],  size=(15,10), expand_y=True, expand_x=True)]]

tab1_layout =  [[TreeData.Tree(treedata, [], True,
                   10, 40, '-TREE-', font, 48, False, True, True, True, ['&Right', command])]]   

tab2_layout = [[sg.Column(ui_settings_layout, expand_x=True, expand_y=True, element_justification='left'), 
                sg.Column(site_settings_layout, expand_x=True, expand_y=True, element_justification='left')],
               [sg.Column(author_settings_layout, expand_x=True, expand_y=True, element_justification='left'),
                sg.Column(deployment_settings_layout, expand_x=True, expand_y=True, element_justification='left')],]

menu_def = [['&Server', ['Start Daemon', 'Stop Daemon']],
                ['&Rebuild', ['Rebuild Local']],
                ['&Debug', ['Launch Debug']],
                ['& Deploy', ['Launch Deploy']],
                ['&Help', ['&About...']], ]

layout = [[sg.MenubarCustom(menu_def, pad=(0,0), k='-CUST MENUBAR-', font=font)],
    [sg.TabGroup([[sg.Tab(starting_path, tab1_layout, font=font, border_width=0), sg.Tab('Settings', tab2_layout, font=font, border_width=0)]], tab_border_width=0)]]

window = sg.Window('Heavymeta Press', layout, use_default_focus=False, finalize=True)
window.set_icon(LOGO)
tree = window['-TREE-']
tree.Widget.configure(show='tree') 
tree.bind("<Double-1>", '+DOUBLE')
block_focus(window)

png_b64 = []
seeds = []

while True:
    event, values = window.read() 
    # ------ Process menu choices ------ #
    if event == 'About...':
        sg.popup('About this program', 'HEAVYMETA PRESS',
                 'Version', '0.0.1',  grab_anywhere=True, keep_on_top=True)
        window.reappear()
        
    elif event == 'Start Daemon':
        deployType = DATA.settings['deploy_type']

        if deployType == 'local' or deployType == 'Pintheon':
            print('should start localhost')
            if SERVER_STATUS.server_running == False:
                threading.Thread(target=StartServer, args=(), daemon=True).start()
                SERVER_STATUS.popup_server_status()
        if deployType == 'Internet Computer':
            print('Start Internet Computer')
            if DATA.HVYM.icp_daemon_running == False:
                DATA.HVYM.start_icp_daemon()
        
    elif event == 'Stop Daemon':
        deployType = DATA.settings['deploy_type']

        if deployType == 'local' or deployType == 'Pintheon':
            print('should Stop Daemon')
            if SERVER_STATUS.server_running == True:
                threading.Thread(target=StopServer, args=(), daemon=True).start()
                #SERVER_STATUS.popup_server_status(False)
        elif deployType == 'Internet Computer':
            print('Stop Internet Computer')
            if DATA.HVYM.icp_daemon_running == True:
                DATA.HVYM.stop_icp_daemon()
        
    elif event == 'Launch Debug':
        deployType = DATA.settings['deploy_type']

        if deployType == 'local' or deployType == 'Pintheon':
            print('Open Debug page')
            if SERVER_STATUS.server_running == True:
                site_data = refreshSiteData(DATA)
                DATA.renderStaticPage('template_index.txt', site_data)
                LaunchStaticSite('serve')
            else:
                sg.popup_ok('Start Localhost first')

        if deployType == 'Internet Computer':
            if DATA.HVYM.icp_daemon_running == True:
                option = DATA.HVYM.choice_popup("Deploy site to local Internet Computer?")
                if option == 'OK':
                    DATA.HVYM.loading_msg('Building Site')
                    site_data = refreshSiteData(DATA)
                    DATA.renderDebugICPPage('template_index.txt', site_data)
                    url = DATA.HVYM.debug_icp_deploy()
                    option = DATA.HVYM.choice_popup(f"Do you want to open debug url?")
                    if option == 'OK':
                        webbrowser.open_new_tab(url)
            else:
                sg.popup_ok('Start Internet Computer first')

    elif event == 'Rebuild Local':
        deployType = DATA.settings['deploy_type']
        if deployType == 'local' or deployType == 'Pintheon':
            print('Rebuild Local')
            site_data = refreshSiteData(DATA)
            DATA.renderStaticPage('template_index.txt', site_data)
        elif deployType == 'Internet Computer':
            if DATA.HVYM.icp_daemon_running == True:
                option = DATA.HVYM.choice_popup("Deploy site to local Internet Computer?")
                if option == 'OK':
                    DATA.HVYM.loading_msg('Rebuilding Site')
                    site_data = refreshSiteData(DATA)
                    DATA.renderDebugICPPage('template_index.txt', site_data)
                    url = DATA.HVYM.debug_icp_deploy()
            else:
                sg.popup_ok('Start Internet Computer first')

    elif event == 'Launch Deploy':
        deployType = DATA.settings['deploy_type']

        if deployType == 'local':
            DATA.HVYM.prompt('Current deploy type is set to local.\n Change settings, if you want to deploy live.\n')
        elif deployType == 'Internet Computer':
            if DATA.HVYM.icp_daemon_running == True:
                    option = DATA.HVYM.choice_popup("Deploy site to Internet Computer Main Net?")
                    if option == 'OK':
                        canister_id = DATA.settings['canister_id']
                        DATA.HVYM.set_canister_id(canister_id)

        
    elif event == 'Version':
        sg.popup_scrolled(__file__, sg.get_versions(), keep_on_top=True, non_blocking=True)
    elif event == 'Refresh Files':
        treedata.delete_tree()
        add_files_in_folder('', starting_path, DATA)
        window['-TREE-'].Update(values=treedata)
        window.Refresh()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if len(values['-TREE-']) > 0:
        path_val = values['-TREE-'][0]
        f_name = os.path.basename(path_val)
        f_path = baseFolder(path_val.replace(f_name, ''))
        
        if event.endswith('DOUBLE'):
            if os.path.isdir(path_val):
                do_open_set_page_data(f_name)
     
            if os.path.isfile(path_val):
                do_open_set_article_data(f_path, f_name, window)

        elif event in command:
            
            if os.path.isfile(path_val) and '.md' in f_name:
                if(event == 'Set-Form-Data'):
                    folderData = DATA.getData(f_path, f_name, DATA.folders)
                    data = DATA.getData(f_path, f_name, DATA.formData)
                    if(folderData['type'] == 'Form'):
                        d = popup_set_form_data(f_name, data)
                        if(d != None):
                            DATA.updateFormData(f_path, f_name, d)
                            DATA.saveData()
                            
                elif(event == 'Set-Meta-Data'):
                    data = DATA.getData(f_path, f_name, DATA.metaData)
                    d = popup_set_meta_data(f_name, data)
                    if(d != None):
                        DATA.updateMetaData(f_path, f_name, d)
                        DATA.saveData()       
        
            elif os.path.isdir(path_val) and '.md' not in f_name:
                if(event == 'Set-Column-Widths'):
                    data = DATA.pageData[f_name]
                    colData = DATA.columnWidths[f_name]
                    columns = int(data['columns'])
                    if columns > 1:
                        d = popup_set_column_widths(f_name, data, colData)
                        if(d != None):
                            DATA.updateColumnWidths(f_name, d)
                            DATA.saveData()
            if(event == 'Move Up'):
                moveTreeElementUp(window, DATA, f_path, f_name)
            if(event == 'Move Down'):
                moveTreeElementDown(window, DATA, f_path, f_name)
                                           
    if 'SETTING-' in event:
        arr = event.split('-')
        setting = arr[len(arr)-1]
        val = values[event]
        
        DATA.updateSetting(setting, val)
        DATA.saveData()
        DATA.deployHandler.updateSettings(DATA.settings)

        if setting == 'deploy_type':
            if val == 'local':
                window.Element('PINTHEON-GRP').Update(visible=False)
                window.Element('ICP-GRP').Update(visible=False)
            elif val == 'Pintheon':
                window.Element('PINTHEON-GRP').Update(visible=True)
                window.Element('ICP-GRP').Update(visible=False)
            elif val == 'Internet Computer':
                window.Element('PINTHEON-GRP').Update(visible=False)
                window.Element('ICP-GRP').Update(visible=True)

        if setting == 'theme':
            DATA.setCss(val)
      
    if event == 'Add-Author' or event == 'Update-Author':
        d = popup_author()
        author_list = list(DATA.authors.keys())
        if(d != None ):
            if d['name'] in author_list:
                DATA.updateAuthor(d['name'], d['image'])
            else:
                DATA.addAuthor(d['name'], d['image'])
                
            DATA.saveData()
            window['AUTHOR-LIST'].Update(DATA.authors.keys())

    if event == 'Delete-Author':
        idx = window.Element('AUTHOR-LIST').Widget.curselection()[0]
        key = window.Element('AUTHOR-LIST').Widget.get(idx)

        if key != 'anonymous':
            d = sg.popup_yes_no(f"Are you sure you want to delete: {key}")
            if d == 'Yes':
                DATA.authors.pop(key)
                window['AUTHOR-LIST'].Update(DATA.authors.keys())
                DATA.deleteAuthor(key)
                DATA.saveData()
                
    if(event == 'Reset-Css'):
        DATA.resetCss()
        window.Element('SETTING-theme').Update(text='')
        
    if event == '-DEBUG-':
        site_data = DATA.generateSiteData()
        #print(site_data)
        DATA.refreshDebugMedia()
        DATA.renderStaticPage('template_index.txt', site_data)
        
    if event == '-CANCEL-':
        threading.Thread(target=StopServer, args=(), daemon=True).start()
        
    if event =='-DEPLOY-':
        print('deploy!')
        media = DATA.gatherMedia()
        media_cid = DATA.deployMedia()
        if media_cid != None:
            sg.popup_no_buttons("Media Deployed, Deploying Site", auto_close=True, auto_close_duration=1.5, non_blocking=False)
            DATA.updateAllArticleHTML(DATA.filePath)
            DATA.refereshDist()
            DATA.refreshCss()
            DATA.saveData()
            
        site_cid = DATA.deploySite(False, False)
        
        if site_cid != None:
            sg.popup_no_buttons("Site Deployed", auto_close=True, auto_close_duration=1.5, non_blocking=False)
            url = os.path.join('https://', DATA.settings['backend_end_point'], 'ipfs' ,site_cid, 'index.html').replace('\\', '/')
            webbrowser.open_new_tab(url)
            
if DATA.HVYM.icp_daemon_running == True:
    DATA.HVYM.stop_icp_daemon()      
    #print(values[event])
    #print(event, values)
DATA.onCloseData()
window.close()