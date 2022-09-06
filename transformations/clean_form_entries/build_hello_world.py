expected_input = [{
    'first_name': 'Hello',
    'last_name': 'World',
}]

expected_output = [{
    **expected_input[0],
    'together': 'Hello World',
}]


def run(df):
    """
    It will create a full name property on the payload
    """
    df['together'] = df['first_name'] + ' ' + df['last_name']

    return df
