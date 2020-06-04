# Python-based N2PK Unpacker

Neocore uses an in-house multi-file archive format they call N2PK.
The file format is not complicated, and data is not compressed or encrypted.
This script simply pulls apart the multiple files held in an N2PK package and writes them out individually.
The files themselves are not converted in any way, so if they are in an unreadable binary format, they will remain so.

Usage:
```
./unpack-n2pk.py <filename> [optional_directory]
```

If a directory is given, it is created if necessary and files are unpacked there.
If no directory is given, files are unpacked locally.
