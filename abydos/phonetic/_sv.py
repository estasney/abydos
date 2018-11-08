# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.phonetic._sv.

The phonetic._sv module implements phonetic algorithms for Scandinavian names
& languages (currently Swedish & Norwegian), including:

    - SfinxBis
    - Norphone
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from unicodedata import normalize as unicode_normalize

from six import text_type

from ._phonetic import Phonetic

__all__ = ['Norphone', 'SfinxBis', 'norphone', 'sfinxbis']


class SfinxBis(Phonetic):
    """SfinxBis code.

    SfinxBis is a Soundex-like algorithm defined in :cite:`Axelsson:2009`.

    This implementation follows the reference implementation:
    :cite:`Sjoo:2009`.

    SfinxBis is intended chiefly for Swedish names.
    """

    _adelstitler = (
        ' DE LA ',
        ' DE LAS ',
        ' DE LOS ',
        ' VAN DE ',
        ' VAN DEN ',
        ' VAN DER ',
        ' VON DEM ',
        ' VON DER ',
        ' AF ',
        ' AV ',
        ' DA ',
        ' DE ',
        ' DEL ',
        ' DEN ',
        ' DES ',
        ' DI ',
        ' DO ',
        ' DON ',
        ' DOS ',
        ' DU ',
        ' E ',
        ' IN ',
        ' LA ',
        ' LE ',
        ' MAC ',
        ' MC ',
        ' VAN ',
        ' VON ',
        ' Y ',
        ' S:T ',
    )

    _harde_vokaler = {'A', 'O', 'U', 'Å'}
    _mjuka_vokaler = {'E', 'I', 'Y', 'Ä', 'Ö'}
    _uc_c_set = {
        'B',
        'C',
        'D',
        'F',
        'G',
        'H',
        'J',
        'K',
        'L',
        'M',
        'N',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'V',
        'W',
        'X',
        'Z',
    }
    _uc_set = {
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
        'Ä',
        'Å',
        'Ö',
    }

    _trans = dict(
        zip(
            (ord(_) for _ in 'BCDFGHJKLMNPQRSTVZAOUÅEIYÄÖ'),
            '123729224551268378999999999',
        )
    )

    _substitutions = dict(
        zip(
            (ord(_) for _ in 'WZÀÁÂÃÆÇÈÉÊËÌÍÎÏÑÒÓÔÕØÙÚÛÜÝ'),
            'VSAAAAÄCEEEEIIIINOOOOÖUUUYY',
        )
    )

    def encode(self, word, max_length=-1):
        """Return the SfinxBis code for a word.

        Args:
            word (str): The word to transform
            max_length (int): The length of the code returned (defaults to
                unlimited)

        Returns:
            tuple: The SfinxBis value

        Examples:
            >>> pe = SfinxBis()
            >>> pe.encode('Christopher')
            ('K68376',)
            >>> pe.encode('Niall')
            ('N4',)
            >>> pe.encode('Smith')
            ('S53',)
            >>> pe.encode('Schmidt')
            ('S53',)

            >>> pe.encode('Johansson')
            ('J585',)
            >>> pe.encode('Sjöberg')
            ('#162',)

        """

        def _foersvensker(lokal_ordet):
            """Return the Swedish-ized form of the word.

            Args:
                lokal_ordet (str): Word to transform

            Returns:
                str: Transformed word

            """
            lokal_ordet = lokal_ordet.replace('STIERN', 'STJÄRN')
            lokal_ordet = lokal_ordet.replace('HIE', 'HJ')
            lokal_ordet = lokal_ordet.replace('SIÖ', 'SJÖ')
            lokal_ordet = lokal_ordet.replace('SCH', 'SH')
            lokal_ordet = lokal_ordet.replace('QU', 'KV')
            lokal_ordet = lokal_ordet.replace('IO', 'JO')
            lokal_ordet = lokal_ordet.replace('PH', 'F')

            for i in self._harde_vokaler:
                lokal_ordet = lokal_ordet.replace(i + 'Ü', i + 'J')
                lokal_ordet = lokal_ordet.replace(i + 'Y', i + 'J')
                lokal_ordet = lokal_ordet.replace(i + 'I', i + 'J')
            for i in self._mjuka_vokaler:
                lokal_ordet = lokal_ordet.replace(i + 'Ü', i + 'J')
                lokal_ordet = lokal_ordet.replace(i + 'Y', i + 'J')
                lokal_ordet = lokal_ordet.replace(i + 'I', i + 'J')

            if 'H' in lokal_ordet:
                for i in self._uc_c_set:
                    lokal_ordet = lokal_ordet.replace('H' + i, i)

            lokal_ordet = lokal_ordet.translate(self._substitutions)

            lokal_ordet = lokal_ordet.replace('Ð', 'ETH')
            lokal_ordet = lokal_ordet.replace('Þ', 'TH')
            lokal_ordet = lokal_ordet.replace('ß', 'SS')

            return lokal_ordet

        def _koda_foersta_ljudet(lokal_ordet):
            """Return the word with the first sound coded.

            Args:
                lokal_ordet (str): Word to transform

            Returns:
                str: Transformed word

            """
            if (
                lokal_ordet[0:1] in self._mjuka_vokaler
                or lokal_ordet[0:1] in self._harde_vokaler
            ):
                lokal_ordet = '$' + lokal_ordet[1:]
            elif lokal_ordet[0:2] in ('DJ', 'GJ', 'HJ', 'LJ'):
                lokal_ordet = 'J' + lokal_ordet[2:]
            elif (
                lokal_ordet[0:1] == 'G'
                and lokal_ordet[1:2] in self._mjuka_vokaler
            ):
                lokal_ordet = 'J' + lokal_ordet[1:]
            elif lokal_ordet[0:1] == 'Q':
                lokal_ordet = 'K' + lokal_ordet[1:]
            elif lokal_ordet[0:2] == 'CH' and lokal_ordet[2:3] in frozenset(
                self._mjuka_vokaler | self._harde_vokaler
            ):
                lokal_ordet = '#' + lokal_ordet[2:]
            elif (
                lokal_ordet[0:1] == 'C'
                and lokal_ordet[1:2] in self._harde_vokaler
            ):
                lokal_ordet = 'K' + lokal_ordet[1:]
            elif (
                lokal_ordet[0:1] == 'C' and lokal_ordet[1:2] in self._uc_c_set
            ):
                lokal_ordet = 'K' + lokal_ordet[1:]
            elif lokal_ordet[0:1] == 'X':
                lokal_ordet = 'S' + lokal_ordet[1:]
            elif (
                lokal_ordet[0:1] == 'C'
                and lokal_ordet[1:2] in self._mjuka_vokaler
            ):
                lokal_ordet = 'S' + lokal_ordet[1:]
            elif lokal_ordet[0:3] in ('SKJ', 'STJ', 'SCH'):
                lokal_ordet = '#' + lokal_ordet[3:]
            elif lokal_ordet[0:2] in ('SH', 'KJ', 'TJ', 'SJ'):
                lokal_ordet = '#' + lokal_ordet[2:]
            elif (
                lokal_ordet[0:2] == 'SK'
                and lokal_ordet[2:3] in self._mjuka_vokaler
            ):
                lokal_ordet = '#' + lokal_ordet[2:]
            elif (
                lokal_ordet[0:1] == 'K'
                and lokal_ordet[1:2] in self._mjuka_vokaler
            ):
                lokal_ordet = '#' + lokal_ordet[1:]
            return lokal_ordet

        # Steg 1, Versaler
        word = unicode_normalize('NFC', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = word.replace('-', ' ')

        # Steg 2, Ta bort adelsprefix
        for adelstitel in self._adelstitler:
            while adelstitel in word:
                word = word.replace(adelstitel, ' ')
            if word.startswith(adelstitel[1:]):
                word = word[len(adelstitel) - 1 :]

        # Split word into tokens
        ordlista = word.split()

        # Steg 3, Ta bort dubbelteckning i början på namnet
        ordlista = [
            self._delete_consecutive_repeats(ordet) for ordet in ordlista
        ]
        if not ordlista:
            # noinspection PyRedundantParentheses
            return ('',)

        # Steg 4, Försvenskning
        ordlista = [_foersvensker(ordet) for ordet in ordlista]

        # Steg 5, Ta bort alla tecken som inte är A-Ö (65-90,196,197,214)
        ordlista = [
            ''.join(c for c in ordet if c in self._uc_set)
            for ordet in ordlista
        ]

        # Steg 6, Koda första ljudet
        ordlista = [_koda_foersta_ljudet(ordet) for ordet in ordlista]

        # Steg 7, Dela upp namnet i två delar
        rest = [ordet[1:] for ordet in ordlista]

        # Steg 8, Utför fonetisk transformation i resten
        rest = [ordet.replace('DT', 'T') for ordet in rest]
        rest = [ordet.replace('X', 'KS') for ordet in rest]

        # Steg 9, Koda resten till en sifferkod
        for vokal in self._mjuka_vokaler:
            rest = [ordet.replace('C' + vokal, '8' + vokal) for ordet in rest]
        rest = [ordet.translate(self._trans) for ordet in rest]

        # Steg 10, Ta bort intilliggande dubbletter
        rest = [self._delete_consecutive_repeats(ordet) for ordet in rest]

        # Steg 11, Ta bort alla "9"
        rest = [ordet.replace('9', '') for ordet in rest]

        # Steg 12, Sätt ihop delarna igen
        ordlista = [
            ''.join(ordet) for ordet in zip((_[0:1] for _ in ordlista), rest)
        ]

        # truncate, if max_length is set
        if max_length > 0:
            ordlista = [ordet[:max_length] for ordet in ordlista]

        return tuple(ordlista)


def sfinxbis(word, max_length=-1):
    """Return the SfinxBis code for a word.

    This is a wrapper for :py:meth:`SfinxBis.encode`.

    Args:
        word (str): The word to transform
        max_length (int): The length of the code returned (defaults to
            unlimited)

    Returns:
        tuple: The SfinxBis value

    Examples:
        >>> sfinxbis('Christopher')
        ('K68376',)
        >>> sfinxbis('Niall')
        ('N4',)
        >>> sfinxbis('Smith')
        ('S53',)
        >>> sfinxbis('Schmidt')
        ('S53',)

        >>> sfinxbis('Johansson')
        ('J585',)
        >>> sfinxbis('Sjöberg')
        ('#162',)

    """
    return SfinxBis().encode(word, max_length)


class Norphone(Phonetic):
    """Norphone.

    The reference implementation by Lars Marius Garshol is available in
    :cite:`Garshol:2015`.

    Norphone was designed for Norwegian, but this implementation has been
    extended to support Swedish vowels as well. This function incorporates
    the "not implemented" rules from the above file's rule set.
    """

    _uc_v_set = {'A', 'E', 'I', 'O', 'U', 'Y', 'Å', 'Æ', 'Ø', 'Ä', 'Ö'}

    _replacements = {
        4: {'SKEI': 'X'},
        3: {'SKJ': 'X', 'KEI': 'X'},
        2: {
            'CH': 'K',
            'CK': 'K',
            'GJ': 'J',
            'GH': 'K',
            'HG': 'K',
            'HJ': 'J',
            'HL': 'L',
            'HR': 'R',
            'KJ': 'X',
            'KI': 'X',
            'LD': 'L',
            'ND': 'N',
            'PH': 'F',
            'TH': 'T',
            'SJ': 'X',
        },
        1: {'W': 'V', 'X': 'KS', 'Z': 'S', 'D': 'T', 'G': 'K'},
    }

    def encode(self, word):
        """Return the Norphone code.

        Args:
            word (str): The word to transform

        Returns:
            str: The Norphone code

        Examples:
            >>> pe = Norphone()
            >>> pe.encode('Hansen')
            'HNSN'
            >>> pe.encode('Larsen')
            'LRSN'
            >>> pe.encode('Aagaard')
            'ÅKRT'
            >>> pe.encode('Braaten')
            'BRTN'
            >>> pe.encode('Sandvik')
            'SNVK'

        """
        word = word.upper()

        code = ''
        skip = 0

        if word[0:2] == 'AA':
            code = 'Å'
            skip = 2
        elif word[0:2] == 'GI':
            code = 'J'
            skip = 2
        elif word[0:3] == 'SKY':
            code = 'X'
            skip = 3
        elif word[0:2] == 'EI':
            code = 'Æ'
            skip = 2
        elif word[0:2] == 'KY':
            code = 'X'
            skip = 2
        elif word[:1] == 'C':
            code = 'K'
            skip = 1
        elif word[:1] == 'Ä':
            code = 'Æ'
            skip = 1
        elif word[:1] == 'Ö':
            code = 'Ø'
            skip = 1

        if word[-2:] == 'DT':
            word = word[:-2] + 'T'
        # Though the rules indicate this rule applies in all positions, the
        # reference implementation indicates it applies only in final position.
        elif word[-2:-1] in self._uc_v_set and word[-1:] == 'D':
            word = word[:-2]

        for pos, char in enumerate(word):
            if skip:
                skip -= 1
            else:
                for length in sorted(self._replacements, reverse=True):
                    if word[pos : pos + length] in self._replacements[length]:
                        code += self._replacements[length][
                            word[pos : pos + length]
                        ]
                        skip = length - 1
                        break
                else:
                    if not pos or char not in self._uc_v_set:
                        code += char

        code = self._delete_consecutive_repeats(code)

        return code


def norphone(word):
    """Return the Norphone code.

    This is a wrapper for :py:meth:`Norphone.encode`.

    Args:
        word (str): The word to transform

    Returns:
        str: The Norphone code

    Examples:
        >>> norphone('Hansen')
        'HNSN'
        >>> norphone('Larsen')
        'LRSN'
        >>> norphone('Aagaard')
        'ÅKRT'
        >>> norphone('Braaten')
        'BRTN'
        >>> norphone('Sandvik')
        'SNVK'

    """
    return Norphone().encode(word)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
