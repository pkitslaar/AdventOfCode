from pathlib import Path
import jinja2
import argparse
import sys


this_dir = Path(__file__).parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("--year", type=int, default=2023)
    parser.add_argument("--template", default="day_xx.py.template")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    day_str = f"{args.day:02}"
    template = jinja2.Template(Path(args.template).read_text())
    output_text = template.render(year=args.year, day_str=day_str)

    assert this_dir.name == str(args.year)
    output_dir = this_dir / f"day {day_str}"

    output_file = output_dir / f"day_{day_str}.py"
    if output_file.exists() and not args.force:
        print(f"File {output_file} already exists! Use --force to overwrite.")
        return
    
    # create output
    output_dir.mkdir(exist_ok=True)
    with open(output_file, "w") as f:
        f.write(output_text)


if __name__ == "__main__":
    sys.exit(main())
