from datetime import datetime

now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d%m_%Y_%Hh%Mm%Ss")
name_video = f"resources\good_posture\{dt_string}.txt"
with open(name_video,'w'):
    pass