import os
import sys
import pickle
import pathlib
import SiteDataHandler
from io import BytesIO
from PIL import Image, ImageDraw
import PySimpleGUI as sg

sg.theme("DarkGrey13")
NAME_SIZE = 23


folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA3XAAAN1wFCKJt4AAAE7mlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4yLWMwMDAgNzkuMWI2NWE3OSwgMjAyMi8wNi8xMy0xNzo0NjoxNCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIzLjUgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyMi0xMC0wNlQyMTo0NToyNy0wNzowMCIgeG1wOk1vZGlmeURhdGU9IjIwMjItMTAtMDZUMjE6NTY6MzctMDc6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjItMTAtMDZUMjE6NTY6MzctMDc6MDAiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOmM2ZTdhMDRkLWNjOTMtNDc0NC1hNjgwLWY2ODZjOWZjOTkyNyIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpjNmU3YTA0ZC1jYzkzLTQ3NDQtYTY4MC1mNjg2YzlmYzk5MjciIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDpjNmU3YTA0ZC1jYzkzLTQ3NDQtYTY4MC1mNjg2YzlmYzk5MjciPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmM2ZTdhMDRkLWNjOTMtNDc0NC1hNjgwLWY2ODZjOWZjOTkyNyIgc3RFdnQ6d2hlbj0iMjAyMi0xMC0wNlQyMTo0NToyNy0wNzowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIzLjUgKFdpbmRvd3MpIi8+IDwvcmRmOlNlcT4gPC94bXBNTTpIaXN0b3J5PiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PuxPXaQAAAFhSURBVFiF7de9itRQGMbx3znJREEHVNBiC7HyLpRBC6/AWhY/aq/C0htwi90LERRL72CttFywERk0cfJaZAZGGHGYjZwt5oFAzglv3v9585yPpIhQUrlo9osAUDtJ6+1nuIfL6EfOlfEDH3C06kxxvHwY3gqzv4aOq3d4iD5r0XohzFTLZKurQkKLxfJ+HM3wEmo3KiqPXa2oE+uzIi0zznvOOjpMMM7EuY/XtYPJU8kDPfogbaj3rZom8bkdnDFOJTqodfHqz/4Nw5sH04pp5ms/WPQ8SkgWAwDXtgpaBDdruo4udjdmMvipNV8BtGj+GdgFTeZOM0Ts+hkSfgXf+wOLUNvWUslQhbSGu6sZJ5kr+RGepHh/6RumO77qvDorvRRfLw3wszRAlAYovx3vAfYAe4DV4atY/mybrfj/qck4LQhwmnFYEOCwxkfcxXPcNubhe7MCX/AGn9L+57Q0wG/4oVYsu0eeMwAAAABJRU5ErkJggg=='
folder_icon_off = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA3XAAAN1wFCKJt4AAACkElEQVRYhe2XT0gUURzHP+/tY92NNtyJlswlKsSDkcYGwkKJ/aGIqEMQBFEhWWfDU8qeVkQCy0snvXfbwLNeLPIQSHgQWiMiFMFghBbd1XbmdRgddilxRse2Q1+Yw/zen99nfu/3fu+N0FpTS8maev8XAETuzOnK927gAhAB7IB9SaAEvAXGtozKbdRMouncdmhwegDcAy4DtsSWYMsnaDqRm84qH+F0CzgenUAPgCIKSO6IOgUhAZW7QggA9LoNBcAWIAPbNR3ACyXq1SMEl9CArUH8Hm9xKARKoE0LNE5U9q6fAApLD1aZ/1QXNoCIhIgNpRDo8t5cC0BgOQBQ72mQBnFQoi0Lyuw+CgInn2y5tgWwAYR3HFjWoCTisMBh34MsjV63j6EdAG9ZJXByBCC0adttPiqJiMhrwEO1Y+cKtfRkAFiammBlZtq1x1NpGjquADA3kt15Isslf+4L4MCRBMn0eRrOtTN5/6ZrTz3tI9aYZGH6nZ/pAOK+atzscJaiaRJrTNLWPwRAW/8QscYkRdNkdtjD11drPXT35NFnQJ2X3lZxFfPzPCeu3iB+qgkZT9B03YnE+0wvq18++QbwXeVXZqbJj+cAaL51G4D8eK4qJ/xoV8fM3EiWcqkIQLlU9JZ4QQK09GRQkSgAKhJ1d8dfAYin0m7oP46+ApyliKfS+w8QNhK09w0Azrp/fT3m5kN73wBhI7G/AK29GaKGQWFxwV33uZEshcUFooZBa6//pfBciMJGgrXvy+THcyxNTVS1zbwcdCth2EiwYS57BhBvLp79AcQ8jwhWha2LV60kJV6O4v1TWAL5GgLkJdBVQ4AuBXwAmoHHwHGCunJuLw18A0aBefH/57TWAL8As2q+p/+gTSYAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACTUlEQVRYheWXy2sTURSHf+fOI69JrVRFixSE0oWgBUEQly7cFFeCi+6lf0Ch0L8gdCO4jK58kJXQRdtFqWIXLbZQFNSVm4LRRJvSptbWkOTe46JNGWdi585koogfZJFz7z3nu/fMIyFmhpv7j+dQq+32SSWniOgmgF4EIKVCKmlLJ+NM9DjZh4MD5yCVajv32vDQL99Nf7LmScXqLQH9QYVbMBgAIZUwHlw43/fj6qXBp7prhTdQb+zfA3M/iHRzHEkkEwl8LG08WX79/nZkAWa+FbZ4C8MwoJTCuw/rz4rlykgkAbRpiy7MDNu2kM2ksLC8Nlv8UrkRRaAeVaAlkbRtGKaBlytvXmzt7F4PK9AxihlOOgmpGHOLK0vfvu9d+aMCAKAUo8dJoyklzS6uvtrbr13smgADICLYlgnbMmEdfgxD4FTvCUgp7fmltdV6oznkXRv5gnNjCIFmU6JYroDo4DpwI4TA56+bzqPpned374wMxC9ABCklNreqh6fhnyNIYP1T+aw3HovAUQts69h5WTNd9YnFIdAJf10gsAWTY6MAgFy+4Iu54+6Yd+w4tE+gXYE41oRuQVDSXL7w29OKRSBuQgmEaYNO/0MLhEFXNpKA7u50iOVJ6Ma78yBZ7ROIsmudNeR9c+XyhQ0Ap0NX06MyOTZ6xh34t27D/0bA7mI9X+52Ao0uCvhy+wWIZg5+48QLM4OYZgIFLDM5DoiS9/bssDpIUMnOpMe9Q74noWUmtqVqXJZSTQHQ+nseQJWZFwxhThgpa9s7+BMoWNGFUVzMQgAAAABJRU5ErkJggg=='
block = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAB2ElEQVRYhe2XvW7UUBCFv7nXe1drLSIKAYQUGgq6SDwBEiUVJR3vlieISEFKJJ6AeiWIBJEoCCIoq/gnvjMUXiSIbO86YQ3FHrdn5oxn5lhjMTOI3yF+heheI+4ZwpS1QOaovcVXL/A74LcRM4Py22Pi6Xv8aLIe4SuIZYa/94SwPROLx1BJgVUBkUH0MQUJJYkbJ+T5AUkSEA/YMAWIBysDeXUglh/niI6HUb4ClcL9M3EAZ+Okm6EgE3Bp/+R6AZYBrpOWYBhCw/bpQjhAeUIToxUGjB6ASF1IWxGGtXfATUBG8PkV/HgHS3r1Byrg9lN4uF/n0aKV2p5WplB+hLMjiPQzSKSOu38C4RHQXkD3gAZAewdsDmEXtp73H4FQjyDs1nm6qJZ/0OYljLUD/BbEsx7qC/yKswzwzRzDVhjBdb+Oq8V1uCAFCfDp5c1cYLJxQSc2Lti4YOOC/9kFvx0kl1+ud5BQrnCQNIpTB+kFiNVv0hernGSCLGmsAysgti/R0vilDO1Y0XVDrXCYHWFKvyHfFFL/HRlvxOIpVPMCuwzIQK40BRmVJOnY4e4A0z20yoZRBzRmcGsPd3exJZ4ZSZIS5RC1cwzF/vqjKOdEDvFJimcG8BMSLBgJ+mh9jgAAAABJRU5ErkJggg=='
block_thumb = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAADRklEQVRYhe2Xv28cRRTHP29mbi93XPCv2JadgKwIHCgiRSmoEBINkouIClEi8R/Q8qOioKSJ6JFoQJFCUmApUYQUqBAgItHEwQSIZQviiw2++O72duZRzBns2Lu+jbErvlfN7sx733nv+52dE1UFvwb+PnhzBTEvIzQ4FEiLoF9is1exJ8COIqoKaXMWv/oDtlI7nMSPwKdt7MQ5ktEFUX8XMumiWYLIkeRHA0iS4kzV0elcxrkEsYBy56dfWF7+HQUepbP1bHp6kmefmXl8AmJB04ROdtlhj81B6IeH6ze+5rnzr/RTKQoYiaOg8dn1G9cORgAFMWCqcw4J1e2vsswzc+YFAIKCs2AN+ADOQLcHP34zf4Dk22C06vLehQBP1mJd3ruUca+pvP9ahZMjgNTAjhQHD5ugbcAUTnMoiuxsd1CoV+NunYW1h9BsRUKNY4Bfh95SflQFKlMgEonkkVB0zwqcaMBfbXjrk4znTwofveFYasKn1zIuvGih+SEsXswnkAFDL8FTH4OpQegWVGAPbHSEdy/1aG4oX91WTo0ZVhY9F69k3LylXDAp9NJ8Ah5Yn4fJJUhOAyUJvP1Zj3sPlMlhQYHPv/NsrinnThtWVgNM5Ocuiz0J/LqqTA0JPsTx8QRGnhYePoBxBWwClUp+VCG2IDkF2ipPYGpI8PrvWIkVr41KPCyTd2D2zcLA2OEoVm0DdnAC1lom/LcYQBEQB5rFjbUFngAb8gPupL0/RDuLYbsNF+7cZXnlD5AKIhW4/wG0boED7cecHhdmZwr8vd0Fmua7QNFdBP6BHYP0Z7h9Pqp6kE1vYWv+me+jC3wzl0DxMXUEyD2K0VZU8fAc/HmzaOZulHBBfgvw/TN/OKq5LAZxwWAtGEzNj7suv7CmDpLAb6+Xb8EOF0j5bwEA0oguWJ+Pqi5TiBLfgv9dUOCCEHVAAr2V3TfUImxdSEgHuJDsmZy4KGyCaNxJWQxyJRNkn8Ia0C74fBHtu37fGaFAooeNoF2D6jwaKNfkg0LivyPlC1G/Clmri/YS5IhcqQGkkuLqVYMZAxpnCVn7aLIDwbfh+FnMeF8llgWcq+PlKkE3UAL6n/8CgQ08V7GujmUB4G8kg4WLRjM/2wAAAABJRU5ErkJggg=='
block_inset = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAADDUlEQVRYhc2XMW8cVRSFv/vmzXhn1saOQ7I2hVFQhCwBCUUSIUThLolS8QNoKPgXVPwLChoKfgNCkdxFQEVCYaGARaLYWWNlbda7O5l5712KSRBRMutZ22tyy3lX75x37tF5b0RVoehB8RdEZptgOijCNMqIItrFu2WSNyFZxAAg4TqqijdLUwMHCCp4ltCgCNcBRPNNCKI4BzI97BdKA9gEjBFLyLfwFkwEqqdDwETgCrBuS3S4qfhwOsAvERFsLbgAETxzydEqAB6oEzYothbcwmhwwIM/NhkO8sn8oUrWbrHyzgXS9iy4ehKi/d9fXrIwHPT57de7BJPizBkqKZqMquqzoYcJI959/xJZe64i0ZhAAht3f2FYeIx7yvz+OnH5GI1fLdgLG5aOMl5if36NYGfIkojVS5eheHV/7Y6jQYFLOnT2vmb75++qj9Gh+NXMgeWrA7rnvmA06I5tr7WYmghVoZXfrzZtagGpSLTy+6gKasazriUgwSOijLLVSqemEaFUBs5WEVEk+LHttSMQccR+h94bN1n8eBnreqhp4IHgcPYMvexDYr+DSI37DiMAYMoRxcxbPFn4lH+H26giotAnebqFRuNJ16+qUCQdZoc/svLnl+yNII4Phy5LWEjhwdtfcZBeIXZPjkYgEKOmxXx/nXubVG5pkooBHgZYWVyn3/6EwHjWxwnaE6laBQwlEnL259b44MLtyUcwt4aEHEN5NAKIkhRd+ulH3HvvDgTffAQmwvgDZopHxzAhEOKUxO2Q/f0D1u8dGipQ5YeLFhhmlwlxioQjKqBqKaPznN/7hsc/fVsFTNMoFli69hk7Zz8n9seM4nS4Ud1kk0Sxg3S4cTJRnLcuViefJIojyFsXjxfFaTtBi116C7foXGtPfB335tewukvaTsb3v54Pkv/9SfacxLQfpYBFahqUWtlOrEQxGN1Gw+n9FUGFpQEMW6LFLrgDxZUgp3Q3aQAbg83EEJ8FO3tj+nr/tzzYuRvE557lgPI9xgpGtgmhg05pHoJi6OLt8nPf/QNzJHCGkCkPvgAAAABJRU5ErkJggg=='
block_inset_thumb = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEdklEQVRYhb2X328UVRTHP/fOj+1Mu/QX/QWIRaApMY2NQuMDifXFhBg1MfGRmPjgu69Gn/gXjI+86IuGBOFBEohoUGNiSpTUGLpQ0Lb0F20X2O3sj5m5x4dpKbA72xYs32Qy2XvvnvM933vPuWeUiEA1D9W7IPoc6DdRtLAjUEVEfkRF7+HuBrcDGwAxA8TyJ5b2dsbxOiSL4l1iEyAMAzkl5dsQqQomclFqZ/0/5GFAu1VsnbGplM+ibRdtgQg3Jv9hdnYBAZ6ksz62Z08Phw/2Pz0BbYGpulSiszZW0wnEgAgAly7/wuDRt9ZcCQJoBUqBMcnYpcsXn42ACCgNKnPCRkzm0bkoiuk/MgKAEbAtsDTEBmwNlRD++vUChFuJdO1J3VnJ2GlTxsAuL5H98zMR08vCqQ8c9rbDzNwUf4yPNYzQb/bY/8JhPMcBR6eSsKF2u42An0mitS3Ir8JyMSHU0gSxaia0OhuEbVgt5Zm4PsbA4Gv4OgN2XQZSV4HdLfCgBJ98HXFkr+LLD21mluGbixHvHLdoDa7Qt3KnrnsVRoROL/dbRzGOx9RUjsHBY0AlVYEaFMqKz86ELBeEnyeEfZ2aucmYL85FXLkmDE2Pc+fqeH0B4uTVd2yVha6PKQUL4LRAtA0Cn34bMr0i9LQpBPjuakyQF4Zf0swtGYbqu16TAIigqXwTEYVoq9Hq+gT+XRL6WhWxSX5nXWjfr1hdgS4B5htYlMRqyR9EKUGZGMJiw0NYg75WRSyP2wyr4HUolIKWynG6RurroExEZLeT94dx4kWUiiAMwK2vRA0By7Loro4RBAUQg2gXYePPvoZSdoS7He+nSABgYZkCbmUWsVIzPSEshUnDIwLlbtxmdmaRm7f+JrayeJUJuhdOs1pNKihAbysc7KlvMAyhzYOpF09R9I7iRCsMv/oGqLqHsDYNBw4fYKD/ALt22URuF/vmLzKVh7YmkhQHMHBrLiUkA9MG9nf8RKH5OAanYRbouqPPEakbpAlRpsz97ChDB37gXgkcZ3ODD7cgO4oyZTTh9rMAACW41QUK3uuMv/wbmHhrehmY1hY6LpKp3kkO4Xay4DFbjocbLeI/uIQd39u0qAAoExNZbQT+KxjHQ5nG12YqARGb0Oqm+95p5n//KikGm/tPSrGC3pGTLHZ+hBMvgOOTdhekiiraQkThBdchosGd/gTWSrEXXN8oxU56j5tKQJkYpYRy06Ekcklb+SRzwIJy06GNUtwAqVvg+S4SLpFve5uekWaccB5xGlc12LiO862j2LKE52caZkFNJQQghiAokstdw2iPSLez3mhsjmSdbfJoU0oakoyb9HO1ECWFyVpxBYigVF5lamaSIKiwrZZ9Gy1ZfQLrJAxbCzoNmzalYCNUUGRqZhTJ4dtK6j0tRCoa5AJitifxs0Kp5OsIvldSXYJqsYIJXdRzupvEgHaquH5G43SC3TKEiUrPxztg4hJ2dgina60QKXLYto+o84gUSI6e/M+PQSggnMeyfRQ5gP8AuX7rgBNTjGAAAAAASUVORK5CYII='
expandable = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACnElEQVRYhe2XzU8TQRjGfzO73X7YgiD4kRAlBhcTL3qGePIgepSzfwPhr9CY8A/oxTtehcTEg8azYtRgReFAwoEilBba3e7OeJjyEdldSsEqic9tZt99n2fmnWf2XaG1hto6bK+ClJMgxwEXcDhZ+AhRBD1NGEyR64NsL8IIWOtjq/QKK3XzhEmjEfpznDl/h2xvSejNRVDiK0HgIkVH+FEKbKeILYdtGvUJsF2kBejOCJAWBL5LGEwIvb74Ca1udIb5d4jPEq0G/w45gB60gfjCawV2FlK59vI3tiGogZBxEcIGwljyVA6kA+XlJJnR0EDhEghhhESLCO3YBKksWCl48RAW3kB8ZDQCYOg2PHgOZCHwIsMSBORh/QfMz5g9Co4oIMS8W16GnquxAmKL0ynE70CjCt0DcH3seCXoHjC5YiD0z++bQOHAE63AzoHlQG3NzIUeaA3ShnSXOWBJyHRDvdx0ghUVUYlfl5DQ2IJ0HvIXzJyTB68C2R6oroCKNtBRkLyxmbOw8h6KL83YvQ+XR+DtI3j9GEQj3p77XSBEGy6w0uBXDfnWqplbmIUro1CcgcoGpBPEn34XhB44BXDv7ZVg6K45hO4YLH9srQRtuwAMWboLQt+MrRR4m5DrNwdUq+TlteCCf7gEYFa/+uWgC949+e+CE8MpcYHfTODkwa9ApnkVh2G8gJ2GRPnGMQnfgsgnRp4whFaz2H7FWK9ehvxFDm2TdluyWArLppVePNx3gIQEFNQ3Dn1tLz4WWgJLrWX6A9B6SYJ+hlIcves8DoT5OxI8FbpWAq86T9AYRnbIlUqBnSri5IYlmXPg5EfRwYfOsAM6nMMpjJDt370HSlj2LYSYRKlxhLhG8j3XDjzgG4JppD21M/kLU7wpI7/D7KcAAAAASUVORK5CYII='
expandable_thumb = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAADsklEQVRYhc2XS2icVRTHf/feb57ONCbNo2lCDaGdaHVRN0VIEMUHPujKuu6mG6GLWneiK92IWDdFBEUQ3ChZ6MZIAxaqFsQHRkTbqbUpCY6amaSZRzLzPe51cWda05lvZtLGkP/uO3O5///5zvmf74wwxsD6CqwtgZSnQB4FMkCUrYWLEFkw0wT+aZL9kOhDWAGFfir5WVTk0BaTtkbgznHX4OMk+vLCFK+CFpfw/QxSbAs/WoMTzeLICQevehKcDFIBhst/zPNn7m+MAXGLnkZs7/AQB8bHbl+AVOC7GQL/pIOMH8dowAAwe+5r7j38JCAAgwGksE/a2NjsubN3JgADUgKx4w5Gb7jJ9wPGDh4GQBtwFCgJgQZHQs2DXy7M3AH5BiFjDja5JmgNuxL2vbw67bNQMLz2fISRXiCSgHhv5/u9NfDXQciwE8IBgiZyA8mYzdZRsFKBQtkKSsWB6nUoLnZIDkgP26bx1sJEBE6raH8Kiuvw4kc+940I3jnmsFiAj8/6HJlScOFt0GfaC/CB/Q/Dcx8CCfBrLY+1FFCqCl6Z9iiUDF9dMozuluSuBJz5zOf8nOGI50LVbS8gAC7OwOoi9I5vTsDLn3gsLBuG7hYY4NMfAtZWDIfGJbm8bk+8SbQUcC1vGO4RBHWudBR69wkqyzBggH+iEI+0v7lRgp5R8MqbEzDcIwjMzWcDeC4k+oQdToMvwYkXmifVrYj3QHW17gTVnQClFIPu90jqY0hF7QgEhHYg6aPkCCgHdJOBNo0mAU88Msn9f12zhJEkrM7DwrcAmNGHYOgB9uauwlsHQXghU4SNLhAitAmFWb5SBNJNv6gYBC589y5UlmwsvQceex0+eBR+Ow+xNqkFgAJO/GhdsF5odaoUOqK2Cy2bEICgBtE0ZJ6B7Oc2tv8p2w+Zp2Hx5+5K0MEF4SUASxbbZUsBoCJQK0JyALwK9ivaBp1dsJNLADb7pV9vliDzLOybhG/ehC/f2BIXhAtQMXDLlrzhgt+/gHumIDsDpeudXdDFt2AHl2BHucCtXxBNgVuy21A5B0EQLqCxkGjXOibEBQ52XoXIE5ZQ1Yvtlqz1qquQ2kM4ex03VrJQCuXQWIfbIfhPAwkJaLuWdYPwfRDASGC+u5v+BxgzL8G8j9Z0fJ1bCmHXbsF7wqznoVa+iO9N2D8L2wCtwYlkiSYnJPHdEE1NYfyftocdMMEc0fQkiYEbcyCPch5EiFNofRQhDtB+zt0OasBlBNNI53Qj+C/m+YRcxXtYXQAAAABJRU5ErkJggg=='
expandable_inset = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEHElEQVRYhb2XTW8bVRSGn3PvzPgjdgu1nUCatEUUukCFoi6gQiCVDRIqZc0KiR+ABP+ADb8AsWfBAoFUUVUgxAIJqQuEyoeKQARCmyZp7DSpE9uNPZ6597BwKC3xuElpcqTZzD2673s+3jNnRFUhbkLvBoj5HDWnEUrsikkH9Bs0fZ18FXIHCABQ/yRef8KaArI70APTMnAW7zdQTgAzop0roBLj0gjZVfQ7eHiwUR9rcgFp7xwSRIgFdG8IiAXXj3DpOdHWlR7qc3uDvIVJHIwE9/y/pAhgRjloLsg8Sx0rN66zuHgNJ3kwdlC7bQEb8CmHpiapHqhBGGa6BgxivLv7PDQa89SXrpFENZwpIc6B3R4+DjS0zNWbeJcwPjENdmgqdHgGFJYbSyRRjWLnN8YXPiVwTTTcHgNJHGmuSn3yDRZXHmP8YAE0HuqbWYKEHM6UeHT+I36//MsgRzvIAPoHR4HZJ96HsAT94QQyW0QlQpwjf2tu8GK74Hf45rpziHcjXTMJWO2iYUCrenIQ/eh77jYHCLQfPokaC0kn0zWzBOJjwt4y9cm3qJx+nkBb4B3GerwzuGA/msFf8LiwyHLxGLmkAclBCIanMFuGCNa1ScMKq4+cQXyKmgibdnBBGfExghueGat4U8Smt4j6C9kQowmAs2Vs0qZW/4x8d5b1h15itXaG8aWP2Xf5AzY8yJAbkgTKOWg/9TarlTMQFneuAjUhanPsW/uW/TcvIvQJ3QXWKi9TvXGBX1dG019uwrHaV6wcOHt/Khhq/sF/LUc0YYJIQqv8HEG/SXHjT9b2v4iXiNXaqzxe/ZDuPUrQHH8FET9SBaLrs57/jmIHP/94EXA4KeHsGIKiCFHaoB9N4YNwoPFtNOEzJ17IUkHGKP7nVEMQyLvr2LhNP6zhzBhh3KBwcwaj/eFRbcqwWzyGmsIoiHuoICiT712lVv+EQnyV9fIpFg6/w5G/3uPq919nT8fNrBw69Rrz0++OVEH2KDYRai2l9R8obFxB+8K+9e+waYty+9LoPWFzuSo3Lw3KFGbvuNkq8Cminl7pCGlYxUhKt3AUHxTphYdHoHM7A3Hh8GAUj7DMElgDuA1ujT3N8qSQ7y3QHnsWk27QmH6TowRY14JwqzTv/BxH2rkPFXhoLM1RX5pHTQ5nCqixiEsJXJM0rJCaMuL98D5woNYSuBbTtRLjE1Ngs1WwNQQDExNTWGNZXJzDuhQkQOgDliBZQ0x8G2xrWAbSlEMHJ6lWalngACK6PpvdTru+lA56IAaGb8Y7G9Q7N9XYgH452Hb36K8IBljqQfhCNF6BfifGJRGy2yFvmnqwYZ+wmDNEFQhKx/Fpd2/QAe+6BOXj5GqbVRZmCIIiyHlU2/zbfg/y8Sht4Dw2KCLMAPwNgivPR6qFILIAAAAASUVORK5CYII='
expandable_inset_thumb = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAEyElEQVRYhb2XzW9UVRjGf+ece2c605lC25k29ItWSquSIkajaapRFmoggisXrvAvMMGl0YUxcefO8Be4wZAgLCRSDYlfiUFQlBApVNr0c7BlaKeddmbuOa+LW6Cxc4cWgSeZ3Mw9997ned/zPu85R4kIlPKw+g8ofQrR+1GkeCRQSyDnkOAt6jIQb8IDQFwfTn7H6ATq0VCHkDRwGOeKCPuAESVLN0BUCRvEUI+UfZ0OByZWxui4R7B6EuXFUAYQro2OMT2TQ2BDMu7ca9vRyu5d3Q8uQBmw5Rg2OOmh6w4gbu3zMHzuR558/nVQCkQQQOuQ2El4b/jc2f8nAAGlgfgBD3Hx9UNBYOl++gUAnIBnwGiwDjwNpQpc/vkM2M1ECuiaQuJe1JBz0JAI8/LRiYCJeeGTt33aG2FyeoKLly7WINbgAro62sg0ZcH3Ix/1YON0O4FkPIzWM5BfhvmlUFCqDqxJEsSaogVYEN8wPpvH2QotrZ1hGqukoGoGMilYXIGjXwQ81a44dsRjch6Onw049JIhmzvB7r++i05AxRLEM8y2vcPUXA8t7QmQUmQGNqCwqvjwRIX5gvDDVaGjWTMzavn8VMD3l4SBmRxXL+dqZgC5Ri8wuvtT8FNQ3oKAD76sMHFLaN2uEOCrC5ZiXtj3hGZmzjEQTR3CAAHEV8ZRrna1VhUwPifs2KawLvyfjkFjl2L5FmTlfuyEGVBQaHwO0QYqS1sTsGObwq4jEqBShkSTQilILw2ReWUIifCYwmH9JDeT/cQrOai0h9W8GQHGGFrKv1JcXgwbkfYQ5a/J0NRrS7FpkPnsQRS2ej8wgtNJTLBMrDwZGX1VAa/tH2LP1Dij1/7EmTjaVkgvnidWmmYptZfFhkH6G2bZ9e2rFB2oKjmsVCAdh8Ke95hvfhP85OZd0NfbQ19PD9vTCmvqaZwfpnn2OooyNvYH1/vepf/KZ1yZq/b2PdzMQ3/2G+aaDtd0Qc1GuQHu4a+WkTEoV0GpCovpF/HKeZLF69ze9jJOxZjPHmRX5hgr95mCfMsbKOVqukDJwqjjvyuvhUu//QRYrEphTT0KQVDEghzlWAfO80OPb6IIn9k3FOWC6q347qj4oKDOTmNKBcp+Fqvr8Us5ErdG0FKuHtWaDVeS/YhO1KKoVUZgvTR1q2NkZ4+TKI2xkB5kcudRuv/+mLHzw2HHq/pieOkaPMRE5/s1XRBZhKJjiDGkFi6SKN5AyoqGhV8wwSLpwoU7+5fqCDdXpPMXwmnyo/e40S5wAUocq6luAj+DVgEriV6cl2TV31mDnbsZKCV2hq24BiKnwGjAFlmu38vNNkXd6iSF+mfRQZFc5xF68TB2EfyN1ly/HMdk6QFc4CA3M87szASi41idQLRB2QDP5gn8ZgKdRjlXvQ4siDF4dpHObIqW1g4w0S7YGIKG1tYOjDZMTY1jbADKQ1EGDF7lNkqX7pJtDEtDENDV3kamORtFDqCULIxGl9O9zfKD4b6b0rAGSkC86ujWGvXWIVLSIGfCc8FjOhVByCUOFF8rKc1BeamErcTCw8JjgDgwfhk/GdfEmsFLDeCClcfDDji7gpceIJ5dm2XFCJ6XBHUakQL3yu9h/hxCATiN8ZIoRgD+BUwpDkCitwrUAAAAAElFTkSuQmCC'
card = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAA7AAAAOwBeShxvQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAF2SURBVFiF7Za/SgNBEIe/kXSioKBPYB5AX0RMYWFhJRZKECFoFUFtREhSCL6FGPQJbGIXEDuN9iL4tzQ7a3G5eJfLJSdkL839YNm722W/HzN7w0CmTGOWxK407CxKAcMiljkMYAEDaIJnb/8rhiZtLtmQt+QGGnYH5QhlGg0cnmT03/uJUmZTzoYbaNgqyu6QA/8DD65X2JZSvIFbW8Bw4QTuD8syRbnykRMhA4ZDp3AF2hz3j8CNzSM8OIWb7rzAnjz1RiCfClw7rI5yXbxlMhW4N6Z87F8E0oN73yIR8AuNa7gSUi70lga8x0TyFIy2IPWJwKAUjPp+BDQ8Ba4uZ0eDU+Dyz4hEwPAdSoFLuOUraqBNC0kBrsAPj9EUrEoL5T6FgnRHTZ6jBrw0HDiGg6EcRIYNrEkdpeIMrpxSk+t4AwDrUkIp4rVRo4J/oGxRlf1eXHxTem5nEFawLGGZ7zaaSrLm1JtfUJrkqHMi77GsTJnGqV9yNlgHEHsA2gAAAABJRU5ErkJggg=='
form_email = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAE7mlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4yLWMwMDAgNzkuMWI2NWE3OSwgMjAyMi8wNi8xMy0xNzo0NjoxNCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIzLjUgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyMi0xMC0wN1QxNDowNDo1Ni0wNzowMCIgeG1wOk1vZGlmeURhdGU9IjIwMjItMTAtMDdUMTQ6MjE6NDQtMDc6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjItMTAtMDdUMTQ6MjE6NDQtMDc6MDAiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjhkMzcwOWVmLTg1OTItMTE0ZC04ZTg2LWM1ZWM1OTA2YmZmYiIgeG1wTU06RG9jdW1lbnRJRD0i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'
ignore_file = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACWklEQVRYheWXPW8TQRCG39m9O/suDrKxYyMgCFFQUIBEAYiSgiYikaCi5S9E+D8kESkCEgjS8FEBDYQOuUNCVCjIiI4G2UKO0UVBsbmP3aUKOu6c3IcvIMTb3czOzDM7d3taUkohqMGNOfS+U1U4YoGILgMoI07SByYOiFK51Cw1yg/0cxegHG/kUuPq9d+etfAC11cV6aoPUuOHuZCxtQFA+YAGCafcuK+fOT+0ZmafJAoEwMIGe4uWBWeJi/+CEATdKsJprz+2nz67lhlAKXUlbfEdcc4hpcR2q/Xc+dSeyQSAEWNJKqUUeNECq9Wxsbr6yml/vJQFwM0KsAPBJk1w6Og/etjyO52LaQHGFnkCVJsC91z0VlbeuP1vZ/8oAACQ74LX6lCuT/byrbdiyz61bwBMAEQEmCZgWmAFE6xgAnoBxvEjEEIY9r2779RwcDICGj6IPs/N9gBMpQEgX4IMDVr1ICRpCOdkjMHvfYU+Pf3l6O07x4K+zG98UKKogzwfXrcD5glIFk3LdMLg/fqhsD0XAOYLgAhcLwA6wHdZp1Urm5HYPADG0V8HiB1B7WYTANBfWozYgvagLezbS4l3YFSBPGJSjyAuaX9pcdfdygUgb6UCSDOGJPNPDZBGSWEzASTtLolyOQmDCnceB5t4B7J0nSQml79hCm2cePGyHjT8W5/hfwNg7GO9SO5RAKMvdfkokjsCwCXWBOV+PEApBbJoLRZg0pLzBrxu+PMcR4IzEPRuZZvNh32RVidKzP4xVKd9pS2ARLLr+d7aVEq91kk2TdWww86fjc/a7PX2dcMAAAAASUVORK5CYII='

def load_save_data(file_dir):
    result = None
    if os.path.isfile(file_dir) and os.path.basename(file_dir) == 'site.data':
        data = open(file_dir, 'rb')
        result = pickle.load(data)
        
    return result
    

def add_files_in_folder(parent, dirname, command, data):
    files = os.listdir(dirname)
    
    if(data.fileExists):
        for f in files:
            fullname = os.path.join(dirname, f)
            if os.path.isdir(fullname):
                treedata.Insert(parent, fullname, f, values=[0], icon=folder_icon )
                add_files_in_folder(fullname, fullname, command, data)
            else:
                file_extension = pathlib.Path(f).suffix
                f_icon = file_icon
                f_name = os.path.basename(f)
                f_path = fullname.replace(f_name, '')

                dataObj = None
                
                if f_path in data.folders.keys():
                
                    for key in data.folders[f_path]:
                        obj = data.folders[f_path][key]

                        if(obj['path'] == f_name):
                            dataObj = obj
                            break
                    if dataObj != None:
                        if(dataObj['active'] == False):
                            f_icon = ignore_file
                        else:
                            if(dataObj['type'] != 'Default'):
                                f_icon = get_file_icon(dataObj['type'])

                                
                if file_extension == '.md':
                    treedata.Insert(parent, fullname, f, values=[
                                    os.stat(fullname).st_size, 0], icon=f_icon)
    else:
        for f in files:
            fullname = os.path.join(dirname, f)
            if os.path.isdir(fullname):
                treedata.Insert(parent, fullname, f, values=[0], icon=folder_icon )
                add_files_in_folder(fullname, fullname, command, data)

            else:
                file_extension = pathlib.Path(f).suffix
                f_icon = file_icon
                f_name = os.path.basename(f)
                                
                if file_extension == '.md':
                    f_path = fullname.replace(f_name, '')
                    treedata.Insert(parent, fullname, f, values=[
                                    os.stat(fullname).st_size, 0], icon=f_icon)
                    
                    data.updateFile(f_path, f, 'Default', True)
                
    data.saveData()
                
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
    elif uiType == 'Card':
        result = card
    elif uiType == 'Form-Email':
        result = form_email
        
    return result
                
def set_file_icon(event):
    item = tree.Widget.selection()[0]
    key = tree.IdToKey[item]
    f_icon = get_file_icon(event)
        
    tree.update(key=key, icon=f_icon)
        
    
def double_click(method_arr):
    item = tree.Widget.selection()[0]
    key = tree.IdToKey[item]
    index = treedata.tree_dict[key].values[-1]
    index = (index + 1) % 3
    treedata.tree_dict[key].values[-1] = index
    tree.update(key=key, icon=method_arr[index])
    
def dir_icon(check):
    png = folder_icon
    
    if check == 2:
        png = folder_icon_off
    return png

def icon(check):
    png = file_icon
    
    if check == 2:
        png = ignore_file
    return png


def name(name):
    dots = NAME_SIZE-len(name)-2
    return sg.Text(name + ' ' + ' '*dots, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Courier 10')

#Window controll
def block_focus(window):
    for key in window.key_dict:    # Remove dash box of all Buttons
        element = window[key]
        if isinstance(element, sg.Button):
            element.block_focus()
            
def popup_set_description(md_name):

    col_layout = [[sg.Button("Save", bind_return_key=True, enable_events=True, k='-SAVE-DESCRIPTION-'), sg.Button('Cancel')]]
    layout = [
        [sg.Text(f"File: {md_name}")],
        [name('Meta-Description'), sg.Multiline(s=(15,2), k='-DESCRIPTION-')],
        [sg.Column(col_layout, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Set Description", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    return values['-DESCRIPTION-'] if event == '-SAVE-DESCRIPTION-' else None

dir_check = [dir_icon(0), dir_icon(1), dir_icon(2)]

check = [icon(0), icon(1), icon(2)]

starting_path = sg.popup_get_folder('Folder to display')
if not starting_path:
    sys.exit(0)
    
DATA = SiteDataHandler.SiteDataHandler(starting_path)

command = ['Block', 'Block-Thumb', 'Block-Inset', 'Block-Inset-Thumb', 'Expandable', 'Expandable-Thumb', 'Expandable-Inset', 'Expandable-Inset-Thumb', 'Card', 'Form-Email', 'Set-Description']
treedata = sg.TreeData()
add_files_in_folder('', starting_path, command, DATA)
font = ('Ariel', 16)

tab1_layout =  [[sg.Tree(data=treedata, headings=[], auto_size_columns=True,
                   num_rows=10, col0_width=40, key='-TREE-', font=font,
                   row_height=48, show_expanded=False, enable_events=True, right_click_menu=['&Right', command])],
          [sg.Button('Ok', font=font), sg.Button('Cancel', font=font)]]    

tab2_layout = [[name('Site Name'), sg.Input(s=15)],
               [name('Navigation'), sg.Combo(DATA.navigation, default_value=DATA.settings['pageType'], s=(15,22), enable_events=True, readonly=True, k='-COMBO-')],
               [name('Theme'), sg.Combo(DATA.themes, default_value=DATA.settings['theme'], s=(15,22), enable_events=True, readonly=True, k='-COMBO-')],
               [sg.In(key='in')]] 

layout = [[sg.TabGroup([[sg.Tab(starting_path, tab1_layout, tooltip='tip'), sg.Tab('Settings', tab2_layout)]], tooltip='TIP2')]]

window = sg.Window('Tree Element Test', layout, use_default_focus=False, finalize=True)
tree = window['-TREE-']         # type: sg.Tree
tree.bind("<Double-1>", '+DOUBLE')
block_focus(window)

while True:
    event, values = window.read()
    #print(event)
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if len(values['-TREE-']) > 0:
        path_val = values['-TREE-'][0]
        
        if event.endswith('DOUBLE'):
            if os.path.isdir(path_val):
                double_click(dir_check)
            if os.path.isfile(path_val):
                double_click(check)
        elif event in command:
            if os.path.isfile(path_val):
                f_name = os.path.basename(path_val)
                f_path = path_val.replace(f_name, '')
                if(event == 'Set-Description'):
                    print('x')
                    description = popup_set_description(f_name)
                    print(description)
                else:
                    set_file_icon(event)
                    DATA.updateFile(f_path, f_name, event, True)
                    DATA.saveData()
        
        

    #print(event, values)
window.close()