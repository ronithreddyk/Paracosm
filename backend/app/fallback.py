def fallback_reality(prompt: str) -> dict:
    lower_prompt = prompt.lower()

    if any(word in lower_prompt for word in ("moon", "earth", "ocean")):
        name = "The Tidal Century"
        divergence = (
            "A second moon settles into a stable orbit and reshapes tides, coastlines, "
            "calendars, agriculture, and settlement."
        )
        summary = (
            "The greatest changes arrive through water, navigation, work schedules, and "
            "public infrastructure rather than spectacle. Coastal engineering becomes a "
            "permanent civic duty beneath brighter and more complicated nights."
        )
    else:
        name = "The Adjacent Thread"
        divergence = (
            "One decision changes the available mentors, peer group, and first serious constraint."
        )
        summary = (
            "The alternate path changes what is easy, not only what is possible. Identity "
            "adapts to new incentives while familiar strengths reappear in unfamiliar forms."
        )

    return {
        "realityName": name,
        "divergencePoint": divergence,
        "summary": summary,
        "narration": (
            f"It begins without thunder or spectacle. The question is suddenly no longer "
            f"hypothetical: {prompt}. At first, only a few people understand what has shifted. "
            f"The earliest evidence appears in ordinary places, where a familiar routine now "
            f"produces an unfamiliar result. The central figure moves through that first day "
            f"believing the change can still be contained, explained, or reversed.\n\n"
            f"By the end of the first year, the divergence has acquired a schedule, a budget, "
            f"and a waiting list. Institutions that once dismissed it begin redesigning their "
            f"rules around it. Friends and rivals adapt faster than expected. What looked like "
            f"an advantage becomes a source of pressure: every success increases the number of "
            f"people depending on the new path, while every mistake is treated as proof that the "
            f"old reality was safer. In private, the central figure starts measuring life by "
            f"what can no longer be returned to.\n\n"
            f"Three years after the split, imitation changes the world more than the original "
            f"event did. Schools teach techniques that did not exist before. New professions "
            f"appear around maintenance, interpretation, and control. Language develops compact "
            f"phrases for experiences that once sounded impossible. Then comes the reversal: a "
            f"hidden cost surfaces inside the very system built to protect the new reality. The "
            f"central figure must choose between preserving the public success and admitting "
            f"that its foundation is becoming unstable.\n\n"
            f"The choice does not produce a clean victory. It creates a smaller, stranger future. "
            f"Some institutions collapse; others become more humane because they are forced to "
            f"abandon certainty. Relationships survive only when they can accept that the person "
            f"who began this path no longer exists in the same form. Years later, the change is "
            f"everywhere and almost invisible, embedded in architecture, etiquette, work, and "
            f"memory. In the final image, the central figure stands inside a world that once "
            f"belonged only to imagination, watching strangers perform an everyday ritual born "
            f"from that first impossible moment. A child repeats the gesture without knowing "
            f"where it came from, and the crowd passes without looking up. The world remembers "
            f"the achievement. Only one person remembers the life it replaced."
        ),
        "probability": "Moderate",
        "timeline": [
            {"year": "Divergence", "event": divergence},
            {
                "year": "Year 1",
                "event": "Initial gains are balanced by hidden costs and practical limits.",
            },
            {
                "year": "Year 3",
                "event": "New routines and relationships become stronger than the original plan.",
            },
            {
                "year": "Year 7",
                "event": "The alternate reality develops its own stable norms.",
            },
            {
                "year": "Year 15",
                "event": "Long-range effects become visible in identity, place, and obligation.",
            },
        ],
        "keyEvents": [
            {
                "title": "First constraint",
                "description": "A practical limit makes the new reality believable.",
            },
            {
                "title": "Network shift",
                "description": "New people and institutions reward different traits.",
            },
            {
                "title": "Cultural drift",
                "description": "Repeated choices create a different common sense.",
            },
        ],
        "alternateSelf": {
            "role": "A recognizable self shaped by different pressures",
            "location": "A setting formed by the first major consequence",
            "relationships": "Some bonds deepen while others fade through changed context",
            "innerConflict": "Growth feels inseparable from what had to be surrendered",
        },
        "worldChanges": [
            {
                "title": "Incentives change",
                "description": "Status moves toward the skills this reality needs most.",
            },
            {
                "title": "Places reorganize",
                "description": "Homes, work, and public space adapt around the new constraint.",
            },
            {
                "title": "Language absorbs it",
                "description": "People create shorthand for once-unfamiliar experiences.",
            },
        ],
        "longTermConsequences": [
            {
                "title": "Identity becomes local",
                "description": "Everyday systems shape the alternate self.",
            },
            {
                "title": "Tradeoffs harden",
                "description": "Advantages and sacrifices both become difficult to reverse.",
            },
            {
                "title": "A new normal forms",
                "description": "Future choices begin from the alternate reality's assumptions.",
            },
        ],
        "visualScenes": [
            (
                f"A grounded documentary-style scene showing the exact moment this question "
                f"becomes real: {prompt}. The central subject is clearly visible and actively "
                f"causes the divergence."
            ),
            (
                f"A close human-scale scene of the central subject from '{prompt}' living the "
                f"changed daily reality, surrounded by specific tools, clothing, people, and "
                f"architecture created by that choice."
            ),
            (
                f"A wide scene set fifteen years after '{prompt}', showing one surprising "
                f"social or cultural consequence through visible human activity rather than "
                f"abstract symbolism."
            ),
        ],
    }
