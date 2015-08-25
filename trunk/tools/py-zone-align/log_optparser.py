from optparse import OptionParser

def read_list_arg1(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

#parse des options separees par des ":"
def read_list_arg2(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(':'))

def opt_parser_readlog():
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="logfile", default = "../log/ogpfix_corpus2.log", help="read the log LOGFILE", metavar="LOGFILE")
  parser.add_option("-o", "--outputfile", dest="outputfile", default = "default", help="write results in OUTPUTFILE file", metavar="OUTPUTFILE")

  return parser


def opt_parser_treatlog() :
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="picklefile", default = "../log/ogpfix_corpus2.pickle.log",
                      help="read the log PICKLEFILE[default -f ../log/ogpfix_corpus2.pickle.log]", metavar="PICKLEFILE")

  return parser

