from optparse import OptionParser

def read_list_arg1(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

#parse des options separees par des ":"
def read_list_arg2(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(':'))

def opt_parser():
  parser = OptionParser()
  parser.add_option(
    "-o", "--outputfile", dest="outputfile", default = "out.log",
    help="write results in OUTPUTFILE file", metavar="OUTPUTFILE")

  parser.add_option(
    "-g", "--languages", dest="languages", default = ["es","fr"],
    type = "string", action = "callback", callback = read_list_arg1,
    help="use LIST_LANG languages for alignment", metavar="LIST_LANG")

  parser.add_option(
    "-n", "--nb_multidoc_occur", dest="nb_multidoc_occur", default = [2,10000],
    type = "string", action = "callback", callback = read_list_arg1,
    help = "only considers substrings occuring between NB_MULTI[0] and NB_MULTI[1] different multidocument",
    metavar="NB_MULTI")

  parser.add_option(
    "-c", "--corpus", dest="corpus", default = "corpus_test/", type = "string",
    help="use the corpus CORPUS for alignement", metavar="CORPUS")

  parser.add_option(
    "-d", "--distance", dest="distance", default = "docdistance", type = "string",
    help="compute similarities between substrings using the distance DISTANCE", metavar="DISTANCE")

  parser.add_option(
    "-r", "--relative_frequency", dest="relative_frequency", default = [2,1000],
    type = "string", action = "callback", callback = read_list_arg1,
    help="only considers substrings occuring between REL_FREC[0] and REL_FREC[1] times in the monolingual subcorpus", metavar="REL_FREC")

  parser.add_option(
    "-l", "--length", dest="length", default = [3,500],
    type = "string", action = "callback", callback = read_list_arg1,
    help="only considers substrings of length between LEN[0] and LEN[1] ", metavar="LEN")

  parser.add_option(
    "-s", "--score", dest="score", default = [0.,0.1],
    type = "string", action = "callback", callback = read_list_arg1,
    help="only considers couple of substrings having a score distance between SCORE[0] and SCORE[1] ", metavar="SCORE")

  parser.add_option(
    "-w", "--window_size", dest="window_size", default = 500, type = "int",
    help="compare substrings having comparable relative frequency in a window WIN_SIZE", metavar="WIN_SIZE")

  parser.add_option(
    "-e", "--difference_frequency", dest="difference_frequency", default = 20, type = "int",
    help="compare substrings having the same relative frequency +/- DIFF_FREQ", metavar="DIFF_FREQ")

  return parser
