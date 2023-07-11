import string
from datetime import datetime
from typing import Dict, List


class EngineerRawData:
    """
    This class houses several methods to clean the extracted raw data.
    """

    @staticmethod
    def clean_case_number(case_number_str: str) -> str:
        """
        Cleans the case number to return a serialised code.
        Args:
            case_number_str: string of the case number scraped from site
        Returns:
            Formatted case number string
        """
        return ''.join(char for char in case_number_str if char in string.digits + string.punctuation)

    @staticmethod
    def split_age_range(age_range_str: str) -> Dict[str, int]:
        """
        Splits the age range into a minimum and maximum integar value.
        Args:
            age_range_str: String of the age range
        Returns:
            Dictionary of the min and maximum age values in the folm of {'MIN_AGE': x, 'MAX_AGE': y}
        """
        split_values = [age for age in '18 - 30'.split() if age.isdigit()]
        return {"MIN_AGE": min(split_values), "MAX_AGE": max(split_values)}

    @staticmethod
    def extract_height_cm(height_str: str) -> int:
        """
        Returns the height in cm.
        Args:
            height_str: String value of the height (typially containing cm and ft/inches)
        Returns:
            Integar of the height in cm
        """
        return height_str[:height_str.find('cm')]

    @staticmethod
    def format_date_found(date_found: str) -> datetime.date:
        """
        Formats a string date into a date object
        Args:
            date_found: string for the date found, typically in the "%d %B %Y" format
        Returns:
            Date object
        """
        date_format = "%d %B %Y"
        return datetime.strptime(date_found, date_format).date()

    @staticmethod
    def rough_format_distinguishing_features(dist_features_str: str) -> Dict[str, str]:
        """
        One of the more complex engineering tasks and requires a closer analysis.
        We separate this field into a list where possible.

        Typically, for distingusihing features these come as the following (split by a '-'):

            - CATEGORY: Represents the general category of the entry.
            - SUBCATEGORY: Provides additional details about the entry if available.
            - LOCATION: Indicates the specific body part or location mentioned in the entry.
            - DESCRIPTION: Describes any additional details or information related to the entry.

        Although this is not always the case, often the 'Description' field is missing.
        In some cases this structure is not adhered to whatsoever and it is just a free text input.
        """
        return_dict = {}

        # Split the entry string into a list by the new line character
        descriptors_list = [i for i in dist_features_str.split('\n') if len(i) > 1]

        for n, entry in enumerate(descriptors_list, start=1):
            # Attempt to split into the categories
            category_items = [i.strip().upper() for i in entry.split('-') if len(i) > 1]

            if len(category_items) < 2:
                continue

            category_dict = {
                "CATEGORY": None,
                "SUBCATEGORY": None,
                "LOCATION": None,
                "DESCRIPTION": None,
            }

            for j, key in zip(category_items, category_dict.keys()):
                category_dict[key] = j

            return_dict[f"FEATURE_{n}"] = category_dict

        return return_dict

    @staticmethod
    def rough_format_clothing(clothing_str: str) -> Dict[str, str]:
        """
        One of the more complex engineering tasks and requires a closer analysis.
        We separate this field into a list where possible.

        Typically, for clothing these come as the following (split by a '-'):

            - CATEGORY: Represents the general category type of the entry (footwear etc).
            - SUBCATEGORY: Provides additional details about the entry if available (shoes if CATEGORY is footwear for example).
            - COLOUR: Colour of the CATEGORY/SUBCATEGORY.
            - PATTERN: Describes the pattern of the entry.
            - DESCRIPTION: Describes any additional details or information related to the entry.

        Although this is not always the case, often the 'Description' field is missing.
        In some cases this structure is not adhered to whatsoever and it is just a free text input.
        """
        return_dict = {}

        # Split the entry string into a list by the new line character
        descriptors_list = [i for i in clothing_str.split('\n') if len(i) > 1]

        for n, entry in enumerate(descriptors_list, start=1):
            # Attempt to split into the categories
            category_items = [i.strip().upper() for i in entry.split('-') if len(i) > 1]

            if len(category_items) < 2:
                continue

            category_dict = {
                "CATEGORY": None,
                "SUBCATEGORY": None,
                "COLOUR": None,
                "PATTERN": None,
                "DESCRIPTION": None,
            }

            for j, key in zip(category_items, category_dict.keys()):
                category_dict[key] = j

            return_dict[f"CLOTHING_{n}"] = category_dict

        return return_dict

    @staticmethod
    def format_possessions(possessions_str: str) -> List[str]:

        split_char = ','
        if '(1)' in possessions_str:
            split_char = '(1)'

        return [i.strip().lower() for i in possessions_str.split(split_char) if len(i) > 1]

    @classmethod
    def format_raw_case_dict(cls, case_date_dict: Dict[str, str]) -> Dict[str, str]:

        case_dict_clean = {}

        # Clean case number
        case_dict_clean['CASE_NUMBER'] = cls.clean_case_number(case_number_str=case_date_dict['CASE_NUMBER'])

        # Location Road
        if case_date_dict.get('LOCATION_ROAD'):
            case_dict_clean['LOCATION_ROAD'] = case_date_dict['LOCATION_ROAD'].lower()
        else:
            case_dict_clean['LOCATION_ROAD'] = None

        # Location County
        if case_date_dict.get('LOCATION_COUNTY'):
            case_dict_clean['LOCATION_COUNTY'] = case_date_dict['LOCATION_COUNTY'].lower()
        else:
            case_dict_clean['LOCATION_COUNTY'] = None

        # Location Country
        if case_date_dict.get('LOCATION_COUNTRY'):
            case_dict_clean['LOCATION_COUNTRY'] = case_date_dict['LOCATION_COUNTRY'].lower()
        else:
            case_dict_clean['LOCATION_COUNTRY'] = None

        # Finding Party
        if case_date_dict.get('FINDING_PARTY'):
            case_dict_clean['FINDING_PARTY'] = case_date_dict['FINDING_PARTY'].lower()
        else:
            case_dict_clean['FINDING_PARTY'] = None

        # Clean gender value
        case_dict_clean['GENDER'] = case_date_dict['GENDER'].lower()

        # Clean age ranges
        case_dict_clean.update(cls.split_age_range(age_range_str=case_date_dict['AGE_RANGE']))

        # Clean ethnicity
        if case_date_dict.get('ETHNICITY'):
            case_dict_clean['ETHNICITY'] = case_date_dict['ETHNICITY'].lower()
        else:
            case_dict_clean['ETHNICITY'] = None

        # Clean Height
        if case_date_dict.get('HEIGHT'):
            case_dict_clean['HEIGHT_CM'] = cls.extract_height_cm(height_str=case_date_dict['HEIGHT'])
        else:
            case_dict_clean['HEIGHT_CM'] = None

        # Clean build
        if case_date_dict.get('BUILD'):
            case_dict_clean['BUILD'] = case_date_dict['BUILD'].lower()
        else:
            case_dict_clean['BUILD'] = None

        # Format date found
        case_dict_clean['DATE_FOUND'] = cls.format_date_found(date_found=case_date_dict['DATE_FOUND'])

        # Format estimated death date
        if case_date_dict.get('ESTIMATED_DEATH'):
            case_dict_clean['ESTIMATED_DEATH'] = cls.format_date_found(date_found=case_date_dict['ESTIMATED_DEATH'])
        else:
            case_dict_clean['ESTIMATED_DEATH'] = None

        # Format body found state
        case_dict_clean['BODY_OR_REMAINS'] = case_date_dict['BODY_OR_REMAINS'].lower()

        # Format hair
        if case_date_dict.get('HAIR'):
            case_dict_clean['HAIR'] = case_date_dict['HAIR'].lower()
        else:
            case_dict_clean['HAIR'] = None

        # Format facial hair
        if case_date_dict.get('FACIAL_HAIR'):
            case_dict_clean['FACIAL_HAIR'] = case_date_dict['FACIAL_HAIR'].lower()
        else:
            case_dict_clean['FACIAL_HAIR'] = None

        # Format eye colour
        case_dict_clean['EYE_COLOUR'] = case_date_dict['EYE_COLOUR'].lower()

        if case_date_dict.get('DISTINGUISHING_FEATURES'):
            case_dict_clean['DISTINGUISHING_FEATURES'] = cls.rough_format_distinguishing_features(
                    case_date_dict['DISTINGUISHING_FEATURES']
            )
        else:
            case_dict_clean['DISTINGUISHING_FEATURES'] = None

        if case_date_dict.get('CLOTHING'):
            case_dict_clean['CLOTHING'] = cls.rough_format_clothing(case_date_dict['CLOTHING'])
        else:
            case_dict_clean['CLOTHING'] = None

        if case_date_dict.get('POSSESSIONS'):
            case_dict_clean['POSSESSIONS'] = cls.format_possessions(possessions_str=case_date_dict['POSSESSIONS'])
        else:
            case_dict_clean['POSSESSIONS'] = None

        # Clean circumstances value
        if case_date_dict.get('CIRCUMSTANCES'):
            case_dict_clean['CIRCUMSTANCES'] = case_date_dict['CIRCUMSTANCES'].lower()
        else:
            case_dict_clean['CIRCUMSTANCES'] = None

        # Clean JEWELLERY value
        if case_date_dict.get('JEWELLERY'):
            case_dict_clean['JEWELLERY'] = case_date_dict['JEWELLERY'].lower()
        else:
            case_dict_clean['JEWELLERY'] = None

        # Clean known_not_to_be value
        if case_date_dict.get('KNOWN_NOT_TO_BE'):
            case_dict_clean['KNOWN_NOT_TO_BE'] = case_date_dict['KNOWN_NOT_TO_BE'].lower()
        else:
            case_dict_clean['KNOWN_NOT_TO_BE'] = None

        return case_dict_clean
