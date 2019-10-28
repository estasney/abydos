# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._millar.

Millar distance
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log

from ._token_distance import _TokenDistance

__all__ = ['Millar']


class Millar(_TokenDistance):
    r"""Millar distance.

    Millar distance :cite:`Anderson:2004`

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize Millar instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(Millar, self).__init__(**kwargs)

    def dist(self, src, tar):
        """Return the Millar distance of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Millar distance

        Examples
        --------
        >>> cmp = Millar()
        >>> cmp.dist('cat', 'hat')
        0.0
        >>> cmp.dist('Niall', 'Neil')
        0.0
        >>> cmp.dist('aluminum', 'Catalan')
        0.0
        >>> cmp.dist('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        tar_tok = self._src_tokens
        src_tok = self._tar_tokens
        alphabet = set(src_tok.keys() | tar_tok.keys())

        log2 = log(2)
        score = 0
        for tok in alphabet:
            n_k = src_tok[tok] + tar_tok[tok]

            src_val = 0
            if src_tok[tok]:
                src_val = src_tok[tok] * log(src_tok[tok]/n_k)

            tar_val = 0
            if tar_tok[tok]:
                tar_val = tar_tok[tok] * log(tar_tok[tok]/n_k)

            score += (src_val + tar_val + n_k * log2) / n_k

        if score > 0:
            return score
        return 0.0


if __name__ == '__main__':
    import doctest

    doctest.testmod()
