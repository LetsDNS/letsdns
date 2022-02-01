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
from typing import List

# noinspection PyProtectedMember
from cryptography.hazmat.primitives._serialization import Encoding
from cryptography.x509 import BasicConstraints
from cryptography.x509 import Certificate
from cryptography.x509 import load_pem_x509_certificate


def read_x509_cert(filename: str) -> Certificate:
    """Read x509 certificate from file."""
    with open(filename, 'rb') as f:
        return load_pem_x509_certificate(f.read())


def sha_hexdigest(something):
    """Generate hexadecimal SHA256 and SHA512 hashes for some data."""
    sha256 = hashlib.sha256()
    sha256.update(something)
    sha512 = hashlib.sha512()
    sha512.update(something)
    return sha256.hexdigest(), sha512.hexdigest()


def dane_tlsa_data(certificate: Certificate) -> List[str]:
    """Return TLSA record data for a certificate.

    Args:
        certificate: x509 certificate.
    """
    bc: BasicConstraints = certificate.extensions.get_extension_for_class(BasicConstraints).value
    if bc.ca:
        usage = '2'  # DANE-TA
    else:
        usage = '3'  # DANE-EE
    public_key = certificate.public_bytes(Encoding.DER)
    sha256, sha512 = sha_hexdigest(public_key)
    return [f'{usage} 1 1 {sha256}', f'{usage} 1 2 {sha512}']
