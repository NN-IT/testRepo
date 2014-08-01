__author__ = 'connerjd'
__version__ = '7/18/2014'

import sys

"""
    This program iterates through a Tape Record .x file and
    stores the data in a different file in .csv format.
    
    The directory must contain a csv/txt file with the following
    text inside of it:

    "DSN","VOLUME","ACCT","EXPDT","CDATE","CTIME","CJOB","CSTEP",
    "CDDNAME","CUNIT","FLAG1","FLAG2","CPGM","FLAG3","FLAG4","FLAG5",
    "VOLSEQ","1STVOL","PREVVOL","NEXTVOL","ACTVOL","DSN17","NUMDSNB",
    "1STDSNB","LSTDSNB","LTIME","LJOB","LUNIT","LPGM","TRTCH","DEN",
    "LABEL","RECFM","LRECL","BLKSIZE","BLKCNT","BTHDATE","COUNT",
    "VENDOR","OUTDATE","OUTCODE","SLOT","TRERRI","TRERRC","TWERRI",
    "TWERRC","VOLPERC","SMSMC","PRERRI","PRERRC","PWERRI","PWERRC",
    "FILPERC","COMPRES","DATECLN","USECLN","CLNCNT","BATCHID","HOOKID",
    "CTLGCNT","AUFLAG1","AUDATE","AUTIME","USERID","AUBLKTM","CPUID","AUCODE"

    The directory must also contain the .x file (WITHOUT A HEADER) that
    is to be parsed.
"""



def main(args):
    """ Main """
   
    #xfile = open("InFiles/TMSAudit_0620_thru_0703.txt")
    xfile = open(args[1], 'r')
    xfilelines = xfile.readlines()
    xfile.close()
    fn = open("FieldnameFiles/fieldnames_Aud.txt")             #don't change
    out = open("TempFiles/temp.txt", 'w')                     #don't change
    #out = open(args[2], 'w')
    #isAfterHeader = True       #use for testing
    isAfterHeader = False
    headerEndLineString = "CONTROL STATEMENTS"

    with fn:
        fnames = fn.readline().split(",")

    #Go through every line in the file
    for line in xfilelines:
        if headerEndLineString in line:
            isAfterHeader = True

        if isAfterHeader:
            #Go through every field name
            for fieldname in fnames:
                fn = fieldname[1:-1] + "="

                #If the fieldname is in the line of the xfile, figure out the value of the
                #fieldname and write it to the out file
                if fn in line:

                    #Distinguishes between DSN, DSN17, and others with DSN in the name
                    if fn == "ACTIND=":
                        index = line.index(fn) + len(fn)
                        out.write(str(int((line[index:index+2]), 16)) + ",")
                        #out.write(fn + str(bin(int((line[index:index+2]), 16))[2:]) + ",")
                        volIndex = line.index(fn) - 9
                        out.write((line[volIndex+1:7]).strip() + ",")
                        #out.write("DSNB_VOLUME=" + (line[volIndex:7]).strip() + ",")
                    elif fn == "DSN17=":
                        index = line.index(fn) + len(fn)
                        out.write((line[index:index+17]).strip() + ",")
                        #out.write((fn + line[index:index+17]).strip() + ",")
                    elif fn == "DSN=":
                        index = line.index(fn) + len(fn)
                        out.write((line[index:index+42]).strip() + ",")
                        #out.write((fn + line[index:index+42]).strip() + ",")
                        volIndex = line.index(fn) - 9
                        out.write(("VOLS_VOLUME=" + line[volIndex+1:7]).strip() + ",")

                    #Distinguishes between FLAG1 and AUFLAG1
                    elif "FLAG" in fn:
                        index = line.index(fn) + len(fn)
                        if fn == "FLAG1=":
                            index = line.index(fn) + len(fn)
                            if line[line.index(fn) - 1] == "U":
                                pass
                            else:
                                out.write(str(int((line[index:index+2]), 16)) + ",")
                                #out.write(fn + str(bin(int((line[index:index+2]), 16))[2:]) + ",")
                        else:
                            out.write(str(int((line[index:index+2]), 16)) + ",")
                            #out.write(fn + str(bin(int((line[index:index+2]), 16))[2:]) + ",")

                    #All of the other fieldnames
                    else:

                        if fn == "AUCODE=":
                            index = line.index(fn) + len(fn)
                            out.write(str(int((line[index:index+2]), 16)) + "\n")
                            #out.write(fn + str(bin(int((line[index:index+2]), 16))[2:]) + "\n")
                        elif fn == "AUBLKTM=":
                            index = line.index(fn) + len(fn)
                            out.write(str(int((line[index:index+8]), 16)) + ",")
                        elif fn == "AUFLAG1=":
                            index = line.index(fn) + len(fn)
                            out.write(str(int((line[index:index+2]), 16)) + ",")
                            #out.write(fn + str(bin(int((line[index:index+2]), 16))[2:]) + ",")
                        elif fn == "ACCT=":
                            index = line.index(fn) + len(fn)
                            out.write(("ACCT=" + line[index:index+8]).strip() + ",")
                        else:
                            index = line.index(fn) + len(fn)
                            out.write((line[index:index+8]).strip() + ",")
                            #out.write((fn + line[index:index+8]).strip() + ",")

def audFileSplitter(args):
    audFile = open("TempFiles/temp.txt", 'r')
    outDSNB = open(args[2], 'w')
    outVols = open(args[3], 'w')

    for line in audFile:
        if line[0:5] == "ACCT=":
            newline = line.replace("VOLS_VOLUME=", "")
            outVols.write(newline[5:])
        else:
            newline = line.replace("VOLS_VOLUME=,", "")
            outDSNB.write(newline)

if __name__ == "__main__":
    main(sys.argv)
    audFileSplitter(sys.argv)