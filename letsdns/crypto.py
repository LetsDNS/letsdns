# Copyright © 2022 Ralph Seichter
#
# This file is part of LetsDNS.
#
# LetsDNS is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# LetsDNS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with LetsDNS.
# If not, see <https://www.gnu.org/licenses/>.
import hashlib

# noinspection PyProtectedMember
from cryptography.hazmat.primitives._serialization import Encoding
from cryptography.x509 import Certificate
from cryptography.x509 import load_pem_x509_certificate


def read_x509_cert(filename: str) -> Certificate:
    """Read x509 certificate from file."""
    with open(filename, 'rb') as f:
        return load_pem_x509_certificate(f.read())


def sha256_hexdigest(data) -> str:
    """Generate hexadecimal SHA256 hash for some data."""
    _hash = hashlib.sha256()
    _hash.update(data)
    return _hash.hexdigest()


def dane_tlsa_data(prefix: str, certificate: Certificate) -> str:
    """Return TLSA object for a certificate.

    Args:
        prefix: Prefix string, e.g. 3-1-1. All dashes will be replaced with whitespace.
        certificate: x509 certificate.
    """
    _prefix = prefix.replace('-', ' ')
    cert = certificate.public_bytes(Encoding.DER)
    return f'{_prefix} {sha256_hexdigest(cert)}'
