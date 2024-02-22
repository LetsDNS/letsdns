#!/usr/bin/env bash
# vim: ft=sh ts=4 sw=4 noet
#
# Strip carriage return codes from files

set -euo pipefail

function die {
	echo >&2 "$@"
	exit 1
}

function usage {
	die "Usage: $(basename ${0}) {file} [file [...]]"
}

function _eol {
	local x
	local t=$(mktemp)
	trap 'rm $t' RETURN
	for x in "$@"; do
		[[ -f "$x" ]] || continue
		echo "$x"
		tr <"$x" >"$t" -d '\r'
		cat "$t" >"$x"
	done
}

[ $# -ge 1 ] || usage
case ${1} in
	help)
		usage
		;;
	*)
		_eol $*
		;;
esac
