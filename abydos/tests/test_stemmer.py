# -*- coding: utf-8 -*-
"""abydos.tests.test_stemmer

This module contains unit tests for abydos.stemmer

Copyright 2014 by Christopher C. Little.
This file is part of Abydos.

Abydos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Abydos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Abydos. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals
import unittest
from abydos.stemmer import _m_degree, _has_vowel, _ends_in_doubled_cons, \
    _ends_in_cvc, porter, _snowball_r1, _snowball_r2, \
    _snowball_short_syllable, _snowball_ends_in_short_syllable, porter2
import os

TESTDIR = os.path.dirname(__file__)

class PorterTestCases(unittest.TestCase):
    """test cases for abydos.stemmer._m_degree, abydos.stemmer.porter 
    """
    def test_m_degree(self):
        """test abydos.stemmer._m_degree
        """
        # base case
        self.assertEqual(_m_degree(''), 0)

        # m==0
        self.assertEqual(_m_degree('TR'), 0)
        self.assertEqual(_m_degree('EE'), 0)
        self.assertEqual(_m_degree('TREE'), 0)
        self.assertEqual(_m_degree('Y'), 0)
        self.assertEqual(_m_degree('BY'), 0)

        # m==1
        self.assertEqual(_m_degree('TROUBLE'), 1)
        self.assertEqual(_m_degree('OATS'), 1)
        self.assertEqual(_m_degree('TREES'), 1)
        self.assertEqual(_m_degree('IVY'), 1)

        # m==2
        self.assertEqual(_m_degree('TROUBLES'), 2)
        self.assertEqual(_m_degree('PRIVATE'), 2)
        self.assertEqual(_m_degree('OATEN'), 2)
        self.assertEqual(_m_degree('ORRERY'), 2)


    def test_has_vowel(self):
        """test abydos.stemmer._has_vowel
        """
        # base case
        self.assertFalse(_has_vowel(''))

        # False cases
        self.assertFalse(_has_vowel('B'))
        self.assertFalse(_has_vowel('C'))
        self.assertFalse(_has_vowel('BC'))
        self.assertFalse(_has_vowel('BCDFGHJKLMNPQRSTVWXYZ'))
        self.assertFalse(_has_vowel('Y'))

        # True cases
        self.assertTrue(_has_vowel('A'))
        self.assertTrue(_has_vowel('E'))
        self.assertTrue(_has_vowel('AE'))
        self.assertTrue(_has_vowel('AEIOUy'))
        self.assertTrue(_has_vowel('y'))

        self.assertTrue(_has_vowel('ADE'))
        self.assertTrue(_has_vowel('CAD'))
        self.assertTrue(_has_vowel('ADD'))
        self.assertTrue(_has_vowel('PHI'))
        self.assertTrue(_has_vowel('PFy'))


    def test_ends_in_doubled_cons(self):
        """test abydos.stemmer._ends_in_doubled_cons
        """
        # base case
        self.assertFalse(_ends_in_doubled_cons(''))

        # False cases
        self.assertFalse(_ends_in_doubled_cons('B'))
        self.assertFalse(_ends_in_doubled_cons('C'))
        self.assertFalse(_ends_in_doubled_cons('BC'))
        self.assertFalse(_ends_in_doubled_cons('BCDFGHJKLMNPQRSTVWXYZ'))
        self.assertFalse(_ends_in_doubled_cons('Y'))
        self.assertFalse(_ends_in_doubled_cons('A'))
        self.assertFalse(_ends_in_doubled_cons('E'))
        self.assertFalse(_ends_in_doubled_cons('AE'))
        self.assertFalse(_ends_in_doubled_cons('AEIOUy'))
        self.assertFalse(_ends_in_doubled_cons('y'))
        self.assertFalse(_ends_in_doubled_cons('ADE'))
        self.assertFalse(_ends_in_doubled_cons('CAD'))
        self.assertFalse(_ends_in_doubled_cons('PHI'))
        self.assertFalse(_ends_in_doubled_cons('PFy'))
        self.assertFalse(_ends_in_doubled_cons('FADDY'))
        self.assertFalse(_ends_in_doubled_cons('AIII'))
        self.assertFalse(_ends_in_doubled_cons('Ayyy'))

        # True cases
        self.assertTrue(_ends_in_doubled_cons('ADD'))
        self.assertTrue(_ends_in_doubled_cons('FADD'))
        self.assertTrue(_ends_in_doubled_cons('FADDDD'))
        self.assertTrue(_ends_in_doubled_cons('RAYY'))
        self.assertTrue(_ends_in_doubled_cons('DOLL'))
        self.assertTrue(_ends_in_doubled_cons('PARR'))
        self.assertTrue(_ends_in_doubled_cons('PARRR'))
        self.assertTrue(_ends_in_doubled_cons('BACC'))


    def test_ends_in_cvc(self):
        """test abydos.stemmer._ends_in_cvc
        """
        # base case
        self.assertFalse(_ends_in_cvc(''))

        # False cases
        self.assertFalse(_ends_in_cvc('B'))
        self.assertFalse(_ends_in_cvc('C'))
        self.assertFalse(_ends_in_cvc('BC'))
        self.assertFalse(_ends_in_cvc('BCDFGHJKLMNPQRSTVWXYZ'))
        self.assertFalse(_ends_in_cvc('YYY'))
        self.assertFalse(_ends_in_cvc('DDD'))
        self.assertFalse(_ends_in_cvc('FAAF'))
        self.assertFalse(_ends_in_cvc('RARE'))
        self.assertFalse(_ends_in_cvc('RHy'))

        # True cases
        self.assertTrue(_ends_in_cvc('DAD'))
        self.assertTrue(_ends_in_cvc('PHAD'))
        self.assertTrue(_ends_in_cvc('FADED'))
        self.assertTrue(_ends_in_cvc('MAYOR'))
        self.assertTrue(_ends_in_cvc('ENLIL'))
        self.assertTrue(_ends_in_cvc('PARER'))
        self.assertTrue(_ends_in_cvc('PADRES'))
        self.assertTrue(_ends_in_cvc('BACyC'))

        # Special case for W, X, & Y
        self.assertFalse(_ends_in_cvc('CRAW'))
        self.assertFalse(_ends_in_cvc('MAX'))
        self.assertFalse(_ends_in_cvc('CRAY'))


    def test_porter(self):
        """test abydos.stemmer.porter
        """
        # base case
        self.assertEqual(porter(''), '')

        # simple cases
        self.assertEqual(porter('C'), 'C')
        self.assertEqual(porter('DA'), 'DA')
        self.assertEqual(porter('AD'), 'AD')
        self.assertEqual(porter('SING'), 'SING')
        self.assertEqual(porter('SINGING'), 'SING')


    def test_porter_snowball(self):
        """test abydos.stemmer.porter (Snowball testset)

        These test cases are from
        http://snowball.tartarus.org/algorithms/porter/diffs.txt
        """
        #  Snowball Porter test set
        with open(TESTDIR+'/snowball_porter.csv') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                line = line.strip().split(',')
                word, stem = line[0], line[1]
                self.assertEqual(porter(word), stem.upper())

    def test_snowball_r1(self):
        """test abydos.stemmer._snowball_r1
        """
        # base case
        self.assertEqual(_snowball_r1(''), '')

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(_snowball_r1('beautiful'), 'iful')
        self.assertEqual(_snowball_r1('beauty'), 'y')
        self.assertEqual(_snowball_r1('beau'), '')
        self.assertEqual(_snowball_r1('animadversion'), 'imadversion')
        self.assertEqual(_snowball_r1('sprinkled'), 'kled')
        self.assertEqual(_snowball_r1('eucharist'), 'harist')

    def test_snowball_r2(self):
        """test abydos.stemmer._snowball_r2
        """
        # base case
        self.assertEqual(_snowball_r2(''), '')

        # examples from http://snowball.tartarus.org/texts/r1r2.html
        self.assertEqual(_snowball_r2('beautiful'), 'ul')
        self.assertEqual(_snowball_r2('beauty'), '')
        self.assertEqual(_snowball_r2('beau'), '')
        self.assertEqual(_snowball_r2('animadversion'), 'adversion')
        self.assertEqual(_snowball_r2('sprinkled'), '')
        self.assertEqual(_snowball_r2('eucharist'), 'ist')

    def test_snowball_short_syllable(self):
        """test abydos.stemmer._snowball_short_syllable
        """
        # base case
        self.assertFalse(_snowball_short_syllable(''))

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(_snowball_short_syllable('rap', 1))
        self.assertTrue(_snowball_short_syllable('trap', 2))
        self.assertTrue(_snowball_short_syllable('entrap', 4))
        self.assertTrue(_snowball_short_syllable('ow'))
        self.assertTrue(_snowball_short_syllable('on'))
        self.assertTrue(_snowball_short_syllable('at'))
        self.assertFalse(_snowball_short_syllable('uproot', 3))
        self.assertFalse(_snowball_short_syllable('uproot', 4))
        self.assertFalse(_snowball_short_syllable('bestow', 4))
        #self.assertFalse(_snowball_short_syllable('disturb', 4))

    def test_snowball_ends_in_short_syllable(self):
        """test abydos.stemmer._snowball_ends_in_short_syllable
        """
        # base case
        self.assertFalse(_snowball_ends_in_short_syllable(''))

        # examples from
        # http://snowball.tartarus.org/algorithms/english/stemmer.html
        self.assertTrue(_snowball_ends_in_short_syllable('rap'))
        self.assertTrue(_snowball_ends_in_short_syllable('trap'))
        self.assertTrue(_snowball_ends_in_short_syllable('entrap'))
        self.assertTrue(_snowball_ends_in_short_syllable('ow'))
        self.assertTrue(_snowball_ends_in_short_syllable('on'))
        self.assertTrue(_snowball_ends_in_short_syllable('at'))
        self.assertFalse(_snowball_ends_in_short_syllable('uproot'))
        self.assertFalse(_snowball_ends_in_short_syllable('uproot'))
        self.assertFalse(_snowball_ends_in_short_syllable('bestow'))
        self.assertFalse(_snowball_short_syllable('disturb'))


    def test_porter2(self):
        """test abydos.stemmer.porter2
        """
        # base case
        self.assertEqual(porter2(''), '')

        # simple cases
        self.assertEqual(porter2('c'), 'c')
        self.assertEqual(porter2('da'), 'da')
        self.assertEqual(porter2('ad'), 'ad')
        self.assertEqual(porter2('sing'), 'sing')
        self.assertEqual(porter2('singing'), 'sing')


    def test_porter2_snowball(self):
        """test abydos.stemmer.porter2 (Snowball testset)

        These test cases are from
        http://snowball.tartarus.org/algorithms/english/diffs.txt
        """
        #  Snowball Porter test set
        with open(TESTDIR+'/snowball_porter2.csv') as snowball_testset:
            next(snowball_testset)
            for line in snowball_testset:
                line = line.strip().split(',')
                word, stem = line[0], line[1]
                self.assertEqual(porter2(word), stem.upper())
