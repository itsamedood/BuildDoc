<div align="center">
	<img src="./assets/builddoc-bg.png" width="700" height="400"></img>
	<p>
		<a href="https://github.com/itsamedood/BuildDoc/blob/main/LICENSE">
			<img src="https://img.shields.io/github/license/itsamedood/BuildDoc?color=blue&style=for-the-badge">
		</a>
		<a href="https://github.com/itsamedood/BuildDoc">
			<img src="https://img.shields.io/github/stars/itsamedood/BuildDoc?style=for-the-badge">
		</a>
		<br>
		<!-- Replace WIP with Download when complete. -->
		<a href="https://github.com/itsamedood/BuildDoc/releases"><b><i>~ WORK IN PROGRESS!! ~</i></b></a>
	</p>
</div>


# What is BuildDoc?
> ### A build tool for automatically running, compiling, and managing projects.
>
> Example:
> ```ini
> CC="gcc"
> FLAGS="-Wall -Wextra -O2 -g"
> TARGET="bin/program"
> MAIN="src/main.c"
>
> [build]
> &echo "Building program..."
> $CC $FLAGS -o $TARGET $MAIN
> $TARGET
> &echo "Done!"
> ```
---
# Branches
- `main` (most up to date)
- `og` (horrible please don't read)
- `cmigrate` (C rewrite because it's faster and i need to learn C at some point)
