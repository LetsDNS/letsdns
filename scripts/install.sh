#!/usr/bin/env bash
# vim: ft=sh ts=4 sw=4 noet
#
# Install LetsDNS from scratch.

set -euo pipefail

function die {
	echo >&2 "$@"
	exit 1
}

function usage {
	die "Usage: $(basename "${0}") {destination-directory}"
}

function letsdns_install {
	local d="${1}"
	[ -d "${d}" ] && die "Directory ${d} already exists, exiting."
	mkdir -p "${d}"
	pushd >/dev/null "${d}"
	python3 -m venv .venv
	source .venv/bin/activate
	pip install --pre letsdns
	letsdns -h
	popd >/dev/null
}

[ $# -ge 1 ] || usage
letsdns_install "${1}"
