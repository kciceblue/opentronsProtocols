from opentrons import protocol_api as op_api

requirements = {"robot type": "Flex", "apiLevel": "2.18"}  # set according to examples

# labware settings, fill accordingly
tipType = "opentrons_flex_96_tiprack_1000ul"
tipLoc = "C4"
pipetteSingular = "flex_1channel_1000"
pipette8Channels = "flex_8channel_1000"


def run(protocol: op_api.ProtocolContext):
    # load tip rack
    tipRack = protocol.load_labware(
        load_name=tipType,
        location=tipLoc
    )

    # attach tips to selected pipette
    pipette = protocol.load_instrument(
        instrument_name=pipetteSingular,
        mount="left",
        tip_racks=[tipRack]
    )
