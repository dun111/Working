# The story route, in one place.
# The hint line on the maps, the F9 chapter jumps and EXTRAS > CHAPTERS all read
# from here, so a change to the order of the story only needs making once.
#
# Each chapter is (steps, extra):
#   steps: [(flags, hint)] in order. The hint shows until all its flags are on.
#   extra: flags a chapter jump also switches on (doors, items) that have no hint.
# A chapter jump to stage N turns on every flag in the chapters before it.

init -10 python:
    ROUTE_PART1 = [
        ([(["c1_talked_fedora"], "Carriage 1: talk to Fedora.")],
         ["door_c2_open"]),
        ([(["c2_talked_eduard", "c2_talked_shunyu"], "Carriage 2: talk to Eduard and Shunyu.")],
         []),
        ([(["c3_talked_kimmy", "c3_talked_himmel", "c3_talked_sebastian", "c3_talked_misha"],
           "Carriage 3: talk to Sebastian, and everyone in Cabins 1 and 2.")],
         ["door_c4_open"]),
        ([(["c4_talked_agatha", "c4_talked_ichora"], "Carriage 4: meet the staff.")],
         ["has_key"]),
        ([(["c5_talked_pattison", "c5_talked_alexander"], "Carriage 5: talk to Pattison and Alexander.")],
         []),
    ]
    ROUTE_PART1_END = "Go through the door at the end of Carriage 5."

    ROUTE_PART2 = [
        # Waking up in Carriage 1 again.
        ([], ["door_c2_open_loop"]),
        # The crime scene.
        ([(["c2_p2_found_body"], "Carriage 2: look at the second table."),
          (["c2_p2_reinterviewed_eduard", "c2_p2_reinterviewed_agatha"], "Carriage 2: question Eduard and Agatha.")],
         ["clue_tile_mismatch", "clue_body_moved"]),
        # Carriage 3, first visit.
        ([(["clue_drug_wrapper"], "Carriage 3: look in Cabin 1."),
          (["kimmy_reinterviewed"], "Carriage 3: ask Kimmy (Cabin 1) about the wrapper."),
          (["himmel_reinterviewed"], "Carriage 3: confront Himmel in the corridor.")],
         ["himmel_reinterviewed"]),
        # The mail room, then back to Carriage 3.
        ([(["alexander_reinterviewed", "pattison_reinterviewed"], "Carriage 5: question Alexander, then Pattison."),
          (["clue_hidden_tile"], "Back to Carriage 3: check the carpet in Cabin 2."),
          (["sebastian_reinterviewed", "misha_reinterviewed"], "Carriage 3: question Sebastian, and Misha in Cabin 2.")],
         ["clue_alexander_alibi", "c3_p2_returned"]),
    ]
    ROUTE_PART2_END = "Carriage 3: decide who did it."

    def route_flags(route):
        # One list of flags per chapter, for the chapter jumps.
        return [[f for flags, _hint in steps for f in flags] + list(extra) for steps, extra in route]

    def route_hint(route, done):
        for steps, _extra in route:
            for flags, hint in steps:
                if not all(getattr(store, f, False) for f in flags):
                    return hint
        return done

    def current_objective():
        if getattr(store, "in_loop", False):
            return route_hint(ROUTE_PART2, ROUTE_PART2_END)
        return route_hint(ROUTE_PART1, ROUTE_PART1_END)

    def chapter_stage(label):
        # The F9 chapter stage for a chapter's first label.
        for _name, target, stage in CHEAT_CHAPTERS:
            if target == label:
                return stage
        return 0
