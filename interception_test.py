import interception

interception.move_to(960, 540)

with interception.hold_key("ctrl"):
    interception.press("v")

interception.click(120, 160, button="right", delay=1)