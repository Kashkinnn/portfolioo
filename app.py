import os
from pathlib import Path
from urllib.parse import quote

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont


st.set_page_config(
    page_title="Joel | Portfolio",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAME = "Joel C. Coyoca Jr."
PROGRAM = "BSCS"
YEAR = "3rd Year"
SECTION = "F1"
GITHUB = "https://github.com/Kashkinnn"
EMAIL = "joel.coyoca@cit.edu"

PALETTES = {
    "Neon Rain": {
        "BG": "#07060d",
        "SURFACE": "#100c1c",
        "TEXT": "#ece9f8",
        "MUTED": "#8f89b0",
        "ACCENT": "#ff2e88",
        "ACCENT2": "#00e5ff",
        "ACCENT3": "#9b5cff",
        "ACCENT4": "#ffd23f",
        "BORDER": "rgba(255,46,136,0.28)",
        "RGB": (255, 46, 136),
        "RGB2": (0, 229, 255),
    },
    "Amber Noir": {
        "BG": "#0a0805",
        "SURFACE": "#15110a",
        "TEXT": "#f3eadb",
        "MUTED": "#a09279",
        "ACCENT": "#ffb000",
        "ACCENT2": "#2ad4c0",
        "ACCENT3": "#ff6b3d",
        "ACCENT4": "#f5e6a8",
        "BORDER": "rgba(255,176,0,0.28)",
        "RGB": (255, 176, 0),
        "RGB2": (42, 212, 192),
    },
    "Crimson Alley": {
        "BG": "#0a0506",
        "SURFACE": "#150a0d",
        "TEXT": "#f4e8ea",
        "MUTED": "#a2838b",
        "ACCENT": "#ff2a3d",
        "ACCENT2": "#7df9ff",
        "ACCENT3": "#ff8a5c",
        "ACCENT4": "#ffe08a",
        "BORDER": "rgba(255,42,61,0.28)",
        "RGB": (255, 42, 61),
        "RGB2": (125, 249, 255),
    },
}

defaults = {
    "palette": "Neon Rain",
    "rain": True,
    "scanlines": True,
    "endorsements": 0,
    "messages_sent": 0,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

P = PALETTES[st.session_state.palette]
STYLE_FILE = Path(__file__).parent / "style.css"


def paint(css):
    for token, value in {
        "__BG__": P["BG"],
        "__SURFACE__": P["SURFACE"],
        "__TEXT__": P["TEXT"],
        "__MUTED__": P["MUTED"],
        "__A__": P["ACCENT"],
        "__B__": P["ACCENT2"],
        "__ACCENT4__": P["ACCENT4"],
        "__BORDER__": P["BORDER"],
    }.items():
        css = css.replace(token, value)
    return css


st.markdown(
    f"<style>{paint(STYLE_FILE.read_text(encoding='utf-8'))}</style>",
    unsafe_allow_html=True,
)

toggles = []
if not st.session_state.rain:
    toggles.append("--rain-display:none")
if not st.session_state.scanlines:
    toggles.append("--scan-display:none")
if toggles:
    st.markdown(
        f"<style>:root{{{';'.join(toggles)}}}</style>",
        unsafe_allow_html=True,
    )


def html(block):
    st.markdown(
        "".join(line.strip() for line in block.splitlines()),
        unsafe_allow_html=True,
    )


@st.cache_data
def stand_in_portrait(rgb_a, rgb_b, width=640, height=780):
    y, x = np.mgrid[0:height, 0:width]
    base = np.zeros((height, width, 3), dtype=np.float32)
    glow_a = np.exp(-(((x - width * 0.25) / 260) ** 2 + ((y - height * 0.2) / 320) ** 2))
    glow_b = np.exp(-(((x - width * 0.85) / 280) ** 2 + ((y - height * 0.9) / 340) ** 2))
    for i in range(3):
        base[..., i] = 8 + glow_a * rgb_a[i] * 0.55 + glow_b * rgb_b[i] * 0.45
    blinds = (((x * 0.55 + y) // 26) % 2 == 0) & (y < height * 0.62)
    light = np.exp(-((x - width * 0.3) / 330) ** 2)
    for i in range(3):
        base[..., i] += blinds * light * rgb_a[i] * 0.22
    image = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGB")
    draw = ImageDraw.Draw(image)
    cx = width // 2
    draw.ellipse([cx - 108, 170, cx + 108, 410], fill=(3, 3, 8))
    draw.ellipse([cx - 290, 450, cx + 290, 1000], fill=(3, 3, 8))
    draw.rectangle([cx - 52, 380, cx + 52, 480], fill=(3, 3, 8))
    draw.arc([cx - 112, 166, cx + 112, 414], 200, 340, fill=tuple(rgb_b), width=3)
    draw.arc([cx - 294, 446, cx + 294, 1004], 205, 335, fill=tuple(rgb_a), width=3)
    try:
        big = ImageFont.load_default(size=64)
        small = ImageFont.load_default(size=22)
    except TypeError:
        big = small = ImageFont.load_default()
    draw.text((36, height - 130), "JC", fill=tuple(rgb_a), font=big)
    draw.text((36, height - 52), "PHOTO STAND-IN  //  SUBJECT: JOEL", fill=tuple(rgb_b), font=small)
    return image


SKILLS = pd.DataFrame(
    [
        {"Skill": "Python", "Category": "Languages", "Level": 75},
        {"Skill": "Java", "Category": "Languages", "Level": 65},
        {"Skill": "SQL", "Category": "Languages", "Level": 60},
        {"Skill": "C#", "Category": "Languages", "Level": 60},
        {"Skill": "Bash", "Category": "Languages", "Level": 60},
        {"Skill": "HTML / CSS", "Category": "Web", "Level": 60},
        {"Skill": "Streamlit", "Category": "Frameworks", "Level": 65},
        {"Skill": "Blazor", "Category": "Frameworks", "Level": 55},
        {"Skill": "Git / GitHub", "Category": "Tools", "Level": 65},
        {"Skill": "Docker", "Category": "Tools", "Level": 65},
        {"Skill": "Linux", "Category": "Tools", "Level": 60},
    ]
)

MILESTONES = pd.DataFrame(
    [
        {"Year": "2024", "Milestone": "Started the BSCS program", "Why it mattered": "Turned curiosity into a plan"},
        {"Year": "2025", "Milestone": "Dug into Linux and networking", "Why it mattered": "Saw how systems connect"},
        {"Year": "2025", "Milestone": "Built my first homelab", "Why it mattered": "Learned how servers work"},
        {"Year": "2026", "Milestone": "Hosted a local AI chatbot", "Why it mattered": "Got hands-on with local AI"},
        {"Year": "2026", "Milestone": "Shipped this Streamlit portfolio", "Why it mattered": "Put everything in one place"},
    ]
)

PROJECTS = [
    {
        "number": "CASE 001",
        "name": "Homelab",
        "description": "A personalized home server built for self-hosting services and experimenting with how servers work.",
        "role": "Developer / Sysadmin",
        "tools": ["Debian", "Bash", "Docker"],
        "outcome": "Working server running a local streaming service and a toolkit of self-hosted tools.",
        "url": "",
    },
    {
        "number": "CASE 002",
        "name": "Archive Of Things",
        "description": "A localized archive for storing and browsing a personal collection of things.",
        "role": "Full-Stack Developer",
        "tools": ["Blazor", "Docker", "C#"],
        "outcome": "Containerized archive app running locally with stored data.",
        "url": "",
    },
    {
        "number": "CASE 003",
        "name": "PIM (Personal Inferencing Machine)",
        "description": "A locally hosted conversational assistant prototype for answering a defined set of questions.",
        "role": "Developer",
        "tools": ["Bash", "Qwen", "Ollama"],
        "outcome": "Prototype that answers a fixed question set using a local model.",
        "url": "",
    },
]

PROFILE_TEXT = (
    f"{NAME}\n{PROGRAM} · {YEAR} · Section {SECTION}\n"
    "Computer science student exploring software development, homelabs, networking, and local AI.\n"
    f"GitHub: {GITHUB}\nEmail: {EMAIL}\n"
)


with st.sidebar:
    st.markdown("## JC ▮ NOIR")
    st.caption("PERSONAL PORTFOLIO // FILE #349")
    st.divider()

    st.markdown(f"**{NAME}**")
    st.caption(f"{PROGRAM} · {YEAR} · Section {SECTION}")

    st.selectbox("Palette", list(PALETTES.keys()), key="palette")
    st.checkbox("Rain overlay", key="rain")
    st.checkbox("CRT scanlines", key="scanlines")

    st.divider()
    if st.button("Endorse this portfolio", use_container_width=True):
        st.session_state.endorsements += 1
        st.toast("Endorsement logged. The city remembers.", icon="🌃")
    st.caption(f"Endorsements this session: {st.session_state.endorsements}")

    st.download_button(
        "Download profile",
        PROFILE_TEXT,
        file_name="joel_profile.txt",
        use_container_width=True,
    )
    st.link_button("GitHub ↗", GITHUB, use_container_width=True)


hero_left, hero_right = st.columns([1.35, 0.65], gap="large")

with hero_left:
    html(
        f"""
        <div class="eyebrow">{PROGRAM} · {YEAR} · Section {SECTION}</div>
        <div class="hero-title">
            Hi, I'm Joel.<br>
            <span class="hero-accent">I build things</span><br>
            after dark.
        </div>
        <div class="hero-copy">
            I'm a computer science student exploring software development,
            networking, and the systems behind the tools we use every day.
            I learn by building, experimenting, and improving real projects.
            <br>
            <br>
            AND I LOVE NEO NOIR.
        </div>
        """
    )

    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Program", PROGRAM)
    m2.metric("Projects", len(PROJECTS))
    m3.metric("Skills", len(SKILLS))
    m4.metric("Endorsed", st.session_state.endorsements)

with hero_right:
    photo_path = next(
        (
            str(Path(__file__).parent / name)
            for name in ["photo.jpeg", "photo.jpg", "photo.png"]
            if (Path(__file__).parent / name).exists()
        ),
        None,
    )
    if photo_path:
        st.image(photo_path, caption=f"{NAME} // {PROGRAM} · {SECTION}", use_container_width=True)
    else:
        st.image(
            stand_in_portrait(P["RGB"], P["RGB2"]),
            caption="Photo stand-in // add photo.jpeg to replace",
            use_container_width=True,
        )

html('<div class="divider-line"></div>')

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    html('<div class="section-label">Currently exploring</div>')
    html(
        """
        <span class="pill">Python</span>
        <span class="pill">C# / Blazor</span>
        <span class="pill">Docker</span>
        <span class="pill">Linux</span>
        <span class="pill">Homelab</span>
        <span class="pill">Networking</span>
        <span class="pill">Local AI</span>
        """
    )

with right:
    html(
        """
        <div class="panel">
            <div class="eyebrow">A little about me</div>
            <h3>Curious by default.</h3>
            <p class="muted">
                I enjoy understanding how things work, trying new technologies,
                and turning ideas into practical projects. Outside coding,
                I usually read comics or play games, getting lost in cyberpunk like a true gonk,
                or learning something new.
            </p>
        </div>
        """
    )


tab_about, tab_skills, tab_projects, tab_contact = st.tabs(
    ["Autobiography", "Skills", "Projects", "Contact"]
)


with tab_about:
    st.subheader("A work in progress — in the best way.")

    col1, col2 = st.columns([1.3, 0.7], gap="large")

    with col1:
        chapter = st.radio(
            "Chapter",
            ["Background", "Education", "Interests"],
            horizontal=True,
        )

        if chapter == "Background":
            st.markdown(
                """
                I don't have one fixed lane yet.
                I'm interested in both the software people interact with and
                the infrastructure that makes it run.

                Lately, I've been trying to get deeper into networking because
                I enjoy understanding how systems connect. Running my own
                homelab is where that curiosity turns into practice.

                My approach is simple: build something, learn what I don't know,
                and improve it one iteration at a time.
                """
            )
        elif chapter == "Education":
            st.markdown(
                f"""
                I'm pursuing a **{PROGRAM}** as a **{YEAR}** student in
                **Section {SECTION}**. Coursework gives me the foundations,
                and personal projects are where I test whether I actually
                understand them.

                Right now my focus is Python, C#, Docker, Linux, and how
                networks move data from one place to another.
                """
            )
        else:
            st.markdown(
                """
                I enjoy roguelikes and deckbuilders, especially **Balatro**
                and **Slay the Spire**. Both reward planning, adapting to
                bad luck, and finding the combination that quietly breaks
                the game open.

                That mindset carries over into how I debug and design software.

                I'm also drawn to the neo-noir look, partly because I recently
                got back into cyberpunk. It's the reason this whole portfolio
                looks the way it does.
                """
            )

    with col2:
        html(
            f"""
            <div class="panel">
                <div class="eyebrow">Quick profile</div>
                <p><b>Name</b><br>{NAME}</p>
                <p><b>Program</b><br>{PROGRAM} · {YEAR}</p>
                <p><b>Section</b><br>{SECTION}</p>
                <p><b>Interests</b><br>Coding, homelabs, networking, games, cyberpunk</p>
                <p><b>Approach</b><br>Hands-on learning</p>
            </div>
            """
        )

    html('<div class="section-label">Milestones</div>')

    full_timeline = st.checkbox("Show full timeline", value=True)
    shown = MILESTONES if full_timeline else MILESTONES.tail(2)

    tl_col, table_col = st.columns([1, 1], gap="large")

    with tl_col:
        for _, row in shown.iterrows():
            html(
                f"""
                <div class="timeline-item">
                    <div class="timeline-year">{row["Year"]}</div>
                    <div><b>{row["Milestone"]}</b></div>
                    <div class="muted">{row["Why it mattered"]}</div>
                </div>
                """
            )

    with table_col:
        st.table(shown.set_index("Year"))

    st.markdown("### What I'm aiming for")

    goals = st.columns(3)

    goal_data = [
        ("01 / BUILD", "Useful software", "Create practical tools that solve real problems."),
        ("02 / UNDERSTAND", "Systems and networks", "Understand how applications and infrastructure connect."),
        ("03 / IMPROVE", "Keep iterating", "Turn experiments into better engineering habits."),
    ]

    for col, (label, title, description) in zip(goals, goal_data):
        with col:
            html(
                f"""
                <div class="panel">
                    <div class="eyebrow">{label}</div>
                    <h4>{title}</h4>
                    <p class="muted">{description}</p>
                </div>
                """
            )


with tab_skills:
    st.subheader("Tools I work with")
    st.caption("Levels are self-assessed, not formal test scores.")

    all_categories = SKILLS["Category"].unique().tolist()

    f1, f2, f3 = st.columns([1.4, 1, 1], gap="large")
    with f1:
        categories = st.multiselect(
            "Filter skill categories",
            options=all_categories,
            default=all_categories,
        )
    with f2:
        min_level = st.slider("Minimum level", 0, 100, 0, step=5)
    with f3:
        view = st.radio("Chart view", ["By skill", "By category"], horizontal=True)

    show_chart = st.checkbox("Show chart", value=True)

    filtered = SKILLS[
        SKILLS["Category"].isin(categories) & (SKILLS["Level"] >= min_level)
    ]

    if filtered.empty:
        st.info("No skills match these filters.")
    else:
        k1, k2, k3 = st.columns(3)
        k1.metric("Skills shown", len(filtered))
        k2.metric("Average level", f"{filtered['Level'].mean():.0f}%")
        top = filtered.loc[filtered["Level"].idxmax()]
        k3.metric("Strongest", top["Skill"])

        skill_col, chart_col = st.columns(2, gap="large")

        with skill_col:
            st.markdown("#### Skill overview")
            for _, skill in filtered.iterrows():
                st.markdown(f"**{skill['Skill']}** — {skill['Level']}%")
                st.progress(int(skill["Level"]) / 100)

        with chart_col:
            st.markdown("#### Compare skills")

            if show_chart:
                if view == "By skill":
                    chart_df = filtered.rename(columns={"Skill": "Label"})
                else:
                    chart_df = (
                        filtered.groupby("Category", as_index=False)["Level"]
                        .mean()
                        .round(1)
                        .rename(columns={"Category": "Label"})
                    )
                    chart_df["Category"] = chart_df["Label"]

                spec = {
                    "background": "transparent",
                    "mark": {"type": "bar", "cornerRadiusEnd": 2},
                    "encoding": {
                        "y": {
                            "field": "Label",
                            "type": "nominal",
                            "sort": "-x",
                            "axis": {"title": None},
                        },
                        "x": {
                            "field": "Level",
                            "type": "quantitative",
                            "scale": {"domain": [0, 100]},
                        },
                        "color": {
                            "field": "Category",
                            "type": "nominal",
                            "scale": {
                                "range": [
                                    P["ACCENT"],
                                    P["ACCENT2"],
                                    P["ACCENT3"],
                                    P["ACCENT4"],
                                ]
                            },
                            "legend": {
                                "labelColor": P["MUTED"],
                                "titleColor": P["MUTED"],
                            },
                        },
                        "tooltip": [
                            {"field": "Label", "type": "nominal"},
                            {"field": "Level", "type": "quantitative"},
                        ],
                    },
                    "config": {
                        "view": {"stroke": None},
                        "axis": {
                            "labelColor": P["MUTED"],
                            "titleColor": P["MUTED"],
                            "gridColor": "#ffffff14",
                            "domainColor": "#ffffff22",
                            "tickColor": "#ffffff22",
                            "labelFont": "Share Tech Mono",
                        },
                    },
                }
                st.vega_lite_chart(chart_df, spec, use_container_width=True, theme=None)
            else:
                st.info("Chart hidden.")

        with st.expander("Raw data"):
            st.table(filtered.set_index("Skill"))
            st.download_button(
                "Download skills CSV",
                filtered.to_csv(index=False),
                file_name="joel_skills.csv",
                mime="text/csv",
            )


with tab_projects:
    st.subheader("Selected cases")

    all_tools = sorted({tool for project in PROJECTS for tool in project["tools"]})
    pick = st.selectbox("Filter by tool", ["All"] + all_tools)

    visible = [p for p in PROJECTS if pick == "All" or pick in p["tools"]]

    for start in range(0, len(visible), 2):
        columns = st.columns(2, gap="large")

        for col, project in zip(columns, visible[start:start + 2]):
            with col:
                tags = "".join(
                    f'<span class="pill">{tool}</span>' for tool in project["tools"]
                )

                html(
                    f"""
                    <div class="project-card">
                        <div class="project-label">{project["number"]}</div>
                        <h3>{project["name"]}</h3>
                        <p class="muted">{project["description"]}</p>
                        <p><b>Role:</b> {project["role"]}</p>
                        <div>{tags}</div>
                        <div class="outcome"><b>Outcome:</b> {project["outcome"]}</div>
                    </div>
                    """
                )

                if project["url"]:
                    st.link_button(
                        "View project ↗",
                        project["url"],
                        use_container_width=True,
                    )
                else:
                    st.caption("Project link not added yet.")


with tab_contact:
    st.subheader("Let's connect")

    form_col, side_col = st.columns([1.3, 0.7], gap="large")

    with side_col:
        html(
            f"""
            <div class="panel">
                <div class="eyebrow">Signal</div>
                <p><b>Email</b><br>{EMAIL}</p>
                <p><b>GitHub</b><br><a href="{GITHUB}">{GITHUB.replace("https://", "")}</a></p>
                <p><b>Section</b><br>{SECTION}</p>
            </div>
            """
        )
        st.metric("Messages prepared", st.session_state.messages_sent)

    with form_col:
        st.write(
            "Have a project idea, want to collaborate, or just want to talk tech? "
            "Send me a message."
        )

        with st.form("contact_form"):
            sender_name = st.text_input("Your name")
            sender_email = st.text_input("Your email")
            reason = st.selectbox(
                "Reason",
                ["Collaboration", "Feedback", "Opportunity", "Just saying hi"],
            )
            subject = st.text_input("Subject", value="Hello from your portfolio")
            rating = st.slider("Rate this portfolio", 1, 5, 4)
            message = st.text_area(
                "Your message",
                height=160,
                placeholder="Write your message here...",
            )
            copy_me = st.checkbox("Send me a copy of the draft")

            submitted = st.form_submit_button(
                "Prepare email",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            if not sender_name.strip() or not sender_email.strip() or not message.strip():
                st.error("Please complete your name, email, and message.")
            elif "@" not in sender_email or "." not in sender_email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            else:
                body = (
                    f"From: {sender_name.strip()}\n"
                    f"Reply-to: {sender_email.strip()}\n"
                    f"Reason: {reason}\n"
                    f"Rating: {rating}/5\n\n"
                    f"{message.strip()}"
                )

                cc = f"&cc={quote(sender_email.strip())}" if copy_me else ""
                mailto = (
                    f"mailto:{EMAIL}"
                    f"?subject={quote(subject.strip())}"
                    f"&body={quote(body)}{cc}"
                )

                st.session_state.messages_sent += 1
                st.toast("Message received in the dark.", icon="📨")
                st.success(
                    f"Thanks, {sender_name.strip()}. Your email draft is ready."
                )
                st.link_button(
                    "Open email draft ↗",
                    mailto,
                    type="primary",
                    use_container_width=True,
                )
                st.download_button(
                    "Download message",
                    body,
                    file_name="message_to_joel.txt",
                    use_container_width=True,
                )

        st.caption(
            "This form does not store submissions or send email automatically. "
            "It prepares an email using your email application."
        )


html(
    f"""
    <div class="footer">
        <div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
            <span>© 2026 {NAME} · {PROGRAM} {YEAR} · Section {SECTION}</span>
            <span>Built with Python + Streamlit</span>
        </div>
    </div>
    """
)