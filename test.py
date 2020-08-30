from pathlib import Path

# from src.random_generator import generate_random_yaml
# generate_random_yaml()
from src.gfx_pipeline import gfx

#TODO: Compact representation of Map




r = Path(".") / "random.yml"

gfx.run_pipeline(r)
