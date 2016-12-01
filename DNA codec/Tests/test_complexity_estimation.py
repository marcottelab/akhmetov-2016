"""Unit tests for validating operation of the complexity estimator. All should pass.

Author: Azat Akhmetov <azat@utexas.edu>
"""
from unittest import TestCase
import complexity_estimation


class Tester_number_of_possible_kmers(TestCase):
    def test_k_equals_1(self):
        self.assertEqual(complexity_estimation.__number_of_possible_kmers(1), 1)

    def test_k_equals_2(self):
        self.assertEqual(complexity_estimation.__number_of_possible_kmers(2), 3)

    def test_k_equals_3(self):
        self.assertEqual(complexity_estimation.__number_of_possible_kmers(3), 6)

    def test_k_equals_4(self):
        self.assertEqual(complexity_estimation.__number_of_possible_kmers(4), 10)

    def test_k_equals_5(self):
        self.assertEqual(complexity_estimation.__number_of_possible_kmers(5), 14)

    def test_k_equals_6(self):
        self.assertEqual(complexity_estimation.__number_of_possible_kmers(6), 19)

    def test_k_equals_7(self):
        self.assertEqual(complexity_estimation.__number_of_possible_kmers(7), 25)


class Tester_list_unique_kmers(TestCase):
    def test_a_1(self):
        self.assertListEqual(sorted(complexity_estimation.__list_unique_kmers('A', 1)), sorted(['A']))

    def test_aa_2(self):
        self.assertListEqual(sorted(complexity_estimation.__list_unique_kmers('AA', 2)), sorted(['AA']))

    def test_aaa_3(self):
        self.assertListEqual(sorted(complexity_estimation.__list_unique_kmers('AAA', 3)), sorted(['AAA']))

    def test_at_1(self):
        self.assertListEqual(sorted(complexity_estimation.__list_unique_kmers('AT', 1)), sorted(['A', 'T']))

    def test_atcgatcg_4(self):
        self.assertListEqual(sorted(complexity_estimation.__list_unique_kmers('ATCGATCG', 4)),
                             sorted(['ATCG', 'TCGA', 'CGAT', 'GATC']))


class Tester_estimate_complexity_by_counting_kmers(TestCase):
    precision = 0.01

    def test_AAA(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('AAA'), 0.00, delta=self.precision)

    def test_AAAA(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('AAAA'), 0.00, delta=self.precision)

    def test_AAAAAAAA(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('AAAAAAAA'), 0.00, delta=self.precision)

    def test_AAT(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('AAT'), 0.67, delta=self.precision)

    def test_ATA(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('ATA'), 0.67, delta=self.precision)

    def test_AAAT(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('AAAT'), 0.5, delta=self.precision)

    def test_ATAT(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('ATAT'), 0.5, delta=self.precision)

    def test_AATT(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('AATT'), 0.67, delta=self.precision)

    def test_ATTA(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('ATTA'), 0.67, delta=self.precision)

    def test_AAAATTTT(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('AAAATTTT'), 0.67, delta=self.precision)

    def test_ATC(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('ATC'), 1.00, delta=self.precision)

    def test_ATTC(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('ATTC'), 0.83, delta=self.precision)

    def test_ATCG(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('ATCG'), 1.00, delta=self.precision)

    def test_ATCGGACT(self):
        self.assertAlmostEqual(complexity_estimation.estimate_complexity_by_counting_kmers('ATCGGACT'), 1.0, delta=self.precision)
