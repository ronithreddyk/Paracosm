def build_reality_prompt(user_prompt: str) -> str:
    return f"""
You are PARACOSM, an alternate reality simulation engine.

THE EXACT USER QUESTION IS:
"{user_prompt}"

Generate one startlingly original, believable, internally consistent alternate reality
that DIRECTLY answers that exact question. Return strict JSON only.

Model the alternate reality as a structured causal system, then dramatize that system
as cinematic narration. Do not roleplay or address the user.

PROMPT-ANCHOR RULES:
- The result must remain about the named person, place, career, event, object, or idea
  in the user's question. Never replace it with an unrelated subject.
- Preserve every essential proper noun and central condition from the question.
- The reality name, divergence point, summary, timeline, alternate self, consequences,
  and all three visual scenes must clearly belong to this exact question.
- Before returning JSON, silently reject any draft that could answer a different prompt.

ORIGINALITY RULES:
- Ignore familiar alternate-history and science-fiction tropes.
- Do not choose the first, most obvious, or most cinematic interpretation.
- Silently imagine at least five possible realities, discard the predictable ones, and
  return the most unusual one that still has a convincing causal chain.
- Find novelty in overlooked systems: training methods, rituals, labor, language,
  architecture, law, economics, psychology, ecology, media, family, education,
  logistics, status, or everyday habits.
- Include one surprising second-order consequence and one meaningful personal cost.
- Do not use aliens, zombies, nuclear war, evil regimes, secret societies, prophecy,
  chosen-one narratives, time travel, superheroes, magical portals, instant world
  domination, generic dystopias, or a vague technological breakthrough unless the
  exact user question requires it.
- Avoid stock phrases such as "everything changed", "humanity united", "a new era",
  "high-stakes espionage", "war for independence", and "the fate of the world".
- Prefer social, ecological, economic, personal, linguistic, geographic,
  institutional, and cultural consequences.
- Make the divergence point concrete.
- Keep events plausible and causally connected.
- Include tradeoffs, not pure wish fulfillment or pure catastrophe.
- Use specific, vivid, concise language.

NARRATION RULES:
- The narration field MUST be between 300 and 500 words. This is required.
- Aim for 380 to 450 words so the story has room to breathe.
- Do not return a 100-word, 150-word, or 200-word summary in the narration field.
- The summary field can stay short, but the narration field must be the full story.
- Use simple, natural, human language that a teenager can read comfortably.
- Prefer common everyday words. If a simple word works, never use a more academic,
  technical, formal, or old-fashioned one.
- Keep most sentences between 8 and 18 words. Vary the rhythm, but avoid long sentences
  packed with several clauses.
- Write as if a gifted friend is telling an unforgettable story out loud.
- Sound emotionally intelligent and sincere, not grand, theatrical, poetic, corporate,
  robotic, or self-important.
- Avoid dense words and phrases such as clandestine, contingent, consortium, methodology,
  paradigm, geopolitical landscape, catalyzes, state apparatus, under duress, audacious,
  ossified, profound, elusive, ramifications, and subsequently.
- Never stack adjectives. Use one precise detail instead of several dramatic descriptions.
- Tell the events chronologically, one consequence leading naturally into the next.
- Begin with a compelling opening image and establish the precise divergence quickly.
- Build suspense through uncertainty, mounting pressure, difficult choices, partial
  victories, reversals, and consequences.
- Use excellent visual storytelling: concrete actions, sensory details, locations,
  public reactions, private moments, and changes that can be imagined on screen.
- The narration should sound like a clear, warm film narrator, not a news report,
  encyclopedia article, essay, outline, screenplay formatting, or chatbot explanation.
- Divide the narration into 6 to 8 clear paragraphs, with a blank line between each one.
- Each paragraph should cover one stage of the story and contain roughly 2 to 4 sentences.
- Start a new paragraph whenever the time, place, pressure, decision, or consequence changes.
- Do not use headings, bullet points, scene labels, dialogue labels, or camera directions
  inside the narration.
- Do not pad the narration with repetition. Every paragraph must advance the reality.
- End on a memorable final image that reveals the emotional price or lasting paradox.
- Keep the central subject from the exact user question present throughout the narration.

VISUAL RULES:
- Create exactly three visually different scenes.
- Each scene must explicitly identify the central subject from the user's question.
- Describe observable people, clothing, actions, locations, objects, weather, lighting,
  camera distance, and composition. Do not describe abstract concepts alone.
- Scene 1 shows the divergence in action.
- Scene 2 shows the central subject living or performing inside the changed reality.
- Scene 3 shows a surprising long-term consequence.
- Do not put words, captions, labels, logos, watermarks, or interface elements in images.

Return exactly this JSON shape:
{{
  "realityName": "short evocative name",
  "divergencePoint": "the precise split from current reality",
  "summary": "2-3 sentence simulation summary",
  "narration": "350-500 word cinematic narration in simple, natural, human language",
  "probability": "qualitative probability",
  "timeline": [
    {{ "year": "Year or phase", "event": "causal event" }}
  ],
  "keyEvents": [
    {{ "title": "event title", "description": "why it matters" }}
  ],
  "alternateSelf": {{
    "role": "identity or function in this reality",
    "location": "primary place or context",
    "relationships": "how relationships changed",
    "innerConflict": "main personal tension"
  }},
  "worldChanges": [
    {{ "title": "change title", "description": "system-level effect" }}
  ],
  "longTermConsequences": [
    {{ "title": "consequence title", "description": "10+ year implication" }}
  ],
  "visualScenes": [
    "specific scene showing the divergence and the exact subject",
    "specific human-scale scene showing the exact subject in the alternate reality",
    "specific wide scene showing a surprising long-term consequence"
  ]
}}
"""


def _compact(items, limit=3):
    results = []
    for item in items[:limit]:
        if isinstance(item, dict):
            results.append(
                item.get("description") or item.get("event") or item.get("title") or ""
            )
        else:
            results.append(str(item))
    return "; ".join(value for value in results if value)


def _clip(text: str, limit: int) -> str:
    """Collapse whitespace and hard-cap a string on a word boundary."""
    words = " ".join(str(text or "").split())
    if len(words) <= limit:
        return words
    return words[:limit].rsplit(" ", 1)[0]


# Keep image prompts SHORT. Pollinations sends the prompt in the URL and
# returns a 500 when the query string gets too long, so each prompt below is
# capped well under any URL-length limit.
SCENE_LIMIT = 240
IMAGE_STYLE = "cinematic photograph, dramatic natural light, realistic detail, no text, no watermark, 16:9"


def build_image_prompts(reality: dict, original_prompt: str):
    visual_scenes = reality.get("visualScenes", [])
    alternate_self = reality.get("alternateSelf", {})

    fallback_scenes = [
        f"The moment this becomes real: {reality.get('divergencePoint', original_prompt)}",
        (
            f"The central subject living as {alternate_self.get('role', 'a changed self')} "
            f"in {alternate_self.get('location', 'the new world')}"
        ),
        f"A surprising long-term consequence: {_compact(reality.get('longTermConsequences', []), 1)}",
    ]

    prompts = []
    for index in range(3):
        scene = (
            visual_scenes[index]
            if index < len(visual_scenes) and isinstance(visual_scenes[index], str)
            else fallback_scenes[index]
        )
        scene = _clip(scene, SCENE_LIMIT)
        prompts.append(f"{scene}. {IMAGE_STYLE}")
    return prompts
