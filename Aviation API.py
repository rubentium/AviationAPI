import requests
import numpy as np
from sympy import Matrix, pprint

# Other links (unused) in the AviationStack API below

# airport_url = 'http://api.aviationstack.com/v1/airports'
# airlines_url = 'http://api.aviationstack.com/v1/airlines'
# airplanes_url = 'http://api.aviationstack.com/v1/airplanes'
# aircraft_tupe_url = 'http://api.aviationstack.com/v1/aircraft_types'
# aviation_taxes_url = 'http://api.aviationstack.com/v1/taxes'
# cities_url = 'http://api.aviationstack.com/v1/cities'
# countries_url = 'http://api.aviationstack.com/v1/countries'


class aviation_data:
    # Takes aviation data about flights, their arrivals and destinantions
    
    # The default limit for flights is 25 but the max is 100

    def __init__(self, APIKey=' YOUR API KEY') -> None:
        flights_url = 'http://api.aviationstack.com/v1/flights'
        params = {'access_key': APIKey, 'limit':25}
        r = requests.get(flights_url, params)
        self.status = r.status_code
        self._data = r.json()['data']


    def __meth1(self) -> dict:
        # creates a dictionary with all airports from the data above
        # assigns an index to each airport and an empty list

        airport_info = {}
        index = 0

        for flight in self._data:
            if flight['departure']['airport'] not in airport_info:
                    airport_info[flight['departure']['airport']] = [index, []]
                    index += 1
            if flight['arrival']['airport'] not in airport_info:
                    airport_info[flight['arrival']['airport']] = [index, []]
                    index += 1

        # initializes no direct connections between any two airports
        # no directconnection between a pair of airports is 0 

        for airport in airport_info:
            airport_info[airport][1] = [0]*len(airport_info)

        # returns the above dict
        return airport_info


    def meth2(self) -> dict:
        # creates a dictionary with keys as indices
        # and values as airports and returns it

        index_to_airport = {}
        airport_info = self.__meth1()

        for airport in airport_info:
            index_to_airport[airport_info[airport][0]] = airport
        
        return index_to_airport


    def connected_airports(self) -> dict:
        # changes 0 to 1 if theres is a connection between a pair of
        # airports and it's recorded in the airport info dictionary

        # NOTE: If there are multiple flights from one airport to
        # another, it will take them all as just one connection
        # between the two airports

        airport_info = self.__meth1()
        index_to_airport = self.meth2()

        for flight in self._data:
            dep_airport = flight['departure']['airport']
            arr_airport = flight['arrival']['airport']

            # takes the arrival airport and gives the index
            index_arr_airport = airport_info[arr_airport][0]

            airport_info[dep_airport][1][index_arr_airport] = 1

        return airport_info

    def __str__(self) -> str:
        return str(self._data)


    def matrix(self):
        # uses connected_airport data
        # to create an adjacency matrix
        # returns sympy matrix

        airport_info = self.connected_airports()
        matrix = []
        for airport in airport_info:
            row = airport_info[airport][1]
            matrix.append(row)

        return Matrix(matrix)

    def __jordan_calulator(self) -> tuple:
        # returns  P, J, P^-1 with M = P*J*P^-1
        M = self.matrix()
        P, J = M.jordan_form()
        P_inverse = P**-1
        return P, J, P_inverse

    def connections_bool(self, dep: int, arr: int, layover: int) -> bool:
        # Returns False if there are no flights from dep airport
        # to 'arr' airport with at most 'layover' number of layovers
        # and if there are, then it returns a tuple with True and 
        # the minimum number of layovers needed

        num_flight = layover + 1
        M = self.matrix
        P, J, P_inverse = self.__jordan_calulator()

        for i in range(1, num_flight+1):
            if i == 1:
                if M[dep][arr] != 0:
                    return True, 0
            else:
                M_exponent_i = P*(J**i)*P_inverse
                if M_exponent_i[dep][arr] != 0:
                                return True, i-1
        return False


    def departing_from(self, airport: str) -> bool:
        # if there are any departing flights from
        # the given airport then it returns True
        # else it returns False

        airport_info = self.__meth1()
        airport_ind = airport_info[airport][0]
        if sum(self.matrix().row(airport_ind)) != 0:
            return True
        return False


    def arriving_to(self, airport: str) -> bool:
        # if there are any arriving flights to
        # the given airport then it returns True
        # else it returns False

        airport_info = self.__meth1()
        airport_ind = airport_info[airport][0]
        if sum(self.matrix().col(airport_ind)) != 0:
            return True
        return False

    def _connection_helper(M, connection, index_to_airport) -> list:
        # takes a matrix and returns a list
        # of tuples where the first element is the
        # departure airport, the second is arrival,
        # and the third is the number of layovers + 1
        # if there is no connection between a pair of
        # airports then they wont be included in the list
 
        outlist = []
        for row_i in range(len(M.row(0))): # M is square matrix
            if sum(M.row(row_i)) > 0:
                for col_i in range(len(M.row(row_i))):
                    if M.row(row_i)[col_i] != 0:
                        outlist.append((index_to_airport[row_i], 
                                        index_to_airport[col_i], connection-1))
        return outlist

    def connections(self, layover: int, upto=False, func=_connection_helper) -> list[tuple]:
        # The documentation of the _connection_helper applies here too
        # as most of the job is done by the helper function
        # and this (connection) method mereley deals with different arguments
        # and is one of the methods of the class

        # When upto is False it chech the connections between a pair of
        # airports with specifically that number of layovers
        # when it's True, then it gives the pairs that have upto that
        # number of layovers

        out_list = []
        connection = layover + 1
        M = self.matrix()
        index_to_airport = self.meth2()
        P, J, P_inverse = self.__jordan_calulator()

        if not upto:
            if connection == 1:
                out_list += func(M, connection, index_to_airport)
            
            else:
                out_list += func(P*(J**connection)*P_inverse, connection, index_to_airport)

        else:
            for exponent in range(1, connection+1):
                out_list += func(P*(J**exponent)*P_inverse, exponent, index_to_airport)

        return out_list


# data = aviation_data()

# pprint(data.matrix())
# print(data.connections(0))
# print(data.connections(3))
# print(data.connections(0, True))
# print(data.connections(2, True))
# print(data.connections(3, True))
# print(data.arriving_to('Nanded'))
# print(data.departing_from('Nanded'))
# print(data.arriving_to('East Midlands'))
# print(data.departing_from('East Midlands'))
# print(data._data)
# print(data.status)