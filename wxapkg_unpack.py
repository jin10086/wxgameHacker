#!/usr/bin/python

# lrdcq
# usage python wxapkg_unpack.py filename, unpack at filename.unpack

import sys, os
import struct


class WxapkgFile:
    nameLen = 0
    name = ""
    offset = 0
    size = 0

def run(fname):
    with open(fname, "rb") as f:
        root = os.path.dirname(os.path.realpath(f.name))
        name = os.path.basename(f.name)

        # read header

        firstMark = struct.unpack('B', f.read(1))[0]
        print('first header mark = ' + str(firstMark))

        info1 = struct.unpack('>L', f.read(4))[0]
        print('info1 = ' + str(info1))

        indexInfoLength = struct.unpack('>L', f.read(4))[0]
        print('indexInfoLength = ' + str(indexInfoLength))

        bodyInfoLength = struct.unpack('>L', f.read(4))[0]
        print('bodyInfoLength = ' + str(bodyInfoLength))

        lastMark = struct.unpack('B', f.read(1))[0]
        print('last header mark = ' + str(lastMark))

        if firstMark != 190 or lastMark != 237:
            print('its not a wxapkg file!!!!!')
            exit()

        fileCount = struct.unpack('>L', f.read(4))[0]
        print('fileCount = ' + str(fileCount))

        # read index

        fileList = []

        for i in range(fileCount):
            data = WxapkgFile()
            data.nameLen = struct.unpack('>L', f.read(4))[0]
            data.name = str(f.read(data.nameLen),encoding='utf8')
            data.offset = struct.unpack('>L', f.read(4))[0]
            data.size = struct.unpack('>L', f.read(4))[0]

            print('readFile = ' + data.name + ' at Offset = ' + str(data.offset))

            fileList.append(data)

        # save files

        for d in fileList:
            d.name = '/' + name + '.unpack' + d.name
            path = root + os.path.dirname(d.name)

            if not os.path.exists(path):
                os.makedirs(path)

            w = open(root + d.name, 'wb')
            f.seek(d.offset)
            w.write(f.read(d.size))
            w.close()

            print('writeFile = ' + root + d.name)

        f.close()

if __name__ == '__main__':
    fname = 'wx7c8d593b2c3a7703_3.wxapkg'
    run(fname)