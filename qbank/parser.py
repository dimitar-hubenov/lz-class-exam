#!/usr/bin/python
# Program to parse published pdf files

import sys, getopt
import re

# if you don't have it: pip install PyPDF2 
import PyPDF2


question = {
    "number": 0,
    "question": "",
    "answer": "",
    "options": {}
}

def question_init():
    question["number"] = 0
    question["question"] = ""
    question["answer"] = ""
    question["options"] = {}

def main(argv):
    inputfile = ''
    outputfile = ''
    qWritten = 0
    oWritten = 0
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('parser.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('parser.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if (len(inputfile) == 0):
        print("Input file is not set!")
        sys.exit()
    if (len(outputfile) == 0):
        print("Putputfile file is not set!")
        sys.exit()

    with open(outputfile, 'w', encoding='utf-8') as ofile:
        ofile.write("[\n")

    with open(inputfile,'rb') as pdfFile:
        pdfText = []
        pdfReader = PyPDF2.PdfReader(pdfFile)
        pdfPages = len(pdfReader.pages)
        print("Pages found {}".format(pdfPages))

        for page in pdfReader.pages:
            pageText = page.extract_text().splitlines()
            pdfText = pdfText + pageText

        count = 0
        question_init()
        toParse = ""

        for pdfTextLine in pdfText:
            count += 1
            #print("Line{}: {}".format(count, pdfTextLine.strip()))

            pdfTextLine = pdfTextLine.strip()
            if (len(pdfTextLine) == 0):
                if question["number"] != 0:
                    with open(outputfile, 'a', encoding='utf-8') as ofile:
                        if qWritten > 0:
                            ofile.write(",\n")
                        ofile.write(
                            "\t{{\n"
                            "\t\t\"id\":{},\n"
                            "\t\t\"question\":\"{}\",\n"
                            "\t\t\"answer\":\"{}\",\n"
                            .format(
                                question["number"],
                                question["question"],
                                question["answer"]
                            )
                        )
                        oWritten = 0
                        for option in question["options"]:
                            if oWritten > 0:
                                ofile.write(",\n") 
                            ofile.write(
                                "\t\t\"{}\":\"{}\",\n".format(option, question["options"][option])
                            )
                        ofile.write(
                            "\t\t\"shuffle\":true\n"
                            "\t}"
                        )
                        qWritten += 1
                question_init()
                toParse = ""
                continue

            toParse += " "+pdfTextLine
            if question["number"] == 0:
                #print("regex: \"{}\"".format(toParse))
                parser = re.search("^\s?(?:[0-9]+\s)?([0-9]+)\.\s*(.*\?)\s*\W\(([АБВГ])\)\s*$", toParse)
                if parser:
                    question["number"] = parser.group(1)
                    question["question"] = parser.group(2).strip()
                    question["answer"] = parser.group(3).strip()
                    print("QNum {}: Q:{} A:{}".format(question["number"], question["question"], question["answer"]))
                    toParse = ""
            else:
                #print("regex: \"{}\"".format(toParse))
                parser = re.search("^\s?([АБВГ])\.\s*(.*)[;.]$", toParse)
                if parser:
                    question["options"][parser.group(1).strip()] = parser.group(2).strip()
                    print("QOpt {}: {}".format(parser.group(1).strip(), question["options"][parser.group(1).strip()]))
                    toParse = ""

    with open(outputfile, 'a', encoding='utf-8') as ofile:
        ofile.write("\n]\n")


if __name__ == "__main__":
   main(sys.argv[1:])

#python parser.py -i Class1AktualiziranRazdel1_2022.pdf -o class1-section1.json
#python parser.py -i Class1AktualiziranRazdel2_2022.pdf -o class1-section2.json
#python parser.py -i Class1AktualiziranRazdel3_2022.pdf -o class1-section3.json

#python parser.py -i Class2AktualiziranRazdel1_2022.pdf -o class2-section1.json
#python parser.py -i Class2AktualiziranRazdel2_2022.pdf -o class2-section2.json
#python parser.py -i Class2AktualiziranRazdel3_2022.pdf -o class2-section3.json