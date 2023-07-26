import math
from fractions import Fraction

import requests
from bs4 import BeautifulSoup


def convert_to_degrees(radian_str):
    """Function takes radians in string format and converts them to float degrees"""
    if 'π' in radian_str:
        # Handle the presence of π in the input string
        pi_fraction = Fraction(radian_str.replace('π', '1'))
        angle_in_radians = pi_fraction * math.pi
    else:
        # Convert the input string to a float if it doesn't contain π
        angle_in_radians = float(radian_str)

        # Convert radians to degrees
    angle_in_degrees = math.degrees(angle_in_radians)

    return angle_in_degrees


def get_tables_data(table_list):
    """
    Function takes list of tables (<table>) and scraps dh parameters for each robot
    Returns dictionary in format: {[NAME OF A ROBOT]: [INDEX OF JOINT]: {'theta': , 'r': , 'd': , 'alpha': }}
    """
    results = {}  # Save results as a dictionary
    for table in table_list:
        rows = table.findAll('tr')  # Get all rows
        name = ''
        for row in rows:
            table_data = row.findAll('td')  # Get all <td> elements from a row
            if len(table_data) == 1:  # If there is only one <td> element, then its header
                name = table_data[0].get_text()  # Get name of a robot
                results[name] = {}  # Create key for that robot
            elif table_data[0].text != 'Kinematics':
                # Scrap DH parameters for current joint
                joint_number = table_data[0].get_text()
                results[name][joint_number] = {'theta': 0, 'r': 0, 'd': 0, 'alpha': 0}
                results[name][joint_number]['theta'] = table_data[1].get_text()
                results[name][joint_number]['r'] = table_data[2].get_text()
                results[name][joint_number]['d'] = table_data[3].get_text()
                results[name][joint_number]['alpha'] = table_data[4].get_text()
    return results


def make_lists(parameters):
    """Function takes dictionary of one robot's DH parameters and breaks them into lists"""
    theta = [convert_to_degrees(parameters[f'Joint {i}']['theta']) for i in range(1, 7)]
    r = [float(parameters[f'Joint {i}']['r']) for i in range(1, 7)]
    d = [float(parameters[f'Joint {i}']['d']) for i in range(1, 7)]
    alpha = [convert_to_degrees(parameters[f'Joint {i}']['alpha']) for i in range(1, 7)]

    return theta, r, d, alpha


def convert_to_md(parameters):
    """Function takes dictionary of one robot's DH parameters and converts them to table in MD code"""
    # Take parameters to lists
    theta, r, d, alpha = make_lists(parameters)

    # Make MD code
    result = f'| i | r | d | alpha | theta |\n' \
             f'|---|---|---|-------|-------|\n' \
             f'| 1 |{r[0]}|{d[0]}|{alpha[0]}|{theta[0]}|\n' \
             f'| 2 |{r[1]}|{d[1]}|{alpha[1]}|{theta[1]}|\n' \
             f'| 3 |{r[2]}|{d[2]}|{alpha[2]}|{theta[2]}|\n' \
             f'| 4 |{r[3]}|{d[3]}|{alpha[3]}|{theta[3]}|\n' \
             f'| 5 |{r[4]}|{d[4]}|{alpha[4]}|{theta[4]}|\n' \
             f'| 6 |{r[5]}|{d[5]}|{alpha[5]}|{theta[5]}|\n'

    return result


def convert_to_m2(parameters):
    """Function takes dictionary of one robot's DH parameters and converts them to Macaulay2 code"""
    # Take parameters to lists
    theta, r, d, alpha = make_lists(parameters)

    # Make m2 code
    result = f'dof := 6;\n' \
             f'alpha := {{{alpha[0]}, {alpha[1]}, {alpha[2]}, {alpha[3]}, {alpha[4]}, {alpha[5]}}};\n' \
             f'r := {{{r[0]}, {r[1]}, {r[2]}, {r[3]}, {r[4]}, {r[5]}}};\n' \
             f'd := {{{d[0]}, {d[1]}, {d[2]}, {d[3]}, {d[4]}, {d[5]}}};\n' \
             f'theta := {{{theta[0]}, {theta[1]}, {theta[2]}, {theta[3]}, {theta[4]}, {theta[5]}}};\n' \
             f'dhParams := {{alpha, r, d, theta}};'
    return result


def finalize(name, parameters):
    """Function takes robots name and its parameters and returns finalized version for md document"""
    md = convert_to_md(parameters)
    m2 = convert_to_m2(parameters)
    result = f'## {name}\n' \
             f'### Parameters\n' \
             f'{md}\n' \
             f'### Macaulay2 code\n' \
             f'```\n' \
             f'{m2}\n' \
             f'```\n'

    return result


if __name__ == '__main__':
    url = 'https://www.universal-robots.com/articles/ur/application-installation/dh-parameters-for-calculations-of' \
          '-kinematics-and-dynamics/'
    response = requests.get(url)    # Make request

    if response.status_code == 200:
        html_content = response.text    # Get html
        soup = BeautifulSoup(html_content, 'html.parser')   # Parse to soup
        tables = soup.findAll('table')  # Get all tables
        data = get_tables_data(tables)  # Get dh parameters

        # Finalize each robot
        finals = []  # Contains final format for MD documents for each robot
        for robot in data:
            finals.append(finalize(robot, data[robot]))

        # Print a result
        for final in finals:
            print(final)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        exit()
