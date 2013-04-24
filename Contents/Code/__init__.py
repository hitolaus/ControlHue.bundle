#
# TODO:
# -
####################################################################################################

from clip import *

ART = 'art-default.png'
ICON = 'icon-default.jpg'

####################################################################################################

DEVICE_TYPE = 'Plex ControlHue'
DISCOVERY_BROKER = 'http://www.meethue.com/api/nupnp'

API = None


def Start():
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = L('Title')

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)


@handler('/applications/controlhue', L('Title'), ICON, ART)
def MainMenu():
    global API

    oc = ObjectContainer()

    bridges = FindHueBridges()

    Log(bridges)

    if len(bridges) < 1:
        return MessageContainer("Error", "Cannot find any Philips Hue bridges on your network")
    else:
        # TODO: len(hues) > 1 -> select controller
        bridge = bridges[0]

        API = ClipAPI(bridge)

        return ListLights()

    #oc.add(PrefsObject(title="Preferences", summary="Configure how to connect to Trakt.tv", thumb=R("icon-preferences.png")))
    return oc


@route('/applications/controlhue/refresh')
def Refresh():
    return MessageContainer('test', 'test')


def ListLights():
    global API

    oc = ObjectContainer()
    try:
        for light in API.list():
            if light['active']:
                thumb = R("icon-bulb-on.png")
            else:
                thumb = R("icon-bulb-off.png")

            Log(type(light))

            oc.add(
                DirectoryObject(
                    key=Callback(ToggleLight, light=JSON.StringFromObject(light)),
                    title=light['name'],
                    thumb=thumb))

        oc.add(DirectoryObject(key=Callback(AllLightOff), title='All Off'))
    except LinkError:
        oc.add(DirectoryObject(key=Callback(Refresh), title=L("Refresh"), summary=L("Click this after you have pressed the link button on your Hue bridge.")))

    return oc


def FindHueBridges():
    return JSON.ObjectFromURL(DISCOVERY_BROKER)


@route('/applications/controlhue/toggle')
def ToggleLight(light):
    global API

    light = JSON.ObjectFromString(light)
    if light['active']:
        API.off(light['id'])
    else:
        API.on(light['id'])


@route('/applications/controlhue/alloff')
def AllLightOff():
    global API

    for light in API.list():
        API.off(light['id'])
