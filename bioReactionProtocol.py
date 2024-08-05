from opentrons import protocol_api as op_api

requirements = {"robotType": "Flex", "apiLevel": "2.19"}  # set according to examples

# metadata
metadata = {
    "protocolName": "TX016",
    "author": "Tom Xu",
    "description": "Protocol for biocatalytic reactions to evaluate enzymes in TX016",
}

# labware settings, fill accordingly
tipType1 = "opentrons_flex_96_tiprack_1000ul"
tipLoc1 = "C3"
tipType2 = "opentrons_flex_96_tiprack_200ul"
tipLoc2 = "B3"
hsModName = "heaterShakerModuleV1"
hsAdapter = "opentrons_96_deep_well_adapter"
hsPlate = "nest_96_wellplate_2ml_deep"
holder1Name = "opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical"
holder1Loc = "A2"
holder2Name = "opentrons_24_tuberack_nest_2ml_snapcap"
holder2Loc = "B2"


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
        instrument_name="flex_8channel_1000",
        mount="right",
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
        module_name=hsModName,
        location="D1"
    )

    # load the heater shaker combo
    hs_combo = hs_mod.load_labware(
        "opentrons_96_deep_well_adapter_nest_wellplate_2ml_deep"
    )

    # load holder 1
    holder1 = protocol.load_labware(
        load_name=holder1Name,
        location=holder1Loc
    )

    # load holder 2
    holder2 = protocol.load_labware(
        load_name=holder2Name,
        location=holder2Loc
    )

    # close latch for hs_mod
    hs_mod.close_labware_latch()

    # load NADPH/NADH into wells. Holder2[A1][B1]
    for j in range(2):
        pipetteS.pick_up_tip()
        for i in range(40):
            pipetteS.transfer(
                volume=5,
                source=holder2.wells()[j],
                dest=hs_combo.wells()[i],
                new_tip="never",
                blow_out=True,
                blowout_location="destination well"
            )
        # trash tip between liquids
        pipetteS.drop_tip()

    # load GDH into wells. Holder1[A1]
    pipetteS.pick_up_tip()
    for i in range(40):
        pipetteS.transfer(
            volume=50,
            source=holder1.wells()[0],
            dest=hs_combo.wells()[i],
            new_tip="never",
            blow_out=True,
            blowout_location="destination well"
        )
    pipetteS.drop_tip()

    # load glucose into wells. Holder2[C1]
    pipetteS.pick_up_tip()
    for i in range(40):
        pipetteS.transfer(
            volume=10,
            source=holder2.wells()[2],
            dest=hs_combo.wells()[i],
            new_tip="never",
            blow_out=True,
            blowout_location="destination well"
        )
    pipetteS.drop_tip()

    # load enzyme 1 into wells. Holder1[B1]
    pipetteS.pick_up_tip()
    for i in range(10):
        pipetteS.transfer(
            volume=50,
            source=holder1.wells()[1],
            dest=hs_combo.wells()[i],
            new_tip="never",
            blow_out=True,
            blowout_location="destination well"
        )
    pipetteS.drop_tip()

    # load enzyme 2 into wells. Holder1[C1]
    pipetteS.pick_up_tip()
    for i in range(10):
        pipetteS.transfer(
            volume=50,
            source=holder1.wells()[2],
            dest=hs_combo.wells()[i + 10],
            new_tip="never",
            blow_out=True,
            blowout_location="destination well"
        )
    pipetteS.drop_tip()

    # load enzyme 3 into wells. Holder1[A2]
    pipetteS.pick_up_tip()
    for i in range(10):
        pipetteS.transfer(
            volume=50,
            source=holder1.wells()[3],
            dest=hs_combo.wells()[i + 20],
            new_tip="never",
            blow_out=True,
            blowout_location="destination well"
        )
    pipetteS.drop_tip()

    # load enzyme 4 into wells. Holder1[B2]
    pipetteS.pick_up_tip()
    for i in range(10):
        pipetteS.transfer(
            volume=50,
            source=holder1.wells()[4],
            dest=hs_combo.wells()[i + 30],
            new_tip="never",
            blow_out=True,
            blowout_location="destination well"
        )
    pipetteS.drop_tip()

    # load buffer into wells. Holder1[A3]
    pipetteS.pick_up_tip(tipRack1)
    for i in range(40):
        pipetteS.transfer(
            volume=375,
            source=holder1.wells()[6],
            dest=hs_combo.wells()[i],
            new_tip="never",
            blow_out=True,
            blowout_location="destination well"
        )
    pipetteS.drop_tip()

    # load substrate into wells. Holder2[D1]+
    for m in range(10):
        for n in range(4):
            pipetteS.transfer(
                volume=5,
                source=holder2.wells()[n + 3],
                dest=hs_combo.wells()[m + 10 * n],
                mix_before=(3, 50),
                new_tip="always",
                touch_tip=True,
                blow_out=True
            )

    # wait for membrane
    protocol.delay(minutes=5)

    # start heater shaker
    hs_mod.set_and_wait_for_shake_speed(200)
    hs_mod.set_and_wait_for_temperature(37)
