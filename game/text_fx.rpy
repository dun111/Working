# ==============================================================================
# DEPARTURE AT 4:00  -  text_fx.rpy
# Effects for dialogue, used inside a line in script.rpy:
#
#   l "{shake}Shunyu? Shunyu!!{/shake} Hey, wake up."     shock
#   h "{tremble}O-oh my god dear!{/tremble}"               fear / stammering
#   s "{wave}JACKKKPOTTTTTTT!{/wave}"                       sing-song, creepy voices
#   l "is that {scream}GLASS{/scream}"                      big, red, shaking
#   d "{whisper}Thank you for boarding...{/whisper}"        faint, quiet
#   u "{glitch}Not me. Him.{/glitch}"                       the voice in the dark
#   l "{big}It was you.{/big}"                              bigger, for a reveal
#
# Only the look changes - the words stay as written. Everything that moves is
# switched off with Settings > Accessibility > REDUCE MOTION.
# Settings > Text > TEXT EFFECTS: FULL / STILL (colour and size, no movement) / OFF.
# ==============================================================================

# Shader tags (shake, wave...) need text shaders switched on. "typewriter"
# shows text the same way Ren'Py normally does.
define config.default_textshader = "typewriter"

init python:
    def _fx_shader(shader, contents):
        if persistent.reduce_motion or persistent.text_fx != "full":
            return contents
        return [(renpy.TEXT_TAG, u"shader=" + shader)] + contents + [(renpy.TEXT_TAG, u"/shader")]

    def _fx_wrap(open_tags, close_tags, contents):
        if persistent.text_fx == "off":
            return contents
        return ([(renpy.TEXT_TAG, t) for t in open_tags] + contents +
                [(renpy.TEXT_TAG, t) for t in close_tags])

    def fx_shake(tag, argument, contents):
        return _fx_shader(u"jitter:u__jitter=3.0, 3.0", contents)

    def fx_tremble(tag, argument, contents):
        return _fx_shader(u"jitter:u__jitter=1.2, 1.2", contents)

    def fx_wave(tag, argument, contents):
        return _fx_shader(u"wave:u__amplitude=5.0:u__frequency=2.0:u__wavelength=20.0", contents)

    def fx_scream(tag, argument, contents):
        inner = _fx_shader(u"jitter:u__jitter=4.0, 4.0", contents)
        return _fx_wrap([u"size=+14", u"b", u"color=#ff5a4a"], [u"/color", u"/b", u"/size"], inner)

    def fx_whisper(tag, argument, contents):
        return _fx_wrap([u"alpha=0.6", u"size=-4", u"i"], [u"/i", u"/size", u"/alpha"], contents)

    def fx_glitch(tag, argument, contents):
        inner = _fx_shader(u"jitter:u__jitter=6.0, 0.8", contents)
        return _fx_wrap([u"color=#e8a49c"], [u"/color"], inner)

    def fx_big(tag, argument, contents):
        return _fx_wrap([u"size=+12", u"b"], [u"/b", u"/size"], contents)

    config.custom_text_tags["shake"] = fx_shake
    config.custom_text_tags["tremble"] = fx_tremble
    config.custom_text_tags["wave"] = fx_wave
    config.custom_text_tags["scream"] = fx_scream
    config.custom_text_tags["whisper"] = fx_whisper
    config.custom_text_tags["glitch"] = fx_glitch
    config.custom_text_tags["big"] = fx_big
