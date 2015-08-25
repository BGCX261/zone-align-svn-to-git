from optparse import OptionParser

def read_list_arg1(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

def opt_parser():
  parser = OptionParser()
  parser.add_option(
    "-o", "--outputdir", dest="outputdir", default = "multidoc_cut/",
    type = "string",
    help = "write results in OUTPUTDIR dir [default : -o multidoc_cut]", metavar="OUTPUTDIR")

  parser.add_option(
    "-c", "--corpus", dest="corpus", default = "corpus_test/", type = "string",
    help="use the corpus CORPUS for the treatment [default : -c corpus_test/]", metavar="CORPUS")

  parser.add_option(
    "-d", "--diagdir", dest="diagdir", default = "diagnostic_dir/",
    type = "string",
    help = "use the diagnostic dir DIAGDIR in order to cut some documents in CORPUS [default : -d diagnostic_dir]", metavar="DIAGDIR")

  parser.add_option(
    "-t", "--typediag", dest= "typediag", default = ["a"],
    type = "string", action = "callback", callback = read_list_arg1,
    help = "type of diagnostic TYPEDIAG considered [default : -t a] Values : {a (asynchronous), s (synchronous), u (unknown)}",
    metavar="TYPEDIAG")

  return parser
