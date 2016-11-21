import pickle
import time
import random
import csv
import subprocess
import shlex



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
            	              .replace("\\","\\\\")
            	              .replace("´","\'")
            	              .replace("_","\_"))
            	            )
    return datalines


names = readcsv('./txt/Vornamen.csv', encoding='utf-8')
surnames = readcsv('./txt/Nachnamen.csv', encoding='utf-8')
places = readcsv('./txt/Orte-PLZ.csv', encoding='utf-8')
streets = readcsv('./txt/Strassennamen.csv', encoding='utf-8')


def generate_name():
    s = names[randint(0, len(names)-1)] + surnames[randint(0, len(surnames)-1)]
    return s


def generate_address():
    s = streets[randint(0, len(streets)-1)] + ", " + places[randint(0, len(places)-1)].replace(";", ", ")
    return s


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
def make_header(font):  
    header = (u"\\documentclass[8pt]{extarticle}\n"
    	      "\\usepackage[T1]{fontenc}\n"
    	      "\\usepackage[utf8]{inputenc}\n"
    	      "\\usepackage{newunicodechar}\n"
              "\\usepackage{verbatim}\n"
              "\\usepackage[paperheight=10.75in,paperwidth=8.25in,margin=1in,heightrounded]{geometry}\n"
              "\\geometry{textwidth=6cm}\n"
              "\\usepackage{eurosym}\n"
              "\\usepackage{tgbonum}\n"
              "\\usepackage{times}\n"
              "\\usepackage{tgheros}\n"
              "\\usepackage{tgcursor}\n"
              "\\usepackage{courier}\n"
              "\\usepackage{lmodern}\n"
              "\\usepackage{helvet}\n"
              #"\\usepackage{fontspec}\n"
              #"\\setmainfont[Mapping=tex-text, Color=textcolor]{FreeSans}\n"
              #"\\textwidth=6cm\n"
              "\\makeatletter\n"
              "\\newcommand{\\verbatimfont}[1]{\\def\\verbatim@font{#1}}%\n"
              "\\makeatother\n"
              "\\pagenumbering{gobble}"
              "\\newunicodechar{Ȳ}{\=Y}\n"
              "\\newunicodechar{ȳ}{\=y}\n"
              #"\\newunicodechar{Œ}{\OE}\n"
              #"\\newunicodechar{š}{\v{s}}\n"
              #"\\newunicodechar{š}{\v{S}}\n"
              #"\\newunicodechar{Œ}{\OE}\n"
              #"\\newunicodechar{Œ}{\OE}\n"
              "\\begin{document}\n"
              "\n \\noindent\n")
    return header + "{\\fontfamily{" + font + "}\\selectfont\n"


def make_body(bodylines):
    return "\n \\input{" + bodylines + "}"


# see https://en.wikibooks.org/wiki/LaTeX/Fonts for fontstring. exmpl: "\\itshape\\sffamily"
def make_verbatim_body(bodylines, fontstring):
    return "\n \\verbatimfont{" + fontstring + "} \n \\verbatiminput{" + bodylines + "}"


def make_footer():
    return "\n } \n\\end{document}"


# randomly adds some buzz words between regular text words
def admix_buzz(prob, lines, buzz):
    if uniform(0, 1) <= prob:
        ind = randint(0, len(lines)-1)
        linesplit = lines[ind].split(' ')
        rndind = randint(0, len(linesplit)-1)
        buzzstr = buzz[randint(0, len(buzz)-1)]
        # add some random dates, names, addresses with 30% prob
        if uniform(0, 1) <= 0.3:
            buzzstr = generate_date()
            if uniform(0, 1) <= 0.5:
                buzzstr = generate_name()
            else:
                buzzstr = generate_address()      

        linesplit[rndind] = linesplit[rndind] + " " + buzzstr
        lines[ind] = " ".join(linesplit)


def create_body_file(fbody):
    with open("./txt/keyphrases.txt", "r") as f:
        buzz = f.readlines()
    with open("./txt/BGB.txt", "r") as f:
        lines = f.readlines()
    
    buzz = [b.rstrip('\n') for b in buzz]
    lines = [l.rstrip('\n') for l in lines]
    # admix keyphrases to text
    prob = 0.5
    [admix_buzz(prob, lines, buzz) for l in lines]
    # make body file and write latex
    lines = [l + "\\\\ \n" for l in lines if len(l) > 3]
    with open(fbody, 'w') as bodyfile:
        bodyfile.write(" ".join(lines))


def create_rnd_body_file(fbody, nwords, nlines):
    lines = generate_utf_body(nwords, nlines)
    lines = [l + "\n" for l in lines if len(l) > 3]
    with open(fbody, 'w') as bodyfile:
        bodyfile.write(" ".join(lines))


# generates latex file. Use pdflatex (not xelatex) to translate to pdf
def generate_tex(font, randomize, fontstring):
    if not randomize:
        create_body_file("./body.txt")
    else:
        create_rnd_body_file("./body.txt", nwords=3, nlines=50)

    with open(font + ".tex", 'w') as texfile:
        texfile.write(make_header(font))
        if not randomize:
            texfile.write(make_body("./body.txt"))
        else:
            texfile.write(make_verbatim_body("./body.txt", fontstring))
        texfile.write(make_footer())
