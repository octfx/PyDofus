import io, sys, os, tempfile, fnmatch
from collections import OrderedDict
from pydofus.d2p import D2PReader, D2PBuilder, InvalidD2PFile
from pydofus.swl import SWLReader, SWLBuilder, InvalidSWLFile
from pydofus._binarystream import _BinaryStream

path_input = "./input/"
path_output = "./output/"

try:
    file = sys.argv[1]
except:
    file = None

try:
    mode = sys.argv[2]
except:
    mode = None

if file is None or mode is None:
    print("usage: python compress.py {d2p file} {swl mode true|false}")
else:
    print("D2P Compressor for " + file)

    try:
        os.stat(path_output + "~generated")
    except:
        os.mkdir(path_output + "~generated")

    d2p_input = open(path_input + file, "rb")
    d2p_template = D2PReader(d2p_input)

    d2p_ouput = open(path_output + "~generated/" + file, "wb")
    d2p_builder = D2PBuilder(d2p_template, d2p_ouput)

    list_files = OrderedDict()

    rootPath = path_output + file

    for root, dirs, files in os.walk(rootPath):
        for filename in fnmatch.filter(files, "*.*"):
            path = os.path.join(root, filename).replace("\\", "/")
            file = path.replace(rootPath + "/", "")
            print("pack file " + file)

            object_ = {}

            if "swl" in file and mode == "true":
                print("swl file compression")
                swl_input = open(path, "rb")
                swl_template = SWLReader(swl_input)

                swl_output = tempfile.TemporaryFile()
                swl_builder = SWLBuilder(swl_template, swl_output)

                swf = open(path.replace("swl", "swf"), "rb")

                swl_builder.SWF = swf.read()
                swl_builder.build()

                swl_output.seek(0)
                object_["binary"] = swl_output.read()

                swf.close()
                swl_input.close()
                swl_output.close()
            elif "swf" in file and mode == "mode":
                continue
            else:
                new_file = open(path, "rb")
                object_["binary"] = new_file.read()
                new_file.close()

            list_files[file] = object_

    d2p_builder.files = list_files
    d2p_builder.build()

    d2p_input.close()
    d2p_ouput.close()