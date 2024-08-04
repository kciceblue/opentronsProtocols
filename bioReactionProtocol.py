from opentrons import protocol_api as op_api

# metadata
metadata = {
    "protocolName": "TX014",
    "author": "Tom Xu",
    "description": "Protocol for biocatalytic reactions to evaluate enzymes in TX014",
}

requirements = {"robot type": "Flex", "apiLevel": "2.19"}  # set according to examples

# labware settings, fill accordingly
tipType1 = "opentrons_flex_96_tiprack_1000ul"
tipLoc1 = "C4"
tipType2 = "opentrons_flex_96_tiprack_200ul"
tipLoc2 = "B4"
hsModName = "heaterShakerModuleV1"
hsAdapter = "opentrons_universal_flat_adapter"
hsPlate = "nest_96_wellplate_2ml_deep"


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

    # attach tips to selected pipette
    pipetteS = protocol.load_instrument(
        instrument_name="flex_1channel_1000",
        mount="left",
        tip_racks=[tipRack2]
    )

    # load trash
    trash = protocol.load_trash_bin(location="A3")

    # load heater shaker mod
    hs_mod = protocol.load_module(
        module_name=hsModName, location="C1"
    )

    # load heater shaker adapter
    hs_adapter = hs_mod.load_adapter(hsAdapter)
    # load heater shaker plate
    hs_plate = hs_adapter.load_labware(hsPlate)

