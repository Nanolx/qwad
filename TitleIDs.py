#-*- coding: utf-8 -*-
"""
module storing a titleid dictionary
"""
import binascii, re
from PyQt4.QtCore import QT_TR_NOOP


def sorted_copy(alist):
    # inspired by Alex Martelli
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52234
    indices = map(_generate_index, alist)
    decorated = zip(indices, alist)
    decorated.sort()
    return [ item for index, item in decorated ]

def _generate_index(str):
    """
    Splits a string into alpha and numeric elements, which
    is used as an index for sorting"
    """
    #
    # the index is built progressively
    # using the _append function
    #
    index = []
    def _append(fragment, alist=index):
        if fragment.isdigit(): fragment = int(fragment)
        alist.append(fragment)

    # initialize loop
    prev_isdigit = str[0].isdigit()
    current_fragment = ''
    # group a string into digit and non-digit parts
    for char in str:
        curr_isdigit = char.isdigit()
        if curr_isdigit == prev_isdigit:
            current_fragment += char
        else:
            _append(current_fragment)
            current_fragment = char
            prev_isdigit = curr_isdigit
    _append(current_fragment)
    return tuple(index)

def swap_dic(original_dict):
	####################### Swap Keys and Values of a dictionary ######################
	return dict([(v, k) for (k, v) in original_dict.iteritems()])

TitleDict = {
"IOS4":"0000000100000004",
"IOS9":"0000000100000009",
"IOS10":"000000010000000a",
"IOS11":"000000010000000b",
"IOS12":"000000010000000c",
"IOS13":"000000010000000d",
"IOS14":"000000010000000e",
"IOS15":"000000010000000f",
"IOS16":"0000000100000010",
"IOS17":"0000000100000011",
"IOS20":"0000000100000014",
"IOS21":"0000000100000015",
"IOS22":"0000000100000016",
"IOS28":"000000010000001c",
"IOS30":"000000010000001e",
"IOS31":"000000010000001f",
"IOS33":"0000000100000021",
"IOS34":"0000000100000022",
"IOS35":"0000000100000023",
"IOS36":"0000000100000024",
"IOS37":"0000000100000025",
"IOS38":"0000000100000026",
"IOS40":"0000000100000028",
"IOS41":"0000000100000029",
"IOS43":"000000010000002b",
"IOS45":"000000010000002d",
"IOS46":"000000010000002f",
"IOS48":"0000000100000030",
"IOS50":"0000000100000032",
"IOS51":"0000000100000033",
"IOS52":"0000000100000034",
"IOS53":"0000000100000035",
"IOS55":"0000000100000037",
"IOS56":"0000000100000038",
"IOS57":"0000000100000039",
"IOS58":"000000010000003a",
"IOS60":"000000010000003c",
"IOS61":"000000010000003d",
"IOS70":"0000000100000046",
"IOS80":"0000000100000050", }

TitleSwapDict = swap_dic(TitleDict)

ChannelDict = {
"BOOT2":"0000000100000001",
"System Menu [JAP]":"0000000100000002",
"System Menu [PAL]":"0000000100000002",
"System Menu [KOR]":"0000000100000002",
"System Menu [USA]":"0000000100000002",
"BC":"0000000100000100",
"MIOS":"0000000100000101",
"BBC iPlayer [PAL]":"0001000148434A50",
"Check Mii Out":"00010001484150**",
"Digicam Print [JAP]":"000100014843444A",
"EULA":"0001000848414B**",
"Everyone Votes":"0001000148414A**",
"Jam With The Band":"00010001484341**",
"Japan Food Service [JAP]":"000100084843434A",
"Mii Channel [ALL]":"0001000248414341",
"News":"0001000248414741",
"Nintendo":"00010001484154**",
"Opera":"00010001484144**",
"Photo [ALL]":"0001000248414141",
"Photo 1.1":"00010002484159**",
"Region Select":"0001000848414C**",
"Shashin Channel [JAP]":"000100014843424A",
"Shop":"00010002484142**",
"Today & Tomorrow":"00010001484156**",
"TV Friend / G-Guide [JAP]":"0001000148424E4A",
"Weather":"00010002484146**",
"Wii No Ma [JAP]":"000100014843494A",
"Wii Speak":"00010001484346**"
}

ChannelRegionDict = {
"BOOT2":"4",
"System Menu [JAP]":"128 2.0, 192 2.1, 224 3.0, 256 3.1, 288 3.2,\
\n352 3.3, 384 3.4, 416 4.0, 448 4.1, 480 4.2,\n512 4.3",
"System Menu [PAL]":"130 2.0, 162 2.1, 194 2.2, 226 3.0, 257 3.1,\
\n290 3.2, 354 3.3, 386 3.4, 418 4.0, 450 4.1,\n482 4.2, 514 4.3",
"System Menu [USA]":"97 2.0, 193 2.2, 225 3.0, 257 3.1, 289 3.2,\
\n353 3.3, 385 3.4, 417 4.0, 449 4.1, 481 4.2,\n513 4.3",
"System Menu [KOR]":"390 3.5, 454 4.1, 486 4.2, 518 4.3",
"BC":"2, 4, 5, 6",
"MIOS":"4, 5, 8, 9, 10",
"BBC iPlayer [PAL]":"latest (PAL only)",
"Check Mii Out":"1, 3, 512,\n** = 45 (USA), 4A (JAP), 50 (PAL)",
"Digicam Print [JAP]":"latest (JAP only)",
"EULA":"1, 2, 3,\n** = 45 (USA), 4A (JAP), 4B (KOR), 50 (PAL)",
"Everyone Votes":"latest\n** = 45 (USA), 4A (JAP), 50 (PAL)",
"Japan Food Service [JAP]":"latest (JAP only)",
"Jam With The Band":"latest\n** = 4A (JAP), 50 (PAL)",
"Mii Channel [ALL]":"2, 3, 4, 5, 6",
"News":"3, 6, 7,\n** = 41 (ALL), 45 (USA), 4A (JAP), 50 (PAL)",
"Nintendo":"latest\n** = 45 (USA), 4A (JAP), 50 (PAL)",
"Opera":"1, 3, 257, 512, 1024\n** = 45 (USA), 4A (JAP), 50 (PAL)",
"Photo [ALL]":"1, 2",
"Photo 1.1":"1, 2, 3,\n** = 41 (ALL), 4B (KOR)",
"Region Select":"1, 2,\n** = 45 (USA), 4A (JAP), 4B (KOR), 50 (PAL)",
"Shashin Channel [JAP]":"latest (JAP only)",
"Shop":"3, 4, 5, 6, 7, 8, 10, 13, 14 (KOR only), 16,\n17, 18, 19, 20, ** = 41 (ALL), 4B (KOR)",
"Today & Tomorrow":"latest, ** = 4A (JAP), 50 (PAL)",
"TV Friend / G-Guide [JAP]":"latest (JAP only)",
"Weather":"3, 6, 7\n** = 41 (ALL), 45 (USA), 4A (JAP), 50 (PAL)",
"Wii No Ma [JAP]":"latest (JAP only)",
"Wii Speak":"1, 256, 512,\n** = 45 (USA), 4A (JAP), 50 (PAL)"
}

IOSdict = {
"IOS4":"65280 (stub)",
"IOS9":"520, 521, 778, 1034",
"IOS10":"768 (stub)",
"IOS11":"10, 256 (stub)",
"IOS12":"6, 11, 12, 269, 525, 526",
"IOS13":"10, 15, 16, 273, 1031, 1032",
"IOS14":"262, 263, 520, 1031, 1032",
"IOS15":"257, 258, 259, 260, 265, 266, 523, 1031, 1032",
"IOS16":"512 (stub)",
"IOS17":"512, 517, 518, 775, 1031, 1032",
"IOS20":"12, 256 (stub)",
"IOS21":"514, 515, 516, 517, 522, 525, 782, 1038, 1039",
"IOS22":"777, 780, 1037, 1293, 1294",
"IOS28":"1292, 1293, 1550, 1806, 1807",
"IOS30":"1037, 1039, 1040, 2576, 2816 (stub)",
"IOS31":"1037, 1039, 1040, 2576, 3088, 3092, 3349,\n3607, 3608",
"IOS33":"1040, 2832, 2834, 3091, 3607, 3608",
"IOS34":"1039, 3087, 3091, 3348, 3607, 3608",
"IOS35":"1040, 3088, 3092, 3349, 3607, 3608",
"IOS36":"1042, 3090, 3094, 3351, 3607, 3608",
"IOS37":"2070, 3609, 3612, 3869, 5662, 5663",
"IOS38":"3610, 3867, 4123, 4124",
"IOS40":"3072 (stub)",
"IOS41":"2835, 3091, 3348, 3606, 3607",
"IOS43":"2835, 3091, 3348, 3606, 3607",
"IOS45":"2835, 3091, 3348, 3606, 3607",
"IOS46":"2837, 3093, 3350, 3606, 3607",
"IOS48":"4123, 4124",
"IOS50":"4889, 5120",
"IOS51":"4633, 4864",
"IOS52":"5661, 5888 (stub)",
"IOS53":"4113, 5149, 5406, 5662, 5663",
"IOS55":"4633, 5149, 5406, 5662, 5663",
"IOS56":"4890, 5405, 5661, 5662",
"IOS57":"5404, 5661, 5918, 5919",
"IOS58":"6175, 6176",
"IOS60":"6174, 6400 (stub)",
"IOS61":"4890, 5405, 5661, 5662",
"IOS70":"6687, 6912 (stub)",
"IOS80":"6943",
}

DESCdict = {
"BOOT2":"Second level boot",
"System Menu [JAP]":"System Menu for japanese Wii",
"System Menu [PAL]":"System Menu for european Wii",
"System Menu [USA]":"System Menu for american Wii",
"System Menu [KOR]":"System Menu for korean Wii",
"BC":"GameCube compat",
"MIOS":"GameCube IOS",
"IOS4":"",
"IOS9":"",
"IOS10":"",
"IOS11":"",
"IOS12":"",
"IOS13":"",
"IOS14":"",
"IOS15":"",
"IOS16":"",
"IOS17":"",
"IOS20":"",
"IOS21":"",
"IOS22":"",
"IOS28":"",
"IOS30":"",
"IOS31":"",
"IOS33":"",
"IOS34":"",
"IOS35":"",
"IOS36":"",
"IOS37":"",
"IOS38":"",
"IOS40":"",
"IOS41":"",
"IOS43":"",
"IOS45":"",
"IOS46":"",
"IOS48":"",
"IOS50":"",
"IOS51":"",
"IOS52":"",
"IOS53":"",
"IOS55":"",
"IOS56":"",
"IOS57":"",
"IOS58":"",
"IOS60":"",
"IOS61":"",
"IOS70":"",
"IOS80":"",
}

IOSids = {}
for ios in IOSdict:
    IOSids[IOSdict[ios]] = ios

def AsciiID(channelname):
    return binascii.unhexlify(TitleDict[channelname][7:])

if __name__ == "__main__":
    print TitleDict["System Menu"]
    print TitleDict["Mii Channel"][7:]
    print AsciiID("Mii Channel")
    print idDict["0001000248414741"]
