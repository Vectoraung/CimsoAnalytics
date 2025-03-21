class Enums:
    def __init__(self):
        pass

    def booking_status(value, by):
        enum_desc_mapping = {
            'Q': 'Quote',
            'E': 'Quote rejected',
            'W': 'Waiting list',
            'I': 'Internet',
            'P': 'Provisional',
            'C': 'Confirmed',
            'D': 'Deposit paid',
            'U': 'Fully paid',
            'A': 'Active',
            'L': 'Left',
            'N': 'No show',
            'F': 'Faulty',
            'X': 'Cancelled',
            'O': 'Closed',
            'R': 'Restricted'
        }

        if by == 'enum':
            # Return description based on enum value
            return enum_desc_mapping.get(value, 'Invalid enum')
        elif by == 'desc':
            # Return enum based on description
            for enum, desc in enum_desc_mapping.items():
                if desc.lower() == value.lower():
                    return enum
            return 'Invalid description'
        else:
            return 'Invalid "by" parameter. It should be "enum" or "desc".'