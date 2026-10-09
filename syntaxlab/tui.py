from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Label, ListItem, ListView, Markdown, Static, Select
from syntaxlab.checks import check
from syntaxlab.cli import bar
from syntaxlab.config import LabError, inside
from syntaxlab.courses import Exercise
from syntaxlab.progress import percentage
from syntaxlab.runner import run
from syntaxlab.service import Lab
from syntaxlab.languages import LANGUAGES


class SyntaxLabApp(App):
    TITLE = "SyntaxLab"
    SUB_TITLE = "Read · Understand · Write · Compile · Debug · Test"
    CSS = """
    Screen { background: #101923; color: #d6e3ec; }
    Header { background: #182a39; }
    #summary { height: 4; padding: 1 2; color: #74d8c8; }
    #body { height: 1fr; }
    #sidebar { width: 39%; min-width: 28; border-right: solid #294454; }
    #path-title { height: 3; padding: 1 2; text-style: bold; }
    #module, #language { margin: 0 1 1 1; }
    ListView { background: #101923; height: 1fr; }
    ListItem { padding: 1 2; }
    ListItem.-highlight { background: #244556; }
    #detail { width: 1fr; padding: 0 2; }
    #actions { height: auto; padding: 1 0; }
    Button { margin-right: 1; min-width: 12; }
    #results { padding: 1; color: #eacb8b; height: auto; }
    Footer { background: #182a39; }
    """
    BINDINGS = [("q", "quit", "Quit"), ("l", "language", "Language"),
                ("p", "projects", "Projects"), ("d", "docs", "Docs"),
                ("o", "open", "Open VS Code"), ("c", "check", "Check"),
                ("h", "hint", "Hint"), ("g", "progress", "Progress"),
                ("b", "lesson", "Lesson"), ("enter", "resume", "Continue")]

    def __init__(self, lab: Lab):
        super().__init__()
        self.lab = lab
        self.language = "scala"
        current = lab.catalog.exercises.get(lab.progress.get("current") or "")
        if current:
            self.language = current.language
        self.project_mode = bool(current and current.project)
        self.module = "all"
        self.doc_path = ""
        self.items: list[Exercise] = []
        self.selected: Exercise | None = None
        self.checking = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(id="summary")
        with Horizontal(id="body"):
            with Vertical(id="sidebar"):
                yield Label(id="path-title")
                yield Select([(language.title(), language) for language in LANGUAGES],
                             value=self.language, allow_blank=False, id="language")
                yield Select([("All modules", "all")], value="all", allow_blank=False, id="module")
                yield ListView(id="lessons")
            with VerticalScroll(id="detail"):
                yield Markdown("Choose a lesson to begin.", id="lesson")
                with Horizontal(id="actions"):
                    yield Button("Workspace", id="prepare", variant="primary")
                    yield Button("VS Code", id="editor")
                    yield Button("Check", id="check")
                yield Static("", id="results", markup=False)
        yield Footer()

    async def on_mount(self) -> None:
        self.refresh_modules()
        await self.refresh_path()

    def refresh_modules(self) -> None:
        done = self.lab.progress.completed()
        options = [("All modules", "all")]
        for module in self.lab.catalog.modules:
            ids = [e.id for e in self.lab.catalog.ordered(self.language)
                   if e.module == module["id"] and bool(e.project) == self.project_mode]
            if module["language"] == self.language and ids:
                options.append((f"{module['title']}  {len(set(ids) & done)}/{len(ids)}", module["id"]))
        select = self.query_one("#module", Select)
        with self.prevent(Select.Changed):
            select.set_options(options)
            select.value = self.module if self.module in {value for _, value in options} else "all"

    @on(Select.Changed, "#module")
    async def module_changed(self, event: Select.Changed) -> None:
        if isinstance(event.value, str) and self.module != event.value:
            self.module = event.value
            await self.refresh_path()

    async def refresh_path(self) -> None:
        done = self.lab.progress.completed()
        ids = [e.id for e in self.lab.catalog.ordered(self.language)]
        self.query_one("#summary", Static).update(
            f"{self.language.upper()}   {bar(percentage(ids, done))}    "
            f"Overall {percentage(list(self.lab.catalog.exercises), done)}%\n"
            f"Current: {self.lab.progress.get('current') or 'Start with the first lesson'}")
        self.query_one("#path-title", Label).update("Growing projects" if self.project_mode else "Skill path")
        self.items = [e for e in self.lab.catalog.ordered(self.language) if bool(e.project) == self.project_mode
                      and (self.module == "all" or e.module == self.module)]
        view = self.query_one(ListView)
        await view.clear()
        for e in self.items:
            symbol = "✓" if e.id in done else "●" if self.lab.catalog.unlocked(e, done) else "🔒"
            await view.append(ListItem(Label(f"{symbol} {e.module.replace('-', ' ').title()}\n   {e.title}")))
        current = self.lab.progress.get("current")
        view.index = next((i for i, e in enumerate(self.items) if e.id == current), 0)
        view.focus()

    @on(ListView.Highlighted)
    def highlight(self, event: ListView.Highlighted) -> None:
        index = event.list_view.index
        if index is None or index >= len(self.items):
            return
        self.selected = self.items[index]
        self.action_lesson()
        self.query_one("#results", Static).update("")

    def action_lesson(self) -> None:
        e = self.selected
        if e is None:
            return
        unlocked = self.lab.catalog.unlocked(e, self.lab.progress.completed())
        text = f"# {e.title}\n**{e.language.upper()} / {e.module}** · Level {e.difficulty}/5\n\n{e.assignment}"
        if not unlocked:
            text += "\n\n## Locked\nComplete: " + ", ".join(e.prerequisites)
        text += "\n\n---\nWrite the source yourself. **D** reference · **H** hint · **O** editor · **C** check"
        self.query_one("#lesson", Markdown).update(text)

    async def action_language(self) -> None:
        await self.change_language(LANGUAGES[(LANGUAGES.index(self.language) + 1) % len(LANGUAGES)])

    @on(Select.Changed, "#language")
    async def language_changed(self, event: Select.Changed) -> None:
        if isinstance(event.value, str) and event.value != self.language:
            await self.change_language(event.value)

    async def change_language(self, language: str) -> None:
        self.language = language
        with self.prevent(Select.Changed):
            self.query_one("#language", Select).value = language
        self.module = "all"
        self.refresh_modules()
        await self.refresh_path()

    async def action_projects(self) -> None:
        self.project_mode = not self.project_mode
        self.module = "all"
        self.refresh_modules()
        await self.refresh_path()

    def action_docs(self) -> None:
        if self.selected:
            path = inside(self.lab.config.root / "content", self.selected.docs)
            self.doc_path = self.selected.docs
            self.query_one("#lesson", Markdown).update(path.read_text())
            self.lab.progress.encounter("docs", self.selected.docs)

    @on(Markdown.LinkClicked)
    def documentation_link(self, event: Markdown.LinkClicked) -> None:
        event.stop()
        if not self.doc_path or not event.href.endswith(".md"):
            return
        from pathlib import PurePosixPath
        relative = str(PurePosixPath(self.doc_path).parent / event.href)
        try:
            path = inside(self.lab.config.root / "content", relative)
            self.query_one("#lesson", Markdown).update(path.read_text())
            self.doc_path = relative
            self.lab.progress.encounter("docs", relative)
        except (LabError, OSError) as exc:
            self.notify(str(exc), severity="error")

    def action_progress(self) -> None:
        done = self.lab.progress.completed()
        text = "# Your learning path\n\n| Module | Progress |\n|---|---|\n"
        for module in self.lab.catalog.modules:
            if module["language"] != self.language:
                continue
            ids = [e.id for e in self.lab.catalog.ordered(self.language) if e.module == module["id"]]
            value = f"{percentage(ids, done)}% · {len(set(ids) & done)}/{len(ids)}" if ids else "Roadmap"
            text += f"| {module['title']} | {value} |\n"
        text += "\n**B** returns to the selected assignment. CLI `syntaxlab progress` includes concept-level detail."
        self.query_one("#lesson", Markdown).update(text)

    @on(ListView.Selected)
    def selected_lesson(self, event: ListView.Selected) -> None:
        self.action_resume()

    def action_hint(self) -> None:
        if self.selected:
            key = "hint:" + self.selected.id
            level = min(int(self.lab.progress.get(key) or "0") + 1, len(self.selected.hints))
            self.lab.progress.set(key, str(level))
            self.query_one("#results", Static).update(self.selected.hints[level - 1] if level else "Review the docs.")

    def action_resume(self) -> None:
        if self.selected:
            try:
                path = self.lab.prepare(self.selected)
                self.query_one("#results", Static).update(f"Workspace ready:\n{path}\n\ncd {path}\nsyntaxlab check")
            except (LabError, OSError) as exc:
                self.notify(str(exc), severity="error")

    @work(thread=True, exclusive=True, group="editor")
    def action_open(self) -> None:
        if self.selected:
            try:
                path = self.lab.prepare(self.selected)
                result = run([self.lab.config.editor, str(path)], self.lab.config.root, 20)
                self.call_from_thread(self.notify, "Workspace opened" if result.ok else result.stderr)
            except (LabError, OSError) as exc:
                self.call_from_thread(self.notify, str(exc))

    @work(thread=True, exclusive=True, group="checks")
    def action_check(self) -> None:
        if not self.selected or self.checking:
            return
        self.checking = True
        e = self.selected
        try:
            path = self.lab.prepare(e)
            self.call_from_thread(self.query_one("#results", Static).update, "Checking… compiler output will appear here.")
            results = check(e, path, self.lab.config, self.lab.progress)
            text = "\n".join(f"{'✓' if r.passed else '✗'} {r.label}\n{r.output}" for r in results)
            if all(r.passed for r in results):
                text += "\nExercise complete! Use the next unlocked lesson."
                if e.project:
                    text += "\nFor an explicit Git checkpoint: syntaxlab check --checkpoint"
            self.call_from_thread(self.post_check_refresh)
            self.call_from_thread(self.query_one("#results", Static).update, text)
        except (LabError, OSError) as exc:
            self.call_from_thread(self.notify, str(exc))
        finally:
            self.checking = False

    def post_check_refresh(self) -> None:
        self.refresh_modules()
        done = self.lab.progress.completed()
        ids = [e.id for e in self.lab.catalog.ordered(self.language)]
        self.query_one("#summary", Static).update(
            f"{self.language.upper()}   {bar(percentage(ids, done))}    "
            f"Overall {percentage(list(self.lab.catalog.exercises), done)}%\n"
            f"Current: {self.lab.progress.get('current') or 'Choose a lesson'}")
        for item, exercise in zip(self.query_one(ListView).children, self.items):
            symbol = "✓" if exercise.id in done else "●" if self.lab.catalog.unlocked(exercise, done) else "🔒"
            item.query_one(Label).update(
                f"{symbol} {exercise.module.replace('-', ' ').title()}\n   {exercise.title}")

    @on(Button.Pressed)
    def pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "prepare":
            self.action_resume()
        elif event.button.id == "editor":
            self.action_open()
        elif event.button.id == "check":
            self.action_check()
