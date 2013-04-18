#
# TODO:
# -
####################################################################################################

import ClipAPI

ART = 'art-default.png'
ICON = 'icon-default.jpg'

####################################################################################################

DEVICE_TYPE = 'Plex ControlHue'
DISCOVERY_BROKER = 'http://www.meethue.com/api/nupnp'

LINK_RETRY_COUNT = 5

def Start():
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = L('Title')

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)


@handler('/applications/controlhue', L('Title'), ICON, ART)
def MainMenu():

    oc = ObjectContainer()

    bridges = FindHueBridges()

    if len(bridges) < 1:
        return MessageContainer("Error", "Cannot find any Philips Hue bridges on your network")
    else:
        # TODO: len(hues) > 1 -> select controller
        bridge = bridges[0]

        errcnt = 0
        while (errcnt < LINK_RETRY_COUNT):
            try:
                api = ClipAPI(bridge)
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

                # Break out of our retry loop since we reach here without exceptions
                break
            except LinkError as e:
                errcnt = errcnt + 1
                return MessageContainer("Error", "Press the link button on your Philips Hue bridge")

    #oc.add(PrefsObject(title="Preferences", summary="Configure how to connect to Trakt.tv", thumb=R("icon-preferences.png")))
    return oc


def FindHueBridges():
    return JSON.ObjectFromURL(DISCOVERY_BROKER)


def ToggleLight(light, api):
    if light.get('active'):
        api.off(light.get('id'))
    else:
        api.on(light.get('id'))
