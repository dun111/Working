# Saves from an older version can point back into script lines that have since
# moved. Every carriage map is a `call screen`, and a conversation started from
# it returns to the line after that call. If that line can't be found any more,
# Ren'Py would crash. Instead, send the player back to the carriage map they
# were on.

define config.return_not_found_label = "return_lost"

define HUB_LABELS = (
    "carriage_1_hub", "carriage_2_hub", "carriage_3_hub", "carriage_4_hub", "carriage_5_hub",
    "carriage_2_part2_hub", "c2_p2_investigation_hub", "carriage_3_part2_hub", "carriage_5_part2_hub",
)

# The last carriage map the player stood on.
default last_hub = None
# For saves made before last_hub existed: the map worked out from the scene
# the save was made in.
default resume_hub_guess = None

init python:
    # Scene label prefix -> the map it was opened from. Longest prefixes first.
    HUB_BY_PREFIX = [
        ("c2_p2_reinterview_", "c2_p2_investigation_hub"),
        ("c2_p2_investigation", "c2_p2_investigation_hub"),
        ("c2_p2_", "carriage_2_part2_hub"),
        ("c3_p2_", "carriage_3_part2_hub"),
        ("c5_p2_", "carriage_5_part2_hub"),
        ("c1_", "carriage_1_hub"),
        ("c2_", "carriage_2_hub"),
        ("c3_", "carriage_3_hub"),
        ("c4_", "carriage_4_hub"),
        ("c5_", "carriage_5_hub"),
    ]

    def _note_hub(name, abnormal):
        if name in HUB_LABELS:
            store.last_hub = name

    config.label_callbacks.append(_note_hub)

    def label_at(filename, line):
        # The label a script line sits under.
        best, best_line = None, -1
        for lab in renpy.get_all_labels():
            if lab.startswith("_"):
                continue
            node = renpy.game.script.lookup(lab)
            if node.filename == filename and best_line < node.linenumber <= line:
                best, best_line = lab, node.linenumber
        return best

    def hub_for_label(lab):
        if lab in HUB_LABELS:
            return lab
        for prefix, hub in HUB_BY_PREFIX:
            if lab and lab.startswith(prefix):
                return hub
        return None

    def _guess_hub_after_load():
        # This runs inside Ren'Py's own after-load label, so the line the save
        # was made on is the newest entry on the return stack that still exists.
        guess = None
        try:
            for name in reversed(renpy.game.context().return_stack):
                node = renpy.game.script.namemap.get(name)
                if node is not None and node.filename.startswith("game/"):
                    guess = hub_for_label(label_at(node.filename, node.linenumber))
                    break
        except Exception:
            guess = None
        store.resume_hub_guess = guess

    config.after_load_callbacks.append(_guess_hub_after_load)

    def hub_from_progress():
        # The carriage the current objective points to (see route.rpy).
        import re
        m = re.search(r"Carriage (\d)", current_objective())
        n = m.group(1) if m else "1"
        if not store.in_loop:
            return "carriage_%s_hub" % n
        if n == "2":
            return "c2_p2_investigation_hub" if store.c2_p2_found_body else "carriage_2_part2_hub"
        if n in ("3", "5"):
            return "carriage_%s_part2_hub" % n
        return "carriage_1_hub"

    def recovery_hub():
        return store.last_hub or store.resume_hub_guess or hub_from_progress()

label return_lost:
    python:
        for _s in ("window_view", "fullscreen_pop", "cast_peek", "clue_popup"):
            renpy.hide_screen(_s)
    $ renpy.jump(recovery_hub())
