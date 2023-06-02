from pathlib import Path

BASE_DIR = Path(__name__).parent


log_dir = BASE_DIR / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "bot.log"
