from syntaxlab.config import Config, LabError
from syntaxlab.courses import Catalog, Exercise
from syntaxlab.progress import Progress
from syntaxlab.workspace import Workspaces


class Lab:
    def __init__(self, config: Config):
        self.config = config
        self.catalog = Catalog(config.root)
        self.progress = Progress(config.root / config.database)
        self.progress.sync(self.catalog)
        self.workspaces = Workspaces(config, self.catalog)

    def select(self, key: str | None = None, language: str | None = None) -> Exercise:
        done = self.progress.completed()
        exercise: Exercise | None
        if key:
            if key not in self.catalog.exercises:
                raise LabError(f"Unknown exercise: {key}")
            exercise = self.catalog.exercises[key]
        else:
            current = self.catalog.exercises.get(self.progress.get("current") or "")
            if language is None and current:
                language = current.language
            exercise = current if current and current.id not in done and (
                not language or current.language == language) else self.catalog.next(done, language)
        if exercise is None:
            raise LabError("All available exercises complete. See the roadmap in syntaxlab progress.")
        if not self.catalog.unlocked(exercise, done):
            raise LabError("Locked. Complete prerequisites: " + ", ".join(set(exercise.prerequisites) - done))
        return exercise

    def prepare(self, exercise: Exercise):
        self.select(exercise.id)
        path = self.workspaces.create(exercise)
        self.progress.set("current", exercise.id)
        return path
