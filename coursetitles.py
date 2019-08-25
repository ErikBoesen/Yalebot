import yalecourses
import os
import time

SUBJECTS = ["ACCT", "AFAM", "AFST", "AKKD", "AMST", "AMTH", "ANTH", "APHY", "ARBC", "ARCG", "ARCH", "ARMN", "ART", "ASL", "ASTR", "BENG", "BIOL", "BNGL", "BRST", "BURM", "CENG", "CGSC", "CHEM", "CHLD", "CHNS", "CLCV", "CLSS", "CPAR", "CPSC", "CSEC", "CZEC", "DEVN", "DRST", "DUTC", "EALL", "EAST", "ECON", "EDST", "E&EB", "EENG", "EGYP", "ENAS", "ENGL", "ENRG", "ENVE", "EP&E", "ER&M", "EVST", "F&ES", "FILM", "FNSH", "FREN", "G&G", "GLBL", "GMAN", "GREK", "HEBR", "HGRN", "HIST", "HLTH", "HMRT", "HNDI", "HSAR", "HSHM", "HUMS", "INDN", "ITAL", "JAPN", "JDST", "KHMR", "KREN", "LAST", "LATN", "LING", "LITR", "MATH", "MB&B", "MCDB", "MENG", "MGRK", "MMES", "MTBT", "MUSI", "NAVY", "NELC", "NSCI", "PERS", "PHIL", "PHYS", "PLSC", "PLSH", "PNJB", "PORT", "PSYC", "RLST", "ROMN", "RSEE", "RUSS", "S&DS", "SAST", "SBCR", "SCIE", "SKRT", "SLAV", "SNHL", "SOCY", "SPAN", "SPEC", "STCY", "SWAH", "TAML", "TBTN", "THST", "TKSH", "TWI", "UKRN", "URBN", "USAF", "VIET", "WGSS", "WLOF", "YORU", "ZULU"]
SLEEP = 1

api = yalecourses.YaleCourses(os.environ["YALE_API_KEY"])
titles = []
for subject in SUBJECTS[3:]:
    print("-> " + subject + " \r", end="")
    titles += [course.name for course in api.courses(subject)]
    time.sleep(SLEEP)

with open("resources/coursetitles.txt", "w") as f:
    f.write("\n".join(titles) + "\n")
