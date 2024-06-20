from opentrons import protocol_api as op_api

requirements = {"robot type": "Flex", "apiLevel": "2.18"}  # set according to examples

# labware settings, fill accordingly
tipType1 = "opentrons_flex_96_tiprack_1000ul"
tipLoc1 = "C4"
tipType2 = "opentrons_flex_96_tiprack_50ul"
tipLoc2 = "B4"


def run(protocol: op_api.ProtocolContext):
    # load tip rack1
    tipRack1 = protocol.load_labware(
        load_name=tipType1,
        location=tipLoc1
    )

    # load tip rack2
    tipRack2 = protocol.load_labware(
        load_name=tipType2,
        location=tipLoc2
    )

    # attach tips to selected pipette
    pipetteL = protocol.load_instrument(
        instrument_name="flex_1channel_1000",
        mount="left",
        tip_racks=[tipRack1]
    )

