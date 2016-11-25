import pickle
import time
import random
import csv
import re
import subprocess
import shlex
from time import gmtime, strftime
from random import uniform, randint

data_path = "./GDATA/"
# fonts to run:
# times-like: ptm, lmr
# helvetica/arial: lmss, qhv, phv
# typewriter: lmtt, qcr, pcr

# with unicode euro sign, etc
FONT_FACES = ["lmr", "lmss", "lmtt", "qcr"]


# too many, for later finetuning
#FONT_SIZES = ["tiny", "scriptsize", "footnotesize", 
#              "small", "normalsize", "large", "Large",
#              "LARGE", "huge", "Huge"]


FONT_SIZES = ["tiny", "scriptsize", "normalsize", "Large", "huge"]

FONT_WEIGHTS = ["regular", "italic", "bold", "italicbold"]

rnd_seed = 3048678
buzzwords_prob = 0.7
toupper_prob = 0.15


def set_seed(seed):
    random.seed(seed)


def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def randomDateSlash(start, end, prop):
    # return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)
    return strTimeProp(start, end, '%m/%d/%Y', prop)


def randomDateDot(start, end, prop):
    #return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)
    return strTimeProp(start, end, '%m.%d.%Y', prop)


def generate_date():
    rndnum = uniform(0, 1)
    if rndnum <= 0.5:
        return randomDateSlash("1/1/1990", "1/1/2030", random.random())
    else:
        return randomDateDot("1.1.1990", "1.1.2030", random.random())


def readcsv(fname, encoding):
    datalines = []
    with open(fname, 'r', encoding=encoding) as f:
        reader = csv.reader(f)
        for row in reader:
            datalines.append((" "
                              .join(row)
                              .replace(u'\xa0', u' ')
                              .replace("\\", "\\\\")
                              .replace("´", "\'")
                              .replace("_", "\_"))
                            )
    return datalines


names = readcsv('./txt/Vornamen.csv', encoding='utf-8')
surnames = readcsv('./txt/Nachnamen.csv', encoding='utf-8')
places = readcsv('./txt/Orte-PLZ.csv', encoding='utf-8')
streets = readcsv('./txt/Strassennamen.csv', encoding='utf-8')


def generate_name():
    if uniform(0, 1) <= 0.2:
        s = names[randint(0, len(names)-1)] + surnames[randint(0, len(surnames)-1)]
    else:
        specchar = ["@", "\#", "\$", "\%", "\^", "\&", "\_", "\{", "\}", " \{", "\} ", "*", "|", "€ "]
        char = random.choice(specchar)
        s = names[randint(0, len(names)-1)].lower().strip(" ") + char + surnames[randint(0, len(surnames)-1)].lower().strip(" ")
    return s


def generate_address():
    prefix = [", ","-", " ", " D-"]
    return streets[randint(0, len(streets)-1)] + ", " + places[randint(0, len(places)-1)].replace(";", random.choice(prefix))



def generate_mail():
    pass

# see: http://www.sql-und-xml.de/unicode-database/basic-latin.html
#      http://www.sql-und-xml.de/unicode-database/latin-1-supplement.html
basiclatin = [chr(i) for i in range(32, 127)]
latinsuppl = [chr(i) for i in range(161, 256) if i != 173]


def generate_utf_word(minwlen, maxwlen):
    s = ''
    for i in range(0, randint(minwlen, maxwlen)):
        s = s + basiclatin[randint(0, len(basiclatin)-1)]
    return s


def generate_utf_body(nwords, nlines):
    l = []
    for i in range(0, nlines):
        l.append([generate_utf_word(2, 30) for i in range(0, nwords)])
    l = [" ".join(ll) for ll in l]
    return l


def set_font(fontfamily):
    pass


def set_font_size():
    pass

# fonts to run:
# times-like: ptm, lmr
# helvetica/arial: lmss, qhv, phv
# typewriter: lmtt, qcr, pcr
# latex memory problem: > kpsewhich texmf.cnf
#                       > gedit corresponding textmf.cnf:
#                              buf_size = 400000
#                              main_memory = 10000000
#                       > fmtutil-sys --all
# textwidth tuning for different fontsizes(latex notation)
textwidth = {"tiny": 150,
             "scriptsize": 1.1*150,
             "footnotesize": 1.2*150,
             "small": 1.3*150,
             "normalsize": 1.4*150,
             "large": 1.5*150,
             "Large": 1.7*150,
             "LARGE": 1.8*150,
             "huge": 2.0*150,
             "Huge": 2.1*150}


def make_header(fontface, fontsize, fontweight):
    if fontweight == "bold":
        fweight = "\\textbf{"
    elif fontweight == "italic":
        fweight = "\\textit{"
    elif fontweight == "bolditalic":
        fweight = "\\textit{ \\textbf{"
    elif fontweight == "italicbold":
        fweight = "\\textit{ \\textbf{"
    else:
        fweight = "{"
    header = (u"\\documentclass[10pt]{extarticle}\n"
              "\\usepackage[T1]{fontenc}\n"
              "\\usepackage[utf8]{inputenc}\n"
              "\\usepackage{verbatim}\n"
              #"\\usepackage[none]{hyphenat} \n"
              "\\usepackage[paperheight=10.75in,paperwidth=8.25in,margin=1in,heightrounded]{geometry}\n"
              "\\geometry{textwidth=6cm}\n"
              "\\usepackage{eurosym}\n"
              "\\usepackage{tgbonum}\n"
              "\\usepackage{times}\n"
              "\\usepackage{tgheros}\n"
              "\\usepackage{tgcursor}\n"
              "\\usepackage{courier}\n"
              "\\usepackage{lmodern, textcomp}\n"
              "\\usepackage{helvet}\n"
              "\\makeatletter\n"
              "\\newcommand{\\verbatimfont}[1]{\\def\\verbatim@font{#1}}%\n"
              "\\makeatother\n"
              "\\pagenumbering{gobble}\n")
    #header = header + "\\renewcommand{\\baselinestretch}{" + str(linespace[fontsize]) + "}\n "
    header = header + "\\renewcommand{\\baselinestretch}{1.3}\n "
    header = header + "\\textwidth " + str(textwidth[fontsize]) + "pt \\begin{document}\n"
    header = header + "\\begin{raggedright} {\\fontfamily{" + fontface + "}\\selectfont\n {\\" + fontsize
    header = header + fweight
    return header


def make_body(bodylines):
    return "\n \\input{" + bodylines + "}"


# see https://en.wikibooks.org/wiki/LaTeX/Fonts for fontstring. exmpl: "\\itshape\\sffamily"
def make_verbatim_body(bodylines, fontstring):
    return "\n \\verbatimfont{" + fontstring + "} \n \\verbatiminput{" + bodylines + "}"


def make_footer(fontweight):
    if fontweight == "bolditalic":
        bclosed = "\n }"
    elif fontweight == "italicbold":
        bclosed = "\n }"
    else:
        bclosed = " "
    return bclosed + "\n } \n } \n } \n \\end{raggedright}\n\\end{document}"


# randomly adds some buzz words between regular text words
def admix_buzz(prob, lines, buzz):
    if uniform(0, 1) <= prob:
        ind = randint(0, len(lines)-1)
        linesplit = lines[ind].split(' ')
        rndind = randint(0, len(linesplit)-1)
        buzzstr = buzz[randint(0, len(buzz)-1)]
        # add some random dates, names, addresses with 50% prob
        if uniform(0, 1) <= 0.6:
            buzzstr = generate_date()
            if uniform(0, 1) <= 0.5:
                buzzstr = generate_name()
            else:
                buzzstr = generate_address()      

        linesplit[rndind] = linesplit[rndind] + " " + buzzstr
        lines[ind] = " ".join(linesplit)


def admix_specialchar(lines):
    specchars = ["\\textbackslash", " \\textbackslash ", "$\\mathrm{=}$"]
    if uniform(0, 1) <= 0.01:
        ind = randint(0, len(lines)-1)
        linesplit = lines[ind].split(' ')
        rndind = randint(0, len(linesplit)-1)
        buzzstr = random.choice(specchars)   
        linesplit[rndind] = linesplit[rndind] + buzzstr
        lines[ind] = " ".join(linesplit)


def create_body_file(fbody):
    with open("./txt/keyphrases.txt", "r") as f:
        buzz = f.readlines()
    with open("./txt/BGB.txt", "r") as f:
        lines = f.readlines()

    buzz = [b.rstrip('\n') for b in buzz]
    lines = [l.rstrip('\n') for l in lines]
    # admix keyphrases to text
    [admix_buzz(buzzwords_prob, lines, buzz) for l in lines]
    # convert some strings to upper case
    lines = [l.upper() if uniform(0, 1) < toupper_prob else l for l in lines]
    # make body file and write latex
    lines = [l + " \n" for l in lines if len(l) > 3]
    [admix_specialchar(lines) for l in lines]
    #lines = [l for l in lines if len(l) > 3]
    with open(fbody, 'w') as bodyfile:
        bodyfile.write(" ".join(lines))


def create_rnd_body_file(fbody, nwords, nlines):
    lines = generate_utf_body(nwords, nlines)
    lines = [l + "\n" for l in lines if len(l) > 3]
    with open(fbody, 'w') as bodyfile:
        bodyfile.write(" ".join(lines))


def write_metadata(fdata):
    success = subprocess.call(shlex.split("pdflatex -output-directory " + data_path + " " + fdata[0]))
    ifpdf = True if success==0 else False
    with open(str(fdata[0]) + ".meta", 'w') as f:
        f.write("# ***************************************************************** \n")
        f.write("#  datagen input parameters for data: " + fdata[0] + " \n")
        f.write("# ***************************************************************** \n \n ")
        f.write("Production Date: " + strftime("%d/%m/%Y %H:%M:%S", gmtime()) + "\n")
        f.write(" rnd_seed: " + str(rnd_seed) + "\n")
        f.write(" pdf success: " + str(ifpdf) + "\n \n")
        f.write(" buzzwords_prob: " + str(buzzwords_prob) + "\n toupper_prob: " + str(toupper_prob) + "\n \n")
        f.write(" font_size: " + fdata[2] + "\n")
        f.write(" font_face: " + fdata[1] + "\n")
        f.write(" font_weight: " + fdata[3] + "\n \n \n")


# generates latex file. Use pdflatex (not xelatex) to translate to pdf
def generate_tex(fontface, fontsize, fontweight, randomize, fontstring):
    set_seed(rnd_seed)
    if not randomize:
        create_body_file("./body.txt")
    else:
        create_rnd_body_file("./body.txt", nwords=3, nlines=50)
    
    fname = data_path + fontface + "_" + fontsize + "_" + fontweight + ".tex"
    with open(fname, 'w') as texfile:
        texfile.write(make_header(fontface, fontsize, fontweight))
        if not randomize:
            texfile.write(make_body("./body.txt"))
        else:
            texfile.write(make_verbatim_body("./body.txt", fontstring))
        texfile.write(make_footer(fontweight))
    return [texfile.name, fontface, fontsize, fontweight]
