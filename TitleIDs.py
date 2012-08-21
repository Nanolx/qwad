#-*- coding: utf-8 -*-
"""
module storing a titleid dictionary
"""
import binascii, re
from PyQt4.QtCore import QT_TR_NOOP

TitleDict = {
#"BOOT2":"0000000100000001",
"System Menu":"0000000100000002",
#"BC":"0000000100000100",
"MIOS":"0000000100000101",
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
"IOS50":"0000000100000032",
"IOS51":"0000000100000033",
"IOS53":"0000000100000035",
"IOS55":"0000000100000037",
"IOS60":"000000010000003c",
"IOS61":"000000010000003d",
"IOS254":"00000001000000fe",
#TODO: Add remaining IOSes
#QT_TR_NOOP("Wii Speak Channel"):"00010001484346xx",
#QT_TR_NOOP("Photo Channel 1.1 [USA]"):"0001000148415a45",
QT_TR_NOOP("Photo Channel 1.1 [PAL]"):"0001000148415a50",
#QT_TR_NOOP("Photo Channel 1.1 [JAP]"):"0001000148415a4a",
#QT_TR_NOOP("Metroid Prime 3 Preview"):"00010001484157xx",
QT_TR_NOOP("Nintendo Channel"):"00010001484154xx",
QT_TR_NOOP("Check Mii Out / Mii Contest Channel[USA]"):"0001000148415045",
QT_TR_NOOP("Check Mii Out / Mii Contest Channel[PAL]"):"0001000148415050",
QT_TR_NOOP("Check Mii Out / Mii Contest Channel[JAP]"):"000100014841504A",
QT_TR_NOOP("Everyone Votes Channel[USA]"):"0001000148414a45",
QT_TR_NOOP("Everyone Votes Channel[PAL]"):"0001000148414a50",
QT_TR_NOOP("Everyone Votes Channel[JAP]"):"0001000148414a4A",
#QT_TR_NOOP("Opera / Internet Channel"):"00010001484144xx",
QT_TR_NOOP("Photo Channel"):"0001000248414141",
QT_TR_NOOP("Shopping Channel"):"0001000248414241",
QT_TR_NOOP("Mii Channel"):"001000248414341",
QT_TR_NOOP("Photo Channel 1.1"):"001000248415941",
#QT_TR_NOOP("Wii Message Board"):"001000148414541",
#QT_TR_NOOP("Weather Channel-HAFx"):"00010002484146xx",
#QT_TR_NOOP("Weather Channel-HAFA"):"0001000248414641",
#QT_TR_NOOP("News Channel-HAGx"):"00010002484147xx",
#QT_TR_NOOP("News Channel-HAGA"):"0001000248414741"
}

#idDict = {}
#for title in TitleDict:
#    idDict[TitleDict[title]] = title

IOSdict = {}
for title in TitleDict:
    if re.search("IOS", title):
        IOSdict[title] = TitleDict[title]
IOSdict["IOS202"] = "00000001000000ca"
IOSdict["IOS222"] = "00000001000000de"
IOSdict["IOS249"] = "00000001000000f9"

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
