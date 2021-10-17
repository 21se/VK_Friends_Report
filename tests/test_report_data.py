from unittest import TestCase

from report_data import *


class TestNumSexToStr(TestCase):
    def test_num_sex_to_str_female(self):
        self.assertEqual(num_sex_to_str(1), 'Female')

    def test_num_sex_to_str_male(self):
        self.assertEqual(num_sex_to_str(2), 'Male')

    def test_num_sex_to_str_unknown(self):
        self.assertEqual(num_sex_to_str(3), 'Unknown')

    def test_num_sex_to_str_NaN(self):
        self.assertEqual(num_sex_to_str(float('nan')), 'Unknown')


class TestGetLocationFromDict(TestCase):
    def test_get_location_from_dict(self):
        correct_dict = {'id': 71, 'title': 'Greece'}
        self.assertEqual(get_location_from_dict(correct_dict), 'Greece')

    def test_get_location_from_dict_wrong(self):
        wrong_dict = {'id': 71, 'name': 'Greece'}
        self.assertEqual(get_location_from_dict(wrong_dict), 'Unknown')

    def test_get_location_from_dict_wrong_object(self):
        wrong_object = float('nan')
        self.assertEqual(get_location_from_dict(wrong_object), 'Unknown')


class TestDateToIso(TestCase):
    def test_date_to_iso(self):
        date = '17.09'
        self.assertEqual(date_to_iso(date), '0001-09-17')

    def test_date_to_iso_with_year(self):
        date = '5.9.1971'
        self.assertEqual(date_to_iso(date), '1971-09-05')

    def test_date_to_iso_wrong(self):
        wrong_date = '17/09/1971'
        self.assertRaises(ValueError, date_to_iso, wrong_date)

    def test_date_to_iso_wrong_object(self):
        wrong_object = float('nan')
        self.assertEqual(date_to_iso(wrong_object), '0001-01-01')

    def test_date_to_iso_day_not_in_range(self):
        wrong_date = '32.2.1995'
        self.assertRaises(ValueError, date_to_iso, wrong_date)

    def test_date_to_iso_month_not_in_range(self):
        wrong_date = '31.5005.1995'
        self.assertRaises(ValueError, date_to_iso, wrong_date)

    def test_date_to_iso_year_not_in_range(self):
        wrong_date = '5.9.0000'
        self.assertRaises(ValueError, date_to_iso, wrong_date)


class TestSaveDataFrameToFile(TestCase):
    def test_save_df_to_file_wrong_format(self):
        self.assertRaises(ValueError, save_df_to_file, pd.DataFrame(), 'C:/path/to/file.wrong_format', 'wrong_format')
