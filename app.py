# adventure_game.py (Flask web edition)
# Purpose: A text-based treasure-hunting adventure game, reimagined as a
# browser-playable Flask web application, deployable on Render.
#
# The player explores a dark forest or a mysterious cave, makes a series
# of strategic decisions, and either finds the legendary treasure (win),
# makes a poor decision that ends the quest (lose), or restarts the
# adventure to try again.

import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "adventure-game-dev-secret-key")


# ---------------------------------------------------------------------------
# Game data: every scene, its narrative text, and the choices it leads to.
# Each "outcome" scene has a `result` key of "win" or "lose".
# ---------------------------------------------------------------------------
SCENES = {
    "choice": {
        "text": "Two paths lie before you: a {dark_forest} to the west, "
                "and a {mysterious_cave} to the north. Which will you choose, {name}?",
        "options": [
            {"label": "Enter the dark forest", "action": "forest"},
            {"label": "Enter the mysterious cave", "action": "cave"},
        ],
    },
    "forest": {
        "text": "You step into the dark forest. Towering trees block out the sun, "
                "and you hear the distant sound of rushing water. A narrow game trail "
                "splits in two: one path follows a river, the other leads to a "
                "massive old tree you could climb for a better view.",
        "options": [
            {"label": "Follow the river", "action": "forest_river"},
            {"label": "Climb the tree", "action": "forest_tree"},
        ],
    },
    "forest_river": {
        "text": "The river rushes fast and cold. Downstream, you spot a rickety "
                "rope bridge crossing to the far bank. The current itself looks "
                "tempting to swim across if you want to save time.",
        "options": [
            {"label": "Cross the rope bridge carefully", "action": "forest_river_bridge"},
            {"label": "Swim across the river", "action": "forest_river_swim"},
        ],
    },
    "forest_river_bridge": {
        "text": "You cross the swaying bridge one careful step at a time. On the "
                "far bank, half-buried in the mud, you find a weathered map case. "
                "Inside is a fragment of the treasure map! Following its markings, "
                "you uncover the entrance to the treasure vault hidden behind a "
                "waterfall. You found the legendary treasure!",
        "result": "win",
    },
    "forest_river_swim": {
        "text": "You dive in, but the current is far stronger than it looked. "
                "It sweeps you downstream, and you lose your pack, your supplies, "
                "and any hope of continuing the quest today. Your adventure ends here.",
        "result": "lose",
    },
    "forest_tree": {
        "text": "You climb higher and higher through the branches. From the top, "
                "you could scan the horizon for landmarks, or you could rest a while "
                "on a sturdy branch to catch your breath before deciding what's next.",
        "options": [
            {"label": "Scan the horizon from the treetop", "action": "forest_tree_scan"},
            {"label": "Rest on the branch", "action": "forest_tree_rest"},
        ],
    },
    "forest_tree_scan": {
        "text": "From the treetop, you spot a glint of gold near a distant rock "
                "formation shaped like a crown. You climb down and head straight "
                "for it, and beneath a slab of stone you uncover the treasure chest "
                "at last. You found the legendary treasure!",
        "result": "win",
    },
    "forest_tree_rest": {
        "text": "The branch is comfortable, maybe too comfortable. You doze off, "
                "and by the time you wake, night has fallen and a storm is rolling "
                "in. Soaked and disoriented, you have no choice but to turn back. "
                "Your adventure ends here.",
        "result": "lose",
    },
    "cave": {
        "text": "You step into the mouth of the cave. The air is cool and damp, "
                "and the darkness ahead is absolute. You have a torch in your bag, "
                "but lighting it means giving up the element of surprise if "
                "anything is watching from the dark.",
        "options": [
            {"label": "Light the torch", "action": "cave_torch"},
            {"label": "Proceed in the dark", "action": "cave_dark"},
        ],
    },
    "cave_torch": {
        "text": "The torchlight reveals two tunnels: one curving left, one curving "
                "right. Faint carvings on the wall seem to mark one of them.",
        "options": [
            {"label": "Take the left tunnel", "action": "cave_torch_left"},
            {"label": "Take the right tunnel", "action": "cave_torch_right"},
        ],
    },
    "cave_torch_left": {
        "text": "The left tunnel opens into a vast chamber glittering with gold "
                "coins and jeweled artifacts, exactly as the carvings promised. "
                "You found the legendary treasure!",
        "result": "win",
    },
    "cave_torch_right": {
        "text": "The right tunnel looks promising, until your foot catches a "
                "tripwire. A hidden rockslide seals the passage behind you, and "
                "your torch gutters out in the dust. Your adventure ends here.",
        "result": "lose",
    },
    "cave_dark": {
        "text": "You feel your way along the cold stone walls. Ahead, the "
                "passage forks. You can move carefully, testing each step, or "
                "rush ahead to make up for lost time.",
        "options": [
            {"label": "Proceed carefully, feeling the walls", "action": "cave_dark_careful"},
            {"label": "Rush ahead", "action": "cave_dark_rush"},
        ],
    },
    "cave_dark_careful": {
        "text": "Your careful hands find a hidden seam in the rock, a secret "
                "passage that opens into a moonlit grotto. There, on a stone "
                "pedestal, rests the treasure you've been seeking. "
                "You found the legendary treasure!",
        "result": "win",
    },
    "cave_dark_rush": {
        "text": "Rushing blindly in the dark was a mistake. The floor gives way "
                "beneath you, and you tumble into a deep pit with no way to "
                "climb back out in time. Your adventure ends here.",
        "result": "lose",
    },
}


def get_name():
    return session.get("name", "Explorer")


@app.route("/", methods=["GET"])
def index():
    """Task 1/2: Introduce the quest and ask for the player's name."""
    if session.get("name"):
        return redirect(url_for("scene", scene_id="choice"))
    return render_template("start.html")


@app.route("/start", methods=["POST"])
def start():
    """Task 2: Store the player's name and begin the game (start_game())."""
    name = request.form.get("player_name", "").strip()
    session["name"] = name if name else "Explorer"
    session["log"] = []
    return redirect(url_for("scene", scene_id="choice"))


@app.route("/scene/<scene_id>", methods=["GET"])
def scene(scene_id):
    """Render any scene (choice, forest_path(), cave_path(), or an ending)."""
    if not session.get("name"):
        return redirect(url_for("index"))

    if scene_id not in SCENES:
        return redirect(url_for("scene", scene_id="choice"))

    data = SCENES[scene_id]
    text = data["text"].format(
        name=get_name(),
        dark_forest="dark forest",
        mysterious_cave="mysterious cave",
    )

    log = session.get("log", [])
    log.append(text)
    session["log"] = log

    if "result" in data:
        return render_template(
            "result.html",
            name=get_name(),
            text=text,
            result=data["result"],
            log=log,
        )

    return render_template(
        "scene.html",
        name=get_name(),
        text=text,
        options=data["options"],
        log=log,
    )


@app.route("/restart", methods=["GET", "POST"])
def restart():
    """Task 5: Allow the player to restart the game after completion."""
    name = session.get("name")
    session.clear()
    if name:
        session["name"] = name
        session["log"] = []
        return redirect(url_for("scene", scene_id="choice"))
    return redirect(url_for("index"))


@app.route("/quit", methods=["POST"])
def quit_game():
    """Clear the session entirely and return to the name-entry screen."""
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
