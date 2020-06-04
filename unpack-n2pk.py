#!/usr/bin/env python3

from collections import namedtuple
import os
import os.path
import struct
import sys

File = namedtuple('File', ['name','data'])

class N2PK():
  def __init__(self, filename):
    self._body = None
    self._files = []
    self._import_from(filename)

  def _import_from(self, filename):
    data = self._get_bytes(filename)

    # Pick out n2pk header
    header_format = '<i32sQ'
    header_length = struct.calcsize(header_format)
    (_pad, _neocore, body_length) = struct.unpack_from(header_format, data)

    # Isolate body data
    self._body = data[header_length:header_length+body_length]

    # Construct table of contents
    toc = data[header_length+body_length:]
    toc_format = '<i'
    (num_files, ) = struct.unpack_from(toc_format, toc)

    toc_offset = struct.calcsize(toc_format)
    # Get metadata then data for each file.
    self._files = []
    for f in range(0, num_files):
      meta_len_format = '<ii'
      (_unknown, name_length) = struct.unpack_from(meta_len_format, toc[toc_offset:])
      toc_offset += struct.calcsize(meta_len_format)

      name_format = '<'+str(name_length*2)+'sxxqq'
      (raw_filename, file_offset, file_size) = struct.unpack_from(name_format, toc[toc_offset:])
      filename = raw_filename.decode('utf-16')
      toc_offset += struct.calcsize(name_format)

      self._files.append(File(filename,self._body[file_offset:file_offset+file_size]))


  def _get_bytes(self, filename):
    with open(filename, 'rb') as file:
      b = file.read()
      return b

  @property
  def filenames(self):
    return [f.name for f in self._files]

  def write_files(self, output_directory='./'):
    # Be a bit defensive: check if any of the files exist first.
    for f in self._files:
      name = os.path.join(output_directory, f.name)
      if os.path.exists(name):
        raise IOError('Cannot unpack, file already exists: "'+name+'"')
    # Now write them all out.
    for f in self._files:
      name = os.path.join(output_directory, f.name)
      with open(name, 'wb') as output:
        output.write(f.data)


def main(argv):
  if len(sys.argv)<2:
    print('Usage: %s <file.n2pk> [optional_directory]'%sys.argv[0])
    sys.exit(-1)
  input_filename = argv[1]

  # If an output directory is given, create if necessary, then switch to it
  output_directory = './'
  if len(sys.argv)>2:
    output_directory = argv[2]
    if os.path.exists(output_directory):
      if not os.path.isdir(output_directory):
        raise IOError('"'+output_directory+'" exists but is not a directory.')
    else:
      os.mkdir(output_directory)

  package = N2PK(input_filename)
  print('Unpacking into '+output_directory)
  [print('  '+_) for _ in package.filenames]
  package.write_files(output_directory)


main(sys.argv)
