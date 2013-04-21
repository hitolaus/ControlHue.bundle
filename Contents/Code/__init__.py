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


def Start():
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = L('Title')

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)


@handler('/applications/controlhue', L('Title'), ICON, ART)
def MainMenu():

    oc = ObjectContainer()

    bridges = FindHueBridges()

    Log(bridges)

    if len(bridges) < 1:
        return MessageContainer("Error", "Cannot find any Philips Hue bridges on your network")
    else:
        # TODO: len(hues) > 1 -> select controller
        bridge = bridges[0]

        return ListLights(bridge)

    #oc.add(PrefsObject(title="Preferences", summary="Configure how to connect to Trakt.tv", thumb=R("icon-preferences.png")))
    return oc


@route('/applications/controlhue/refresh')
def Refresh(bridge):
    return MessageContainer('test', 'test')


def ListLights(bridge):
    api = ClipAPI(bridge)

    oc = ObjectContainer()
    try:
        for light in api.list():
            if light.get('active'):
                thumb = R("icon-bulb-on.png")
            else:
                thumb = R("icon-bulb-off.png")

            oc.add(
                DirectoryObject(
                    key=Callback(ToggleLight, light, api=api),
                    title=light.get('name'),
                    thumb=thumb))
    except LinkError:
        oc.add(DirectoryObject(key=Callback(Refresh, bridge=bridge), title=L("Refresh"), summary=L("Click this after you have pressed the link button on your Hue bridge.")))

    return oc


def FindHueBridges():
    return JSON.ObjectFromURL(DISCOVERY_BROKER)

@route('/applications/controlhue/toggle')
def ToggleLight(light, api):
    if light.get('active'):
        api.off(light.get('id'))
    else:
        api.on(light.get('id'))
